'''
Retrieve the relevant data from the database
to be displayed in a table as results.
'''

import sqlite3
import os

DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'db.sqlite3')


QUERY = '''SELECT t.state "State",
            t.coal "Coal (Tn Btu)", 
            t.natural_gas "Natural Gas (Tn Btu)", 
            t.petroleum "Petroleum (Tn Btu)", 
            t.nuclear "Nuclear (Tn Btu)", 
            t.renewable "Renewable (Tn Btu)", 
            p.prices "$/M Btu (all sources)"
            FROM energy_consumption_by_source as t JOIN price_expenditure as p
            ON t.state = p.state 
            WHERE t.state = ?
            UNION
            SELECT t.state "State",
            t.coal "Coal (Tn Btu)", 
            t.natural_gas "Natural Gas (Tn Btu)", 
            t.petroleum "Petroleum (Tn Btu)", 
            t.nuclear "Nuclear (Tn Btu)", 
            t.renewable "Renewable (Tn Btu)", 
            p.prices "$/M Btu (all sources)"
            FROM energy_consumption_by_source as t JOIN price_expenditure as p
            ON t.state = p.state 
            WHERE t.state = ?'''


def retrieve_state_data(args_from_ui, query=QUERY):
    '''
    Given a query, retrieve the relevant data from the database.
    '''

    if not args_from_ui:
        return ([], [])

    conn = sqlite3.connect(DATABASE_FILENAME)
    c = conn.cursor()

    params = [args_from_ui['your_state'], args_from_ui['comparison_state']]
    rv = c.execute(query, params).fetchall()
    header = get_header(c.execute(query, params))

    conn.close()

    return (header, rv)


def get_header(cursor):
    '''
    Given a cursor object, returns the appropriate header (column names).
    '''

    header = []

    for i in cursor.description:
        s = i[0]
        if "." in s:
            s = s[s.find(".")+1:]
        header.append(s)

    return header
