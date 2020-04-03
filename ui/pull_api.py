'''
Retrieve data from the U.S. Energy Information Administration's API.
Store the data as a csv file in './data'.
'''

import os
import csv
import json
import requests

PATH = "http://api.eia.gov/series/?api_key="
API = "2a31861f23d3efab0b0b4a9a37b8e893"
SOURCES = [('Natural Gas', 'NNTCB'), ('Coal', 'CLTCB'), ('Petroleum', 'PMTCB'),
            ('Nuclear', 'NUETB'), ('Renewable Energy', 'RETCB')]
DATA_DIR = os.path.dirname(__file__)
MANUAL_DIR = os.path.join(DATA_DIR, 'data', 'manually_created')


def gen_states(filename):
    '''
    Generates list of states.

    Inputs:
        - filename (string): name of file of state names
    Outputs:
        - list of state names
    '''
    with open(os.path.join(MANUAL_DIR, filename)) as f:
        f.readline()
        col = [tuple(line) for line in csv.reader(f)]

    return [x for x in col]


def retrieve_data(state, source):
    '''
    Retrieves data from API.

    Inputs:
        - state (string): name of state
        - source (string): energy source to retrieve

    Outputs:
        - data: dictionary containing energy source information for state
    '''
    api_url = PATH + API + "&series_id=SEDS." + source[1] + "." + state[1] + ".A"
    response = requests.get(api_url)
    response_dict = json.loads(response.text)
    data = response_dict['series'][0]['data']

    for i in data:
        i.append(state[0])
        i.append(source[0])

    return data


def combine_data(states, sources):
    '''
    Combines energy source data from all states into list.

    Inputs:
        - states: list of state names
        - sources: list of energy sources
    Outputs:
        - list of dictionaries for each state, containing energy data
    '''
    data = []
    for source in sources:
        for state in states:
            data.extend((retrieve_data(state, source)))

    return data


def output_data(index_filename):
    '''
    Writes data from API into csv.

    Input:
        - index_filename: name of output file name
    Output:
        - csv of state energy data for 1960-2017
    '''
    with open(index_filename, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter='|')
        data = combine_data(STATES, SOURCES)
        writer.writerow(['Year', 'Consumption', 'State', 'Source'])
        for r in data:
            if int(r[0]) >= 1960 and int(r[0]) <= 2017:
                writer.writerow(r)


if __name__ == "__main__":
    '''
    Pulls historical state energy data from API and outputs in csv.
    '''
    STATES = gen_states('states_abbrev.csv')
    output_data('data/energy_consumption_by_source_1960_2017.csv')
