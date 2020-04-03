'''
Crawl https://www.eia.gov/state/seds/seds-data-complete.php?sid=US
and retrieve all relevant data.
Store data in csv files in './data'.
Note: We ended up not using all the csv files scraped. The unused files
were moved to '../data/webscraped data not used'.
'''

import re
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

DATA_DIR = os.path.dirname(__file__)
OUTDIR = os.path.join(DATA_DIR, 'data')


def scrape_state_data():
    '''
    Scrapes data from webpage and outputs a csv file for each webpage.
    '''
    if not os.path.exists(OUTDIR):
        os.mkdir(OUTDIR)
    url_dict = make_url_dict()
    for k, v in url_dict.items():
        crawl_through_url(v).to_csv(os.path.join(OUTDIR, '{}.csv')\
            .format(k), encoding='utf-8', index=None, header=None)


def make_url_dict():
    '''
    Generates a dictionary of urls to scrape.
    '''
    url = 'https://www.eia.gov/state/seds/seds-data-complete.php?sid=US'
    page_request = requests.get(url)
    soup = BeautifulSoup(page_request.text, "html5lib")
    table_body = soup.find("table", {"class": "contable"})
    starting_url = 'https://www.eia.gov/statimport requestse/seds/'
    url_dict = dict()

    for row in table_body.findAll('tr'):
        html_link = row.find('a', href=True, text='\nHTML')
        if html_link:
            html_title = html_link['title'].lower().strip().replace(" ", "_")
            if ('energy' in html_title) and ('all_states' not in html_title):
                url_dict[html_title] = starting_url + html_link['href']

    return url_dict


def crawl_through_url(url):
    '''
    Crawls through given webpage, generating a table containing scraped data.

    Input:
        - url: url of webpage to scrape
    Output:
        - table containing data scraped from webpage
    '''
    page_request = requests.get(url)
    soup = BeautifulSoup(page_request.text, "html5lib")
    # state names dict
    state_dict, colnames = create_state_info_dict(soup)

    return create_state_table(state_dict, colnames)


def create_state_info_dict(soup):
    '''
    Creates dictionary containing state data.

    Input:
        - soup: beautiful soup object for a url
    Outputs:
        - state_dict: dictionary of state data scraped from webpage
        - colnames: column names corresponding with dictionary columns
    '''
    state_table = soup.find("table", {"class": "L2_toggle_table"})

    states = []
    for state in state_table.find_all('a', href=True):
        states.append(re.sub(r"\s+", " ", state.string).strip())
    state_dict = {state : {} for state in states}

    # map index to column name
    table = soup.find("table", {"class": "basic_table tpl"})
    table_body = table.find('tbody')

    colnames = []
    for x in table_body.findAll("td"):
        if x.attrs == {'colspan': '2'}:
            colnames.append(x.text)
    col_dict = dict(zip([1+i*2 for i in range(0, len(colnames), 1)], colnames))

    for row in table_body.findAll('tr'):
        row_list = [t.text.strip() for t in row.findAll('td')[1:]]
        if row_list and row_list[0] in state_dict:
            for i, r in enumerate(row_list):
                if i % 2 == 1:
                    state_dict[row_list[i-1]].update({col_dict[i]: r})

    state_dict = {k: v for k, v in state_dict.items() if len(v) > 0}

    return state_dict, colnames


def create_state_table(state_dict, colnames):
    '''
    Create table from dictionary and column names.

    Inputs:
        - state_dict: dictionary containing data
        - colnames: column names corresponding with dictionary columns

    Output:
        - state_df: dataframe containing data scraped from webpage
    '''
    state_dict = {k: v for k, v in sorted(state_dict.items(),
                                          key=lambda x: x[0])}
    state_df = pd.DataFrame(columns=['State'] + colnames)
    state_df['State'] = [state for state in state_dict]

    for colname in colnames:
        state_df[colname] = [col[colname] for col in state_dict.values()]

    return state_df


if __name__ == "__main__":
    scrape_state_data()
    