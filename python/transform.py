import pandas as pd


def process_data(df):

    # Add Cumulative Score
    df['Cummulative Score'] = df[['Participant', 'Score']].groupby('Participant').cumsum()

    # Split into multiple dataframes
    df_prev = df[df['Tag'] == 'P']  # Previous ranking
    df_latest = df[df['Tag'] == 'L']  # Latest ranking

    # Sort previous ranking
    prev = df_prev.sort_values(by=['Cummulative Score'], axis=0, ascending=False)
    # Sort current race scores
    curr = df_latest.sort_values(by=['Score'], axis=0, ascending=False)

    # Get the name for the current race
    race = curr["Grand Prix"].values[0]
    race_bold = '<b>' + race + ' Result</b>'

    # Sort latest ranking
    latest = df_latest.sort_values(by=['Cummulative Score'], axis=0, ascending=False)

    # Work out table movements
    latest['latest_pos'] = latest.reset_index().index + 1
    prev['prev_pos'] = latest.reset_index().index + 1

    # Attach previous_pos to latest dataframe
    latest = pd.merge(latest, prev[['Participant', 'prev_pos']], left_on='Participant', right_on='Participant', how='left')

    # Determine table movements and specify colors
    latest['movement'] = latest.apply(lambda x: '#00CC96' if x['latest_pos'] < x['prev_pos'] else
    '#FC6955' if x['latest_pos'] > x['prev_pos'] else
    '#ffffff', axis=1)

    return prev, curr, latest, race, race_bold
