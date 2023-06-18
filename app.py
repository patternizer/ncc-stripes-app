#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 16:33:41 2023

@author: cqz20mbu
"""

from flask import Flask
import dash
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
from plotly.subplots import make_subplots

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import image

#------------------------------------------------------------------------------

ssp119 = pd.read_csv( 'OUT/ncc_data_baseline_1961_1990_SSP119.csv' ).reset_index(drop=True)
ssp126 = pd.read_csv( 'OUT/ncc_data_baseline_1961_1990_SSP126.csv' ).reset_index(drop=True)
ssp245 = pd.read_csv( 'OUT/ncc_data_baseline_1961_1990_SSP245.csv' ).reset_index(drop=True)
ssp370 = pd.read_csv( 'OUT/ncc_data_baseline_1961_1990_SSP370.csv' ).reset_index(drop=True)
ssp585 = pd.read_csv( 'OUT/ncc_data_baseline_1961_1990_SSP585.csv' ).reset_index(drop=True)

def set_threshold(x,y,threshold):
    xv=[]
    yv=[]
    for i in range(len(y)-1):
    	xv += [x[i]]
    	yv += [y[i]]
    	if y[i] > threshold > y[i+1] or y[i] < threshold < y[i+1]:
    		Xi = x[i] + ((threshold-y[i])*(x[i+1]-x[i]) / (y[i+1]-y[i]))
    		xv += [Xi]
    		yv += [threshold]
    xv += [x[-1]]
    yv += [y[-1]]    
    xv = np.array(xv)
    yv = np.array(yv)

    return xv,yv

#app = Dash(__name__)

#https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.DARKLY]
#external_stylesheets = [dbc.themes.SPACELAB]
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div([

    html.H3("Global Temperature Anomaly Timeseries: 65.5 Myr BCE to 2200 CE"),                                            

    html.Br(),
    html.Div([
        
        dbc.Row([

            dbc.Col(html.Div([                    
            ]), 
            width={'size':1}, 
            ),                   


            dbc.Col(html.Div([                    
                html.H6("Choose your Future 2023-2200 CE"),
                dcc.RadioItems(
                    id="ssp",
                    options=["SSP1-1.9", "SSP1-2.6", "SSP2-4.5", "SSP3-7.0", "SSP5-8.5"],
                    value="SSP3-7.0",
                    inline=True,   
                    labelStyle = {'display': 'flex'},
                ),
            ]), 
            width={'size':3}, 
            ),                   
                       
            dbc.Col(html.Div([
                html.H6("Choose your Epoch"),
                dcc.RadioItems(
                    id="epoch",
                    options=["Age of Mammals", "Interglacials", "Holocene", "Instrumental", "Future"],
                    value="Age of Mammals",
                    inline=True,
                    labelStyle = {'display': 'flex'},
                ),
            ]), 
            width={'size':2}, 
            ),            
        ]),

    ]),
        
    html.Br(),
    dcc.Loading(dcc.Graph(id="graph"), type="cube"),

    html.Div([
        html.H6(['Michael Taylor, CRU/UEA ', html.A('@climatetinker', href='https://twitter.com/climatetinker'), '' ]),                
    ], style={'marginLeft': 1400, 'marginTop': 20})

])

@app.callback(
    Output("graph", "figure"),
    Input("ssp", "value"),
    Input("epoch", "value"),
)
def update_graph(value_ssp,value_epoch):

    df = ssp370
    if value_ssp == "SSP1-1.9":
        df = ssp119
    elif value_ssp == "SSP1-2.6":
        df = ssp126
    elif value_ssp == "SSP2-4.5":
        df = ssp245
    elif value_ssp == "SSP3-7.0":
        df = ssp370
    elif value_ssp == "SSP5-8.5":
        df = ssp585
        
    if value_epoch == "Age of Mammals":
        df = df[ df.Year <= 2023 ]        
    elif value_epoch == "Interglacials":
        df = df[ (df.Year >= -500000) & (df.Year <= (2023-11700))]
    elif value_epoch == "Holocene":
        df = df[ (df.Year > (2023-11700)) & (df.Year <= 2023)]
    elif value_epoch == "Instrumental":
        df = df[ (df.Year >= 1850) & (df.Year <= 2023)]
    elif value_epoch == "Future":
        df = df[df.Year >= 2023]
        
    df = df.reset_index(drop=True)
    x = df['Year'].values
    y = df['Global'].values
        
    x_mod = x.copy()
    y_mod = y.copy()
    limits = [0, 1.5, 2]
    for l in limits:
        x_mod, y_mod = set_threshold(x_mod, y_mod, l)    
    y1, y2, y3, y4 = [y_mod.copy() for i in range(4)]
    y1[y1 < limits[2]] = np.nan                         # i.e. plot > 2
    y2[(y2 < limits[1]) | (y2 > limits[2])] = np.nan    # i.e. plot 1.5 to 2
    y3[(y3 < limits[0]) | (y3 > limits[1])] = np.nan    # i.e. plot 0 to 1.5
    y4[y4 > limits[0]] = np.nan                         # i.e. plot < 0
                
    fig = go.Figure([
        
#        go.Scatter(x=x, y=limits[1]*np.ones_like(x), opacity=0, line_width=0, showlegend=False),
#        go.Scatter(x=x_mod, y=y1, fill="tozeroy", opacity=0.5, connectgaps=True, mode='lines', line_color='indigo'),
#        go.Scatter(x=x, y=limits[0]*np.ones_like(x), opacity=0, line_width=0, showlegend=False),
#        go.Scatter(x=x_mod, y=y2, fill="tozeroy", opacity=0.5, connectgaps=True, mode='lines', line_color='red'),
#        go.Scatter(x=x, y=limits[0]*np.ones_like(x), opacity=0, line_width=0, showlegend=False),
#        go.Scatter(x=x_mod, y=y3, fill="tozeroy", opacity=0.5, connectgaps=True, mode='lines', line_color='orange'),
#        go.Scatter(x=x, y=limits[0]*np.ones_like(x), opacity=0, line_width=0, showlegend=False),
#        go.Scatter(x=x_mod, y=y4, fill="tozeroy", opacity=0.5, connectgaps=True, mode='lines', line_color='blue'),

#        go.Line(x=x_mod, y=y1, fill="none", opacity=0.5, marker = dict(size = 5, color = 'indigo', symbol = 'circle-open', line=dict(width=2)), connectgaps=False, mode='lines+markers', line_color='indigo', name='> 2°C'),
        go.Line(x=x_mod, y=y1, fill="none", opacity=1, connectgaps=False, mode='lines', line=dict(width=3), line_color='indigo', name='> 2°C'),
        go.Line(x=x_mod, y=y2, fill="none", opacity=1, connectgaps=False, mode='lines', line=dict(width=3), line_color='red', name='1.5-2°C'),
        go.Line(x=x_mod, y=y3, fill="none", opacity=1, connectgaps=False, mode='lines', line=dict(width=3), line_color='orange', name='0-1.5°C'),
        go.Line(x=x_mod, y=y4, fill="none", opacity=1, connectgaps=False, mode='lines', line=dict(width=3), line_color='blue', name='< 0°C'),

    ])
       
#    fig = make_subplots(2, 1, shared_xaxes=True)
#    fig.add_trace( go.Scatter(x=df.Year, y=df.Global), row=1, col=1 )
#    fig.add_trace( go.Scatter(x=df.Year, y=df.Global/2), row=2, col=1 )
#    fig.update_xaxes(row=1, col=1, rangeslider_visible=False)
#    fig.update_xaxes(row=2, col=1, rangeslider_visible=True)
   
    fig.update_layout(xaxis = dict(rangeslider=dict(visible=False)))
    fig.update_layout(xaxis = dict(tickfont = dict(size=20), color='white'))
    fig.update_layout(yaxis = dict(tickfont = dict(size=20), color='white'))
#    fig.update_layout(autosize = True, height=600, width=2000)
    fig.update_layout(autosize = True)
    fig.update_layout(legend = dict(orientation="h", x=0.4, y=1, font = dict(size = 16, color = "white")))            
    fig.update_layout(paper_bgcolor = 'black', plot_bgcolor = 'black' )
    fig.update_yaxes(title='Anomaly (from 1961-1990), °C', title_font=dict(size=20), title_font_color="white")    
    fig.update_xaxes(showgrid=False, zeroline = False)
    fig.update_yaxes(showgrid=False, zeroline = False)
    fig.update_layout(margin=dict(l=50, r=50, t=50, b=50))

    return fig

#------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run_server(debug=True)

#------------------------------------------------------------------------------


    