import logging
import requests
from django.core.management.base import BaseCommand
from lacity.process import parse_html
from lacity.models import (LACityContribution,
    LACityCandidate, LACityCommittee)
logger = logging.getLogger('lacity')

COLUMN_TO_FIELD = {
    # 'Last Name': ,
    # 'First Name': ,
    # 'Committee ID': ,
    # 'Committee Name': ,
    # 'Committee Type': ,
    'Office Type': 'office_type',
    'District Number': 'district_number',
    'Schedule': 'schedule',
    'Type': 'contribution_type',
    'Period Beg Date': 'filing_start_date',
    'Period End Date': 'filing_end_date',
    'Election Date': 'election_date',
    'Date': 'date',
    'Amount Rcvd': 'amount_received',
    'Amount Pd': 'amount_paid',
    'Description': 'description',
    'Contributor First Name': 'contributor_first_name',
    'Contributor Last Name': 'contributor_last_name',
    'Contributor Address': 'contributor_address_line_one',
    'Contributor Address 2': 'contributor_address_line_two',
    'Contributor City': 'contributor_city',
    'Contributor State': 'contributor_state',
    'Contributor Zip Code': 'contributor_zip_code',
    'Contributor Zip Code Ext': 'contributor_zip_code_ext',
    'Occupation': 'occupation',
    'Employer': 'employer',
    'Int Name': 'intermediary_name',
    'Int City': 'intermediary_city',
    'Int State': 'intermediary_state',
    'Int Zip Code': 'intermediary_zip_code',
    'Int Occupation': 'intermediary_occupation',
    'Int Employer': 'intermediary_employer',
    'Memo': 'memo',
    'Doc ID': 'document_id',
    'Rec ID': 'record_id',
}


class Command(BaseCommand):
    help = "Download, parse and load L.A. City campaign contributions"
    
    def handle(self, *args, **options):
        # Grab the data
        base_url = "http://ethics.lacity.org/disclosure/campaign/search/public_search_results.cfm"
        payload = {
            'viewtype': 'xl',
            'requesttimeout': '1500',
            'showall': 'yes',
            'orderbydesc': 'no'
            'REPT_TYPE': 'ALLCon',
            'PER_TYPE': 'A',
            'D_BDATE': '01/01/1998',
            'D_EDATE': '01/01/2000',
            # 'D_EDATE': '01/01/2020',
            'SCHEDULE': 'A,B,C',
        }
        logger.debug('Downloading LA City contributions')
        resp = requests.get(base_url, params=payload)
        # Parse the response
        logger.debug('Parsing LA City contributions')
        data = parse_html(resp.text)
    
    def load(self, data):
        """
        Load our contributions into the database
        """
        pass
    
    def get_or_create_committee(self, data):
        """
        Retrieve a committee object from the database,
        or create one on the fly.
        """
        committee_obj = self.committee_cache.get(data.get('committee_id'))
        if committee_obj:
            return committee_obj

        try:
            committee_obj = Committee.objects.get(committee_id=data.get('committee_id'))
        except Committee.DoesNotExist:
            committee_obj = Committee.objects.create(
                committee_id=data.get('committee_id'),
                name=data['committee_name'],
                committee_type=data['committee_type'],
            )

        return committee_obj


