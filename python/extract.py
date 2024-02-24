import pandas as pd
from python.config import MAIN_DIR


def load_data():
    # Ingest
    df = pd.read_csv(MAIN_DIR + "/data/League_results.csv", encoding='utf-8', parse_dates=['Date'])

    # Transpose
    df = df.melt(id_vars=['Date', 'Grand Prix', 'Tag']).rename(columns={'variable': 'Participant', 'value': 'Score'})

    # Drop races that have not happened yet
    df = df.dropna(axis=0, how='any')

    return df
