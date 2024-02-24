from python.config import MAIN_DIR
from python.extract import load_data
from python.transform import process_data
from python.visualise import create_charts

# Load data
df = load_data()

# Prepare data
prev, curr, latest, race, race_bold = process_data(df)

# Visualise outputs
fig = create_charts(df, prev, curr, latest, race, race_bold)

# Update index.html
fig.write_html(MAIN_DIR + '/index.html')
