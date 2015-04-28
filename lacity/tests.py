import os
import datetime
from datetime import date
from django.test import TestCase
from django.core.management import call_command
from lacity.models import LACityContribution, LACityCommittee, LACityCandidate
from lacity.process import clean_string, parse_date, parse_html

TEST_DATA_FILE = os.path.join(
    os.path.dirname(__file__), 'data', 'test_download.html'
)


class LACityTest(TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Load data into the database before running other tests.
        """
        pass



class ProcessFunctionsTest(TestCase):
    
    def test_clean_string(self):
        # Strip
        self.assertEqual(
            clean_string('  foo '),
            'foo'
        )
        # Values that mean blank
        self.assertEqual(
            clean_string('&nbsp;'),
            ''
        )
        self.assertEqual(
            clean_string('N/A'),
            ''
        )
        # returns None
        self.assertEqual(
            clean_string(' ', return_none=True),
            None
        )
    
    def test_parse_date(self):
        # blank strings are None
        self.assertEqual(
            parse_date(''),
            None
        )
        # None should also just return None
        self.assertEqual(
            parse_date(None),
            None
        )
        # date with bogus time
        self.assertEqual(
            parse_date('01/01/15 00:00:00.0'),
            date(2015, 1, 1)
        )
        # default LA City formatting
        self.assertEqual(
            parse_date('01/01/15'),
            date(2015, 1, 1)
        )
    
    def test_parse_html(self):
        data_file = open(TEST_DATA_FILE)
        data = data_file.read()
        parsed = parse_html(data)
        self.assertEqual(
            parsed[0],
            [u'Preven', u'Eric', u'1374066',
            u'Preven for LA City Council 2015',
            u'C', u'CCM', u'C02', u'A', u'I',
            datetime.date(2015, 1, 1),
            datetime.date(2015, 1, 19),
            datetime.date(2015, 3, 3),
            datetime.date(2015, 1, 2),
            u'500.0000', u'0.0000', u'', u'James',
            u'Johnson', u'', u'', u'Studio City',
            u'CA', u'91604', u'', u'Musician', u'Self',
            u'', u'', u'CA', u'', u'', u'', u'',
            u'8442', u'A573004']
        )
        data_file.close()
