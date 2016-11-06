import logging
import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView

import django_filters
from dal import autocomplete

from person.models import Person

from document.models import Agenda, AgendaItem
from document.models import BesluitenLijst
from document.models import CategoryDossier
from document.models import Document, Kamerstuk
from document.models import Dossier
from document.models import Voting
from document import settings

# TODO: remove dependency on website
from website.create import create_or_update_dossier

logger = logging.getLogger(__name__)


class DocumentView(TemplateView):
    template_name = 'document/document.html'

    def get_context_data(self, document_id, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document'] = Document.objects.get(document_id=document_id)
        return context


class KamerstukView(TemplateView):
    template_name = 'document/kamerstuk.html'

    def get_context_data(self, dossier_id, sub_id, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kamerstuk'] = Kamerstuk.objects.get(id_main=dossier_id, id_sub=sub_id)
        return context


class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        persons = Person.objects.exclude(surname='').order_by('surname')
        person_ids = []
        if self.q:
            for person in persons:
                if self.q in person.fullname():
                    person_ids.append(person.id)
            return Person.objects.filter(pk__in=person_ids)
        return persons


class DossierFilter(django_filters.FilterSet):
    VOTING_RESULT_CHOICES = (
        ('ALL', 'Alle'),
        (Voting.AANGENOMEN, 'Aangenomen'),
        (Voting.VERWORPEN, 'Verworpen'),
    )
    title = django_filters.CharFilter(method='title_filter', label='')
    submitter = django_filters.ModelChoiceFilter(
        queryset=Person.objects.all(),
        method='submitter_filter',
        label='',
        widget=autocomplete.ModelSelect2(url='person-autocomplete')
    )
    voting_result = django_filters.ChoiceFilter(
        choices=VOTING_RESULT_CHOICES,
        method='voting_result_filter',
        # widget=forms.ChoiceField()
    )
    categories = django_filters.ModelMultipleChoiceFilter(
        name='categories',
        queryset=CategoryDossier.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Dossier

    def title_filter(self, queryset, name, value):
        dossiers = queryset.filter(document__title_full__icontains=value).distinct()
        return dossiers

    def submitter_filter(self, queryset, name, value):
        dossiers = queryset.filter(document__submitter__person=value).distinct()
        return dossiers

    def voting_result_filter(self, queryset, name, value):
        if value == 'ALL':
            return queryset
        dossier_ids = []
        for dossier in queryset:
            if dossier.voting() and dossier.voting().result == value:
                dossier_ids.append(dossier.id)
        return Dossier.objects.filter(pk__in=dossier_ids)


class DossiersView(TemplateView):
    template_name = 'document/dossiers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dossiers = DossierFilter(self.request.GET, queryset=Dossier.objects.all())
        paginator = Paginator(dossiers, settings.DOSSIERS_PER_PAGE)
        page = self.request.GET.get('page')
        try:
            dossiers = paginator.page(page)
        except PageNotAnInteger:
            dossiers = paginator.page(1)
        except EmptyPage:
            dossiers = paginator.page(paginator.num_pages)
        context['dossiers'] = dossiers
        context['filter'] = DossierFilter(self.request.GET, queryset=Dossier.objects.all())
        return context


class DossierView(TemplateView):
    template_name = 'document/dossier.html'

    def get_context_data(self, dossier_id, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dossier'] = Dossier.objects.get(dossier_id=dossier_id)
        return context


class TimelineItem(object):
    def __init__(self, obj):
        self.obj = obj

    @staticmethod
    def template_name():
        raise NotImplementedError

    @property
    def date(self):
        raise NotImplementedError


class TimelineKamerstukItem(TimelineItem):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def template_name():
        return 'document/items/timeline_kamerstuk.html'

    @property
    def date(self):
        return self.obj.document.date_published


class TimelineBesluitItem(TimelineItem):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def template_name():
        return 'document/items/timeline_besluit.html'

    @property
    def date(self):
        return self.obj.besluit_item.besluiten_lijst.date_published


class DossierTimelineView(TemplateView):
    template_name = 'document/dossier_timeline.html'

    def get_context_data(self, dossier_id, **kwargs):
        context = super().get_context_data(**kwargs)
        dossier = Dossier.objects.get(dossier_id=dossier_id)
        context['dossier'] = dossier
        timeline_items = []
        for kamerstuk in dossier.kamerstukken():
            timeline_items.append(TimelineKamerstukItem(kamerstuk))
        for case in dossier.besluitenlijst_cases():
            timeline_items.append(TimelineBesluitItem(case))
        timeline_items = sorted(timeline_items, key=lambda items: items.date, reverse=True)
        context['timeline_items'] = timeline_items
        return context


class DossierTimelineHorizontalView(TemplateView):
    template_name = 'document/dossier_timeline_horizontal.html'

    def get_context_data(self, dossier_id, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dossier'] = Dossier.objects.get(dossier_id=dossier_id)
        return context


class AgendasView(TemplateView):
    template_name = 'document/agendas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agendas'] = Agenda.objects.all()
        return context


class AgendaView(TemplateView):
    template_name = 'document/agenda.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agenda = Agenda.objects.get(id=self.kwargs['pk'])
        context['agenda'] = agenda
        context['agendaitems'] = AgendaItem.objects.filter(agenda=agenda)
        return context


class AddDossierView(TemplateView):
    template_name = 'document/dossier.html'

    def get(self, request, **kwargs):
        super().get(request=request, **kwargs)
        dossiers = Dossier.objects.filter(dossier_id=self.kwargs['dossier_id'])
        if dossiers.exists():
            dossier = dossiers[0]
        else:
            dossier = create_or_update_dossier(self.kwargs['dossier_id'])
        return redirect(reverse('dossier-timeline', args=(dossier.dossier_id,)))
        # return HttpResponseRedirect()


class VotingView(TemplateView):
    template_name = 'document/voting.html'

    def get_context_data(self, voting_id, **kwargs):
        context = super().get_context_data(**kwargs)
        voting = Voting.objects.get(id=voting_id)
        context['voting'] = voting
        return context


class VotingsView(TemplateView):
    template_name = 'document/votings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(Voting.objects.all(), settings.VOTINGS_PER_PAGE)
        page = self.request.GET.get('page')
        try:
            votings = paginator.page(page)
        except PageNotAnInteger:
            votings = paginator.page(1)
        except EmptyPage:
            votings = paginator.page(paginator.num_pages)
        context['votings'] = votings
        return context


class BesluitenLijstenView(TemplateView):
    template_name = 'document/besluitenlijsten.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(BesluitenLijst.objects.all(), settings.BESLUITENLIJSTEN_PER_PAGE)
        page = self.request.GET.get('page')
        try:
            besluitenlijsten = paginator.page(page)
        except PageNotAnInteger:
            besluitenlijsten = paginator.page(1)
        except EmptyPage:
            besluitenlijsten = paginator.page(paginator.num_pages)
        context['besluitenlijsten'] = besluitenlijsten
        return context


class BesluitenLijstView(TemplateView):
    template_name = 'document/besluitenlijst.html'

    def get_context_data(self, activity_id, **kwargs):
        context = super().get_context_data(**kwargs)
        context['besluitenlijst'] = BesluitenLijst.objects.get(activity_id=activity_id)
        return context
