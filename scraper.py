"""Scraping King County foodsafety information."""

# http://info.kingcounty.gov/health/ehs/foodsafety/inspections/Results.aspx?Output=W&Business_Name=Tango&Business_Address=1100%20Pike%20st&Longitude=&Latitude=&City=Seattle&Zip_Code=98101&Inspection_Type=All&Inspection_Start=&Inspection_End=&Inspection_Closed_Business=A&Violation_Points=&Violation_Red_Points=&Violation_Descr=&Fuzzy_Search=N&Sort=B

import requests
from bs4 import BeautifulSoup
import sys
import re

INSPECTION_DOMAIN = 'http://info.kingcounty.gov'
INSPECTION_PATH = '/health/ehs/foodsafety/inspections/Results.aspx'
INSPECTION_PARAMS = {
    "Output": "W",
    "Business_Name": "",
    "Business_Address": "",
    "Longitude": "",
    "Latitude": "",
    "City": "",
    "Zip_Code": "",
    "Inspection_Type": "All",
    "Inspection_Start": "",
    "Inspection_End": "",
    "Inspection_Closed_Business": "A",
    "Violation_Points": "",
    "Violation_Red_Points": "",
    "Violation_Descr": "",
    "Fuzzy_Search": "N",
    "Sort": "B",
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


def extract_data_listings(html):
    """Extract container with data."""
    id_finder = re.compile(r'PR[\d]+~')
    return html.find_all('div', id=id_finder)


def has_two_tds(element):
    """Take an element and return true if contains two tds."""
    is_tr = element.name == 'tr'
    td_children = element.find_all('td', recursive=False)
    has_two = len(td_children) == 2
    return is_tr and has_two


if __name__ == '__main__':
    kwargs = {
        'Inspection_Start': '2/1/2013',
        'Inspection_End': '2/1/2015',
        'Zip_Code': '98109'
    }
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = load_inspection_page()
    else:
        html, encoding = get_inspection_page(**kwargs)
    doc = parse_source(html, encoding)
    listings = extract_data_listings(doc)
    for listing in listings:  # <- add this stuff here.
        metadata_rows = listing.find('tbody').find_all(
            has_two_tds, recursive=False
        )
        print(len(metadata_rows))
