# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 19:19:58 2023

@author: Dhr
"""

import pandas as pd
import plotly.express as px
import webbrowser

df = pd.read_excel("C:\\Work 2\\RS_stns_list.xlsx")

# Create an interactive scatter plot using plotly
fig = px.scatter_geo(df, lon='lon', lat='lat', title='Radiosonde Stations',
                     projection='natural earth', size_max=10, opacity=1,
                     hover_data={'name': True})  # Set hover_data to display station names on hover

# Set marker color to black
fig.update_traces(marker=dict(color='black'))

# Customize the layout
fig.update_geos(
    coastlinecolor='rgb(0,0,0)',
    landcolor='rgb(200, 238, 144)',
    lonaxis=dict(
        showgrid=True,
        gridwidth=1,
        range=[-180, 180],
        dtick=10,  # Adjust the interval between longitude lines
    ),
    lataxis=dict(
        showgrid=True,
        gridwidth=1,
        range=[-60, 60],
        dtick=10,  # Adjust the interval between latitude lines
    )
)


# Add a black line inside the globe along the equator
fig.update_layout(
    geo=dict(
        projection_scale=1,
        center=dict(lon=0, lat=0),
        lonaxis=dict(showgrid=True, gridcolor='black', gridwidth=1),
        lataxis=dict(showgrid=True, gridcolor='black', gridwidth=1),
        projection=dict(type="natural earth"),
    )
)


# Update layout to add labels to x-axis and y-axis
fig.update_layout(
    xaxis=dict(title='Longitude'),
    yaxis=dict(title='Latitude'),
    title=dict(text='RADIOSONDE STATIONS', x=0.5, y=0.95,font=dict(size=24))  # Title in the center
)

# Add interactivity for trend graph
def open_trend_graph(trace, points, selector):
    selected_station = df.iloc[points.point_inds[0]]
    station_name = selected_station['name']
    trend_graph_path = f"trend_graphs/{station_name}_trend.png"  # Replace with your actual path
    webbrowser.open(trend_graph_path)

# Save the interactive plot as an HTML file
fig.write_html("C:\\Work 2\\worldmap_interactive.html")

# Update the click event for the entire figure
fig.update_layout(clickmode='event+select')

# Define the click event callback
def on_click(trace, points, selector):
    if points.point_inds:
        open_trend_graph(trace, points, selector)

# Assign the callback to the entire figure
fig.for_each_trace(lambda trace: trace.on_click(on_click))

# Show the interactive plot in a web browser
fig.show()
