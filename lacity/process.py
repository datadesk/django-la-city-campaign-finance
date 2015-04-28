from bs4 import BeautifulSoup
from datetime import datetime

# The rows in our data that have dates
# we will need to parse.
DATE_ROWS = [9, 10, 11, 12]


def clean_string(value, return_none=False):
    """
    Simple cleanup for a raw string coming out of the download.

    If return_none is True, will return None instead of an empty string.
    """
    value = value.strip()
    if value in ['&nbsp;', 'N/A']:
        value = ''

    if return_none and value == '':
        return None

    return value


def parse_date(datestring):
    """
    Takes a date formatted like "01/01/15 00:00:00.0"

    Removes the bogus time, and returns a Python date object.
    """
    if datestring is None or datestring == '':
        return None

    datestring = datestring[:8]
    return datetime.strptime(datestring, '%m/%d/%y').date()


def parse_html(html):
    """
    Takes an HTML table formatted data download from the county, and returns
    a nice list
    """
    soup = BeautifulSoup(html)
    table = soup.find("table")
    data = []
    for row in table.findAll('tr')[1:]:
        temp = []
        for index, column in enumerate(row.findAll('td')):
            val = clean_string(column.string)
            # see if we have a date and parse it
            if index in DATE_ROWS:
                val = parse_date(val)

            temp.append(val)
        data.append(temp)
    return data
