from datetime import date
from django.test import TestCase
from django.core.management import call_command
from lacity.models import LACityContribution, LACityCommittee, LACityCandidate
from lacity.process import clean_string, parse_date, parse_html

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
            parse_date('2014-06-03 00:00:00.0'),
            date(2014, 6, 3)
        )
        # default LA City formatting
        self.assertEqual(
            parse_date('2014-06-03'),
            date(2014, 6, 3)
        )
    
    def test_parse_html(self):
        
        