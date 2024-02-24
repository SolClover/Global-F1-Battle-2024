# Import libraries

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Other utilities
import sys
import os
import getpass

# Assign main directory to a variable
main_dir=os.path.dirname(sys.path[0])
#print(main_dir)

# GitHub Access Token
#print('GitHub Access Token: ')
#gitpsw = getpass.getpass()

# Ingest data
#race='23 - Abu Dhabi'

#race_bold='<b>'+race+' Result</b>'
#race_bold
#race='22 - Abu Dhabi'

print(main_dir)


###### Step 2 - Create a graph
# Ingest
df = pd.read_csv(main_dir+"/data/League_results.csv", encoding='utf-8', parse_dates=['Date'])

# Transpose
df=df.melt(id_vars=['Date', 'Grand Prix', 'Tag']).rename(columns={'variable' : 'Participant', 'value' : 'Score'})

# Drop races that have not happened yet
df=df.dropna(axis=0, how='any')

# Add Cumulative Score
df['Cummulative Score']=df[['Participant', 'Score']].groupby('Participant').cumsum()

# Show DataFrame
#df

# ------------------------------
# ---- Split into multiple -----

# Previous ranking
df_prev=df[df['Tag']=='P']

# Latest ranking
df_latest=df[df['Tag']=='L']

# Setup a list for position numbers
pos=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

# Sort previous ranking
prev=df_prev.sort_values(by=['Cummulative Score'], axis=0, ascending=False)
#prev=df_prev.copy()

# Sort current race scores
curr=df_latest.sort_values(by=['Score'], axis=0, ascending=False)

# Get the name for the current race
race = curr["Grand Prix"].values[0]
race_bold='<b>'+race+' Result</b>'
print(race_bold)

# Sort latest ranking
latest=df_latest.sort_values(by=['Cummulative Score'], axis=0, ascending=False)

# Work out table movements
latest['latest_pos']= latest.reset_index().index+1
prev['prev_pos']= latest.reset_index().index+1

# Attach previous_pos to latest dataframe
latest=pd.merge(latest, prev[['Participant', 'prev_pos']], left_on='Participant', right_on='Participant', how='left')

# Determine table movements and setup the colors
latest['movement']=latest.apply(lambda x: '#00CC96' if x['latest_pos']<x['prev_pos'] else
                                          '#FC6955'   if x['latest_pos']>x['prev_pos'] else
                                          '#ffffff', axis=1)

###### Step 3 - Create a graph
# Initialize figure with subplots
fig = make_subplots(
    rows=2, cols=3,
    column_widths=[0.33, 0.33, 0.33],
    horizontal_spacing=0.02,
    vertical_spacing=0.12,
    subplot_titles=(['', '<b>Previous Total</b>', race_bold, '<b>Latest Total</b>']),
    row_heights=[0.5, 0.5],
    specs=[[{"type": "scatter", "colspan": 3}, None, None],
           [{"type": "table"}, {"type": "table"}, {"type": "table"}]])

# ------ Totals Graph ------
colors = px.colors.qualitative.Plotly + px.colors.qualitative.Light24
i = 0
for item in latest['Participant']:
    fig.add_trace(
        go.Scatter(name=item,
                   x=df[df['Participant'] == item]["Grand Prix"],
                   y=df[df['Participant'] == item]["Cummulative Score"],
                   showlegend=True, mode="lines",
                   marker={"color": colors[i]}
                   ), row=1, col=1)
    i += 1
# ---------------------------

# ---- Add table traces ----
font_header = 12
font_text = 11

fig.add_trace(
    go.Table(
        columnwidth=[0.15, 0.7, 0.15],
        header=dict(values=['Place', 'Participant', 'Score'],
                    fill_color='#6600cc', align='center', height=30,
                    font=dict(family="Arial", size=font_header, color="white")),
        cells=dict(values=[pos, prev['Participant'], prev['Cummulative Score']],
                   fill_color='#ffffff', line_color='lightgrey', align='center', height=30,
                   font=dict(family="Arial", size=font_text, color="black"))),
    row=2, col=1
)

fig.add_trace(
    go.Table(
        columnwidth=[0.15, 0.7, 0.15],
        header=dict(values=['Place', 'Participant', 'Score'],
                    fill_color='#6600cc', align='center', height=30,
                    font=dict(family="Arial", size=font_header, color="white")),
        cells=dict(values=[pos, curr['Participant'], curr['Score']],
                   fill_color='#ffffff', line_color='lightgrey', align='center', height=30,
                   font=dict(family="Arial", size=font_text, color="black"))),
    row=2, col=2
)

fig.add_trace(
    go.Table(
        columnwidth=[0.15, 0.7, 0.15],
        # header=dict(values=['Place', 'Participant &#127942;', 'Score'],
        header=dict(values=['Place', 'Participant', 'Score'],
                    fill_color='#6600cc', align='center', height=30,  # line_color='lightgrey',
                    font=dict(family="Arial", size=font_header, color="white")),
        cells=dict(values=[pos, latest['Participant'], latest['Cummulative Score']],
                   fill_color=[latest['movement']], line_color='lightgrey', align='center', height=30,
                   font=dict(family="Arial", size=font_text, color="black"))),
    row=2, col=3
)
# ------------------------

# ---- Update Layout ----
font_size = 11

fig.update_layout(

    autosize=True,
    # width=1000,
    height=1500,

    paper_bgcolor='#161f39',  # Sets the background color for the whole chart
    plot_bgcolor='#161f39',

    font=dict(family="Arial", size=font_size, color="white"),
    title=dict(
        text='<b>Global F1 Battle 2024 League</b> (After ' + race + ')',
        x=0.5,
        y=0.98,
        font=dict(family='Arial', size=18, color='#ffffff')),

    xaxis=dict(
        fixedrange=True,
        showgrid=False,  # Sets whether to show the grid in the graph
        zeroline=True,  # Sets whether to show the main line (0 line) in the chart
        showticklabels=True,  # Sets whether to show the numbers / labels on tick marks
        tickmode='linear',  # Shows every singe tick label
        tickangle=-45,  # Rotation of tick labels
        tickfont=dict(  # Sets tick options
            family='Arial',  # Font family
            size=font_size,  # Font size
            color='#ffffff'  # Font color
        ),
    ),

    yaxis=dict(
        fixedrange=True,
        showgrid=False,  # Sets whether to show the grid in the graph
        zeroline=True,  # Sets whether to show the main line (0 line) in the chart
        showticklabels=True,  # Sets whether to show the numbers / labels on tick marks
        # range=[-0.05, 13.5] # Sets the range for axis
    ),

    margin=dict(l=80, r=80, t=110, b=0),  # Set margins for chart area

    legend_orientation='h',  # Legend orientation vertical / horizontal
    legend=dict(  # Sets legend location within the paper area
        x=0,
        y=1.03,
        xanchor='left',
        font=dict(
            family='Arial',
            size=font_size,
            color='#ffffff'
        )
    ),
)

# fig.show()
fig.write_html(main_dir + '/index.html')
