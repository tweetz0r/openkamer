import datetime
import gzip
import logging
import os
import shutil
import traceback
import time

import fasteners

from django.core import management
from django.conf import settings
from django_cron import CronJobBase, Schedule
from django.db import transaction


from document.models import Submitter
from government.models import GovernmentMember
from parliament.models import PartyMember
from parliament.models import ParliamentMember
from person.models import Person

import openkamer.besluitenlijst
import openkamer.dossier
import openkamer.gift
import openkamer.kamervraag
import openkamer.parliament
import openkamer.travel
import openkamer.verslagao

import stats.models

from website import settings

logger = logging.getLogger(__name__)


def years_from_str_list(year_start):
    start_date = datetime.date(year=int(year_start), month=1, day=1)
    current_date = start_date
    today = datetime.date.today()
    years = []
    while current_date.year <= today.year:
        years.append(str(current_date.year))
        current_date = datetime.date(year=current_date.year + 1, month=1, day=1)
    years.reverse()
    return years


class LockJob(CronJobBase):
    """
    django-cron does provide a file lock backend,
    but this is not working due to issue https://github.com/Tivix/django-cron/issues/74
    """

    def do(self):
        logger.info('BEGIN')
        lockfilepath = os.path.join(settings.CRON_LOCK_DIR, 'tmp_' + self.code + '_lockfile')
        a_lock = fasteners.InterProcessLock(lockfilepath)
        gotten = a_lock.acquire(timeout=1.0)
        try:
            if gotten:
                self.do_imp()
            else:
                logger.info('Not able to acquire lock, job is already running')
        finally:
            if gotten:
                a_lock.release()
        logger.info('END')

    def do_imp(self):
        raise NotImplementedError


class TestJob(LockJob):
    RUN_EVERY_MINS = 0
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'website.cron.TestJob'

    def do_imp(self):
        logger.info('BEGIN')
        time.sleep(10)
        logger.info('END')


