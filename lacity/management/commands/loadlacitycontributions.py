import logging
import requests
from optparse import make_option
from collections import OrderedDict
from lacity.process import parse_html
from django.core.management.base import BaseCommand
from lacity.models import (
    LACityContribution,
    LACityCandidate,
    LACityCommittee
)

# Some globals
logger = logging.getLogger('lacity')
COLUMN_TO_FIELD = OrderedDict([
    ('Last Name', 'last_name'),
    ('First Name', 'first_name'),
    ('Committee ID', 'committee_id'),
    ('Committee Name', 'name'),
    ('Committee Type', 'committee_type'),
    ('Office Type', 'office_type'),
    ('District Number', 'district_number'),
    ('Schedule', 'schedule'),
    ('Type', 'contribution_type'),
    ('Period Beg Date', 'filing_start_date'),
    ('Period End Date', 'filing_end_date'),
    ('Election Date', 'election_date'),
    ('Date', 'date'),
    ('Amount Rcvd', 'amount_received'),
    ('Amount Pd', 'amount_paid'),
    ('Description', 'description'),
    ('Contributor First Name', 'contributor_first_name'),
    ('Contributor Last Name', 'contributor_last_name'),
    ('Contributor Address', 'contributor_address_line_one'),
    ('Contributor Address 2', 'contributor_address_line_two'),
    ('Contributor City', 'contributor_city'),
    ('Contributor State', 'contributor_state'),
    ('Contributor Zip Code', 'contributor_zip_code'),
    ('Contributor Zip Code Ext', 'contributor_zip_code_ext'),
    ('Occupation', 'occupation'),
    ('Employer', 'employer'),
    ('Int Name', 'intermediary_name'),
    ('Int City', 'intermediary_city'),
    ('Int State', 'intermediary_state'),
    ('Int Zip Code', 'intermediary_zip_code'),
    ('Int Occupation', 'intermediary_occupation'),
    ('Int Employer', 'intermediary_employer'),
    ('Memo', 'memo'),
    ('Doc ID', 'document_id'),
    ('Rec ID', 'record_id'),
])
HEADERS = COLUMN_TO_FIELD.values()
FIELD_TO_COLUMN = dict(zip(COLUMN_TO_FIELD.values(), COLUMN_TO_FIELD.keys()))
CONTRIBUTION_FIELDS = [i.name for i in LACityContribution._meta.get_fields()]

custom_options = (
    make_option(
        "--load-from-file",
        action="store",
        dest="file_path",
        default=None,
        help="Skip downloading and load the data from a file"
    ),
    make_option(
        "--start-date",
        action="store",
        dest="start_date",
        default='01/01/2010',
        help="The start date for the contributions"
    ),
    make_option(
        "--end-date",
        action="store",
        dest="end_date",
        default='01/01/2020',
        help="The end date for the contributions"
    ),
)


class Command(BaseCommand):
    help = "Download, parse and load L.A. City campaign contributions"
    option_list = custom_options
    
    def handle(self, *args, **options):
        # Just for now
        LACityContribution.objects.all().delete()
        LACityCandidate.objects.all().delete()
        LACityCommittee.objects.all().delete()
        # Make the committee lookup more efficient
        self.committee_cache = {}
        # Grab the data, checking if we download it or use a custom file
        if options['file_path']:
            f = open(options['file_path'])
            data = parse_html(f.read())
            f.close()
        else:
            base_url = "http://ethics.lacity.org/disclosure/campaign/search/public_search_results.cfm"
            payload = {
                'viewtype': 'xl',
                'requesttimeout': '1500',
                'showall': 'yes',
                'orderbydesc': 'no',
                'REPT_TYPE': 'ALLCon',
                'PER_TYPE': 'A',
                'D_BDATE': options['start_date'],
                'D_EDATE': options['end_date'],
                'SCHEDULE': 'A,B,C',
            }
            logger.debug('Downloading LA City contributions')
            resp = requests.get(base_url, params=payload)
            
            # Check to see if we have a valid response
            if 'the system is experiencing an unexpected error' in resp.text:
                raise Exception("The website returned an error. Try a smaller date range.")
            
            # Parse the response
            logger.debug('Parsing LA City contributions')
            data = parse_html(resp.text)
        
        # Load it into the db
        self.load(data)
    
    def get_or_create_candidate(self, data):
        """
        Get or create a candidate object
        """
        try:
            candidate_obj = LACityCandidate.objects.get(
                first_name__iexact=data.get('first_name'),
                last_name__iexact=data.get('last_name'),
            )
        except LACityCandidate.DoesNotExist:
            candidate_obj = LACityCandidate.objects.create(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
            )
        
        return candidate_obj
    
    def get_or_create_committee(self, data):
        """
        Retrieve a committee object from the database,
        or create one on the fly.
        """
        committee_id = data.get('committee_id')
        committee_obj = self.committee_cache.get(committee_id)
        if committee_obj:
            return committee_obj

        try:
            committee_obj = LACityCommittee.objects.get(
                committee_id=committee_id
            )
        except LACityCommittee.DoesNotExist:
            candidate_obj = self.get_or_create_candidate(data)
            committee_obj = LACityCommittee.objects.create(
                committee_id=committee_id,
                name=data['name'],
                committee_type=data['committee_type'],
                lacitycandidate=candidate_obj,
            )
        
        # Set the cache and return the object.
        self.committee_cache[committee_id] = committee_obj
        return committee_obj
    
    def load(self, data):
        """
        Load our contributions into the database
        """
        # make a list for our bulk create
        bulk_contribs = []
        for contribution in data:
            # Make it a little easier to work with
            data_dict = dict(zip(HEADERS, contribution))
            # Grab/create our committee and candidate objects
            committee_obj = self.get_or_create_committee(data_dict)
            # make the contrib object
            fields = dict((k, v) for k, v in data_dict.items() if k in CONTRIBUTION_FIELDS)
            contrib = LACityContribution(**fields)
            contrib.lacitycommittee = committee_obj
            bulk_contribs.append(contrib)
        # Run our bulk create
        logger.debug('Running bulk create on %s contributions' % len(bulk_contribs))
        LACityContribution.objects.bulk_create(bulk_contribs)
        logger.debug("Finished loading contribs")