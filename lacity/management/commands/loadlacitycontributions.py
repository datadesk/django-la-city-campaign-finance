import logging
import requests
from django.core.management.base import BaseCommand
from lacity.process import parse_html
from lacity.models import (LACityContribution,
    LACityCandidate, LACityCommittee)
logger = logging.getLogger('lacity')


class Command(BaseCommand):
    help = "Download, parse and load L.A. City campaign contributions"
    
    def handle(self, *args, **options):
        # Grab the URL
        base_url = "http://ethics.lacity.org/disclosure/campaign/search/public_search_results.cfm"
        payload = {
            'viewtype': 'xl',
            'requesttimeout': '1500',
            'showall': 'yes',
            'orderbydesc': 'no'
            'REPT_TYPE': 'ALLCon',
            'PER_TYPE': 'A',
            'D_BDATE': '01/01/1998',
            'D_EDATE': '01/01/2020',
            'SCHEDULE': 'A,B,C',
        }
        resp = requests.get(base_url, params=payload)
        # Parse the response
        data = parse_html(resp.text)


orderby=RPT_DATE
D_BDATE=01/01/1990

CITY=la
FIELDNAMES=CITY,REPT_TYPE,PER_TYPE,CAND_PER_ID,CMT_PER_ID,CID_CRIT,S_TYPE,LNM_CRIT,FNM_CRIT,CNM_CRIT,ST_CRIT,ZIP_CRIT,ENM_CRIT,OCC_CRIT,D_BDATE,D_EDATE,S_BAMT,S_EAMT,SCHEDULE,SUBMITBTN
D_EDATE=01/01/2000


Last Name
First Name
Committee ID
Committee Name
Committee Type
Office Type
District Number
Schedule
Type
Period Beg Date
Period End Date
Election Date
Date
Amount Rcvd
Amount Pd
Description
Contributor First Name
Contributor Last Name
Contributor Address
Contributor Address 2
Contributor City
Contributor State
Contributor Zip Code
Contributor Zip Code Ext
Occupation
Employer
Int Name
Int City
Int State
Int Zip Code
Int Occupation
Int Employer
Memo
Doc ID 
Rec ID