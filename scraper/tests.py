import re

from django.test import TestCase

import scraper.documents
import scraper.persons


class TestPersonInfoScraper(TestCase):

    def test_inititals(self):
        parlement_and_politiek_id = 'vg09llk9rzrp'
        initials_expected = 'F.C.G.M.'
        initials = scraper.persons.get_initials(parlement_and_politiek_id)
        self.assertEqual(initials, initials_expected)
        parlement_and_politiek_id = 'vg09lll5uqzx'
        initials_expected = 'S.A.M.'
        initials = scraper.persons.get_initials(parlement_and_politiek_id)
        self.assertEqual(initials, initials_expected)
        parlement_and_politiek_id = 'vjuuhtscjwpn'
        initials_expected = 'T.H.P.'
        initials = scraper.persons.get_initials(parlement_and_politiek_id)
        self.assertEqual(initials, initials_expected)


class TestDocumentScraper(TestCase):

    def test_document_metadata_kamerstuk_2016(self):
        document_id = 'kst-34575-2'
        metadata = scraper.documents.get_metadata(document_id)
        self.assertEqual(metadata['publication_type'], 'Kamerstuk')
        self.assertEqual(metadata['dossier_ids'], '34575')
        self.assertEqual(metadata['date_published'], '2016-10-13')
        self.assertEqual(metadata['title_short'], 'Voorstel van wet')
        self.assertEqual(metadata['title_full'], 'Wijziging van de Zorgverzekeringswet en de Wet op de zorgtoeslag in verband met enkele inhoudelijke en technische verbeteringen (Verzamelwet Zvw 2016); Voorstel van wet; Voorstel van wet')
        self.assertEqual(metadata['category'], 'Zorg en gezondheid | Ziekten en behandelingen')
        self.assertEqual(metadata['publisher'], 'Tweede Kamer der Staten-Generaal')
        self.assertEqual(metadata['submitter'], 'E.I. Schippers')
        self.assertEqual(metadata['publication_type'], 'Kamerstuk')

    def test_document_metadata_kamerstuk_2009(self):
        document_id = 'kst-32203-2'
        metadata = scraper.documents.get_metadata(document_id)
        self.assertEqual(metadata['publication_type'], 'Kamerstuk')
        self.assertEqual(metadata['dossier_ids'], '32203')
        self.assertEqual(metadata['date_published'], '2009-11-06')
        self.assertEqual(metadata['title_short'], 'officiële publicatie')
        self.assertEqual(metadata['title_full'], 'Voorstel van Wet van de leden Van der Ham, De Wit en Teeven tot wijziging van het Wetboek van Strafrecht in verband met het laten vervallen van het verbod op godslastering; Voorstel van wet')
        self.assertEqual(metadata['category'], 'Recht | Strafrecht|Recht | Staatsrecht|Cultuur en recreatie | Cultuur')
        self.assertEqual(metadata['publisher'], 'Tweede Kamer der Staten-Generaal')
        self.assertEqual(metadata['submitter'], 'Ham van der B.|Wit de J.M.A.M.|Teeven F.')
        self.assertEqual(metadata['publication_type'], 'Kamerstuk')

    def test_document_metadata_kamerstuk_multiple_dossiers(self):
        document_id = 'kst-33037-184'
        metadata = scraper.documents.get_metadata(document_id)
        self.assertEqual(metadata['publication_type'], 'Kamerstuk')
        self.assertEqual(metadata['dossier_ids'], '33037;34532')