class UpdateParliamentAndGovernment(LockJob):
    RUN_AT_TIMES = ['20:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'website.cron.UpdateParliamentAndGovernment'

    def do_imp(self):
        logger.info('BEGIN')
        try:
            openkamer.parliament.create_parliament_and_government()
        except Exception as error:
            logger.exception(error)
            raise
        logger.info('END')


class UpdateActiveDossiers(LockJob):
    RUN_AT_TIMES = ['21:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'website.cron.UpdateActiveDossiers'

    def do_imp(self):
        # TODO: also update dossiers that have closed since last update
        logger.info('update active dossiers cronjob')
        failed_dossiers = openkamer.dossier.create_wetsvoorstellen_active()
        if failed_dossiers:
            logger.error('the following dossiers failed: ' + str(failed_dossiers))


class UpdateInactiveDossiers(LockJob):
    RUN_AT_TIMES = ['22:00']  # note that while it runs every day, it only updates a set depending on the week day
    DAYS_PER_WEEK = 7
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'website.cron.UpdateInactiveDossiers'

    def do_imp(self):
        logger.info('update inactive dossiers cronjob')
        week_day = datetime.datetime.today().weekday()
        try:
            years = years_from_str_list(2008)
            for year in years:
                year = int(year)
                if year % self.DAYS_PER_WEEK == week_day:
                    failed_dossiers = openkamer.dossier.create_wetsvoorstellen_inactive(year=year)
                    if failed_dossiers:
                        logger.error('the following dossiers failed: {}'.format(failed_dossiers))
        except:
            logger.exception('something failed')


class UpdateVerslagenAlgemeenOverleg(LockJob):
    RUN_AT_TIMES = ['23:30']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'website.cron.UpdateVerslagenAlgemeenOverleg'

    def do_imp(self):
        logger.info('update verslagen algemeen overleg')
        skip_if_exists = datetime.date.today().day % 7 == 0
        years = years_from_str_list(2008)
        for year in years:
            openkamer.verslagao.create_verslagen_algemeen_overleg(year, max_n=None, skip_if_exists=skip_if_exists)


class UpdateKamervragenRecent(LockJob):
    RUN_AT_TIMES = ['00:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'website.cron.UpdateKamervragenRecent'

    def do_imp(self):
        logger.info('update kamervragen and kamerantwoorden')
        years = years_from_str_list(2019)
        for year in years:
            openkamer.kamervraag.create_kamervragen(year, skip_if_exists=False)


class UpdateKamervragenAll(LockJob):
    RUN_EVERY_MINS = 60 * 24 * 7  # 7 days
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'website.cron.UpdateKamervragenAll'

    def do_imp(self):
        logger.info('update kamervragen and kamerantwoorden')
        years = years_from_str_list(2010)
        for year in years:
            openkamer.kamervraag.create_kamervragen(year, skip_if_exists=False)


class UpdateSubmitters(LockJob):
    RUN_AT_TIMES = ['05:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'website.cron.UpdateSubmitters'

    def do_imp(self):
        logger.info('BEGIN')
        try:
            submitters = Submitter.objects.all()
            n_total = submitters.count()
            logger.info('submitters: ' + str(n_total))
            counter = 0
            progress_percent = 0
            submitters_batch = []
            for submitter in submitters:
                submitters_batch.append(submitter)
                if counter/n_total*100 > (progress_percent+1):
                    self.update_batch(submitters_batch)
                    submitters_batch = []
                    progress_percent = counter/n_total*100
                    logger.info(str(int(progress_percent)) + '%')
                counter += 1
        except Exception as error:
            logger.exception(error)
            raise
        logger.info('END')

    @transaction.atomic
    def update_batch(self, submitters):
        for submitter in submitters:
            submitter.update_submitter_party_slug()


class UpdateSearchIndex(LockJob):
    RUN_AT_TIMES = ['06:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'website.cron.UpdateSearchIndex'

    def do_imp(self):
        logger.info('BEGIN')
        try:
            management.call_command('update_index', remove=True)
        except Exception as error:
            logger.exception(error)
            raise
        logger.info('END')


class UpdateStatsData(LockJob):
    RUN_AT_TIMES = ['07:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'website.cron.UpdateStatsData'

    def do_imp(self):
        logger.info('BEGIN')
        try:
            stats.models.update_all()
        except Exception as error:
            logger.exception(error)
            raise
        logger.info('END')


class UpdateGifts(LockJob):
    RUN_AT_TIMES = ['12:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'website.cron.UpdateGifts'

    def do_imp(self):
        logger.info('BEGIN')
        try:
            openkamer.gift.create_gifts()
        except Exception as error:
            logger.exception(error)
            raise
        logger.info('END')


class UpdateTravels(LockJob):
    RUN_AT_TIMES = ['14:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'website.cron.UpdateTravels'

    def do_imp(self):
        logger.info('BEGIN')
        try:
            openkamer.travel.create_travels()
        except Exception as error:
            logger.exception(error)
            raise
        logger.info('END')


class CleanUnusedPersons(CronJobBase):
    RUN_AT_TIMES = ['08:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'website.cron.CleanUnusedPersons'

    def do(self):
        logger.info('run unused persons cleanup')
        persons = Person.objects.all()
        persons_to_delete_ids = []
        for person in persons:
            members = PartyMember.objects.filter(person=person)
            if members:
                continue
            members = ParliamentMember.objects.filter(person=person)
            if members:
                continue
            members = GovernmentMember.objects.filter(person=person)
            if members:
                continue
            submitters = Submitter.objects.filter(person=person)
            if submitters:
                continue
            persons_to_delete_ids.append(person.id)
        Person.objects.filter(id__in=persons_to_delete_ids).delete()
        logger.info('deleted persons: ' + str(persons_to_delete_ids))
        logger.info('END')


class BackupDaily(LockJob):
    RUN_AT_TIMES = ['18:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'website.cron.BackupDaily'

    def do_imp(self):
        logger.info('run daily backup cronjob')
        management.call_command('dbbackup', '--clean')
        try:
            BackupDaily.create_json_dump()
        except Exception as e:
            logger.exception(e)
            raise

    @staticmethod
    def create_json_dump():
        filepath = os.path.join(settings.DBBACKUP_STORAGE_OPTIONS['location'], 'openkamer-' + str(datetime.date.today()) + '.json')
        filepath_compressed = filepath + '.gz'
        with open(filepath, 'w') as fileout:
            management.call_command(
                'dumpdata',
                '--all',
                '--natural-foreign',
                '--exclude', 'auth.permission',
                '--exclude', 'contenttypes',
                'person',
                'parliament',
                'government',
                'document',
                'stats',
                'website',
                stdout=fileout
            )
        with open(filepath, 'rb') as f_in:
            with gzip.open(filepath_compressed, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(filepath)
        BackupDaily.remove_old_json_dumps(days_old=30)

    @staticmethod
    def remove_old_json_dumps(days_old):
        for (dirpath, dirnames, filenames) in os.walk(settings.DBBACKUP_STORAGE_OPTIONS['location']):
            for file in filenames:
                if '.json.gz' not in file:
                    continue
                filepath = os.path.join(dirpath, file)
                datetime_created = datetime.datetime.fromtimestamp(os.path.getctime(filepath))
                if datetime_created < datetime.datetime.now() - datetime.timedelta(days=days_old):
                    os.remove(filepath)
