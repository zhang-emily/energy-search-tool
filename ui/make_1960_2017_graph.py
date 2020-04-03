'''
Using data in './data/energy_consumption_by_source_1960_2017.csv',
plot bar graphs showing the composition of energy sources over time (1960-2017)
for each state. Store graphs in './static/graphs' to be displayed in final UI.
'''

import pandas as pd
import seaborn as sns
import matplotlib.style as style
import matplotlib.pyplot as plt
style.use('fivethirtyeight')


def import_data():
    '''
    Imports total energy data (1960-2017) from csv.

    Outputs:
        - coal, ng, petroleum, nuclear, and all_renew dataframes
    '''
    all_energy = pd.read_csv('data/energy_consumption_by_source_1960_2017.csv',
                             delimiter='|')

    coal = all_energy[['Year', 'State', 'Consumption']].loc[
        all_energy['Source'] == 'Coal'].rename(
        columns={'Consumption': 'Coal'})
    
    ng = all_energy[['Year', 'State', 'Consumption']].loc[
        all_energy['Source'] == 'Natural Gas'].rename(
        columns={'Consumption': 'Natural Gas'})

    petroleum = all_energy[['Year', 'State', 'Consumption']].loc[
        all_energy['Source'] == 'Petroleum'].rename(
        columns={'Consumption': 'Petroleum'})

    nuclear = all_energy[['Year', 'State', 'Consumption']].loc[
        all_energy['Source'] == 'Nuclear'].rename(
        columns={'Consumption': 'Nuclear'})

    all_renew = all_energy[['Year', 'State', 'Consumption']].loc[
        all_energy['Source'] == 'Renewable Energy'].rename(
        columns={'Consumption': 'Renewable Energy'})

    return coal, ng, petroleum, nuclear, all_renew


def merge_data(coal, ng, petroleum, nuclear, all_renew):
    '''
    Combines dataframes for energy sources into one dataframe.

    Inputs:
        - coal: coal dataframe
        - ng: natural gas dataframe
        - petroleum: petroleum dataframe
        - nuclear: nuclear dataframe
        - all_renew: renewable energy dataframe
    Outputs:
        - df: combined dataframe with all energy sources
    '''
    df = pd.merge(coal, ng, on=['Year', 'State'])
    df = pd.merge(df, petroleum, on=['Year', 'State'])
    df = pd.merge(df, nuclear, on=['Year', 'State'])
    df = pd.merge(df, all_renew, on=['Year', 'State'])

    return df


def format_for_graph(state, df):
    '''
    Converts dataframe to array for stackplot.

    Inputs:
        - state (string): name of state
        - df: dataframe containing energy data by state
    Outputs:
        - state_df: array for stackplot
    '''
    df.iloc[:, 2:] = df.iloc[:, 2:].divide(df.iloc[:, 2:].sum(axis=1), axis=0)
    state_df = df[df['State'] == state]

    return state_df


def create_graph(state, state_df):
    '''
    Generates stackplot for given state.

    Inputs:
        - state (string): name of state
        - state_df: array of state energy data
    Outputs:
        - stackplot of energy sources for given state, from 1960-2017
    '''
    palette = ["#e5ae38", "#30a2da", "#fc4f30", "#8b8b8b", "#28B463"]
    #palette = ['green', 'blue', 'red', 'black', 'orange']
    plt1, ax = plt.subplots(figsize=(11, 6))

    plt.stackplot(state_df['Year'], state_df[['Nuclear', 'Petroleum',
        'Natural Gas', 'Coal', 'Renewable Energy']].to_numpy().T,
        alpha=0.5, colors=palette, labels=['Nuclear', 'Petroleum',
        'Natural Gas', 'Coal', 'Renewable Energy'])

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='center left', fontsize='x-small')

    ax.set_title('Energy Consumption by Source (1960-2017): {}'.format(state),
        fontsize=15, fontweight="bold", y=1.05)

    ax.margins(0, 0)

    plt1.savefig('static/graphs/full_yoy_{}.png'.format(state))
    plt.close()


if __name__ == "__main__":
    '''
    Generates graphs for all states.
    '''
    coal, ng, petroleum, nuclear, all_renew = import_data()
    df = merge_data(coal, ng, petroleum, nuclear, all_renew)
    for state in list(df['State'].unique()):
        state_df = format_for_graph(state, df)
        create_graph(state, state_df)
