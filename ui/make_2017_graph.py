'''
Using data in './data/2017_____.csv' files, plot bar graphs
showing the composition of energy sources for each state in 2017.
Store graphs in './static/graphs' to be displayed in final UI.
'''

import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.style as style
import matplotlib.pyplot as plt
style.use('fivethirtyeight')

TOTAL_SQL = "SELECT * FROM energy_consumption_by_source"
RENEW_SQL = "SELECT * FROM renewable_energy_consumption"


def make_all_state_graphs():
    '''
    Generates 2017 graphs for all states, including (1) histograms of energy
    by source for all energy sources, and (2) for renewable sources.
    '''
    conn = sqlite3.connect('db.sqlite3')

    tot_cons_df = pd.read_sql_query(TOTAL_SQL, conn)
    tot_cons_df.replace(',', '', regex=True, inplace=True)
    tot_cons_df.iloc[:, 1:] = tot_cons_df.iloc[:, 1:].apply(
        pd.to_numeric, errors='coerce')
    tot_cons_df = tot_cons_df[['state', 'nuclear', 'petroleum',
                               'natural_gas', 'coal', 'renewable']]

    renew_cons_df = pd.read_sql_query(RENEW_SQL, conn)
    renew_cons_df.replace(',', '', regex=True, inplace=True)
    renew_cons_df.iloc[:, 1:] = renew_cons_df.iloc[:, 1:].apply(
        pd.to_numeric, errors='coerce')

    for st in [state for state in tot_cons_df['state']]:
        state_tot_cons, state_renew_cons = filter_to_one_state(
            st, tot_cons_df, renew_cons_df)
        make_state_graph(st, state_tot_cons, state_renew_cons)


def filter_to_one_state(state, tot_cons_df, renew_cons_df):
    '''
    Filters dataset to one state.

    Inputs:
        - state (string): name of state
        - tot_cons_df: dataframe containing total energy consumption data
        - renew_cons_df: dataframe containing renewable energy consumption data

    Output:
        - state_tot_df: total energy data for select state
        - state_renew_df: renewable energy data for select state
    '''
    state_tot_df = tot_cons_df[tot_cons_df['state'] == state]
    state_tot_df = state_tot_df.melt(id_vars='state')\
                            .rename(columns=str.title)

    state_renew_df = renew_cons_df[tot_cons_df['state'] == state]
    state_renew_df = state_renew_df.melt(id_vars='state')\
                            .rename(columns=str.title)

    return state_tot_df, state_renew_df


def make_state_graph(state, state_tot_cons, state_renew_cons):
    '''
    Generates state histograms.

    Inputs:
        - state (string): name of state
        - state_tot_cons: dataframe containing total energy consumption data for state
        - state_renew_cons: dataframe containing total energy consumption data for state
    Outputs:
        - histograms for each state
    '''
    plt1, ax = plt.subplots(figsize=(14, 10))

    plt.subplot(2, 1, 1)
    sns.barplot(x="Variable", y="Value", data=state_tot_cons, alpha=0.5,
                palette=["#e5ae38", "#30a2da", "#fc4f30", "#8b8b8b", "#28B463"])
    plt.xlabel('')
    plt.ylabel('All Consumption (Trillion Btu)')
    plt.title("Energy Consumption by Source (2017): {}".format(state),
              fontsize=25, fontweight="bold", y=1.05)

    plt.subplot(2, 1, 2)
    sns.barplot(x="Variable", y="Value", data=state_renew_cons,
                alpha=0.5, color="#28B463")
    plt.xlabel('')
    plt.ylabel('Renewable Consumption (Trillion Btu)')

    plt1.savefig('static/graphs/2017_{}.png'.format(state))
    plt.close()

if __name__ == "__main__":
    make_all_state_graphs()
