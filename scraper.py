"""Scraping King County foodsafety information."""

import requests
from bs4 import BeautifulSoup

INSPECTION_DOMAIN = 'http://info.kingcounty.gov'
INSPECTION_PATH = '/health/ehs/foodsafety/inspections/Results.aspx'
INSPECTION_PARAMS = {
    'Output': 'W',
    'Business_Name': '',
    'Business_Address': '',
    'Longitude': '',
    'Latitude': '',
    'City': '',
    'Zip_Code': '',
    'Inspection_Type': 'All',
    'Inspection_Start': '',
    'Inspection_End': '',
    'Inspection_Closed_Business': 'A',
    'Violation_Points': '',
    'Violation_Red_Points': '',
    'Violation_Descr': '',
    'Fuzzy_Search': 'N',
    'Sort': 'B'
}


def get_inspection_page(**kwargs):
    """Return inspection information for given search."""
    url = INSPECTION_DOMAIN + INSPECTION_PATH
    params = INSPECTION_PARAMS.copy()
    for key, val in kwargs.items():
        if key in INSPECTION_PARAMS:
            params[key] = val
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.content, resp.encoding


def load_inspection_page():
    """Load response from inspection_page."""
    with open('inspection_page.html', 'r') as f:
        content = f.read()
        encoding = 'utf-8'
    return content, encoding


def write_results(results):
    """Write results of search to file."""
    with open('inspection_page.html', 'w') as f:
        f.write(results)


def parse_source(html, encoding='utf-8'):
    """Set up HTML as DOM nodes for scraping."""
    soup = BeautifulSoup(html, 'html5lib', from_encoding=encoding)
    return soup
