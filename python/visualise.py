import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from python.config import POSITION


def create_charts(df, prev, curr, latest, race, race_bold):
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
            cells=dict(values=[POSITION, prev['Participant'], prev['Cummulative Score']],
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
            cells=dict(values=[POSITION, curr['Participant'], curr['Score']],
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
            cells=dict(values=[POSITION, latest['Participant'], latest['Cummulative Score']],
                       fill_color=[latest['movement']], line_color='lightgrey', align='center', height=30,
                       font=dict(family="Arial", size=font_text, color="black"))),
        row=2, col=3
    )

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
            text='<b>Global F1 Battle 2025 League</b> (After ' + race + ')',
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

    return fig
