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
#import seaborn as sns; sns.set()

#------------------------------------------------------------------------------
# SETTINGS
#------------------------------------------------------------------------------

use_dark_theme = False
use_instrumental_monthly = False

#------------------------------------------------------------------------------
# METHODS
#------------------------------------------------------------------------------

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

#------------------------------------------------------------------------------
# LOAD: timeseries for each SSP
#------------------------------------------------------------------------------

if use_instrumental_monthly == False:

	ssp119 = pd.read_csv( 'OUT/ncc_data_baseline_1851_1900_SSP119.csv' ).reset_index(drop=True)
	ssp126 = pd.read_csv( 'OUT/ncc_data_baseline_1851_1900_SSP126.csv' ).reset_index(drop=True)
	ssp245 = pd.read_csv( 'OUT/ncc_data_baseline_1851_1900_SSP245.csv' ).reset_index(drop=True)
	ssp370 = pd.read_csv( 'OUT/ncc_data_baseline_1851_1900_SSP370.csv' ).reset_index(drop=True)
	ssp585 = pd.read_csv( 'OUT/ncc_data_baseline_1851_1900_SSP585.csv' ).reset_index(drop=True)

else:
	
	ssp119 = pd.read_csv( 'OUT/ncc_data_baseline_1851_1900_SSP119_monthly.csv' ).reset_index(drop=True)
	ssp126 = pd.read_csv( 'OUT/ncc_data_baseline_1851_1900_SSP126_monthly.csv' ).reset_index(drop=True)
	ssp245 = pd.read_csv( 'OUT/ncc_data_baseline_1851_1900_SSP245_monthly.csv' ).reset_index(drop=True)
	ssp370 = pd.read_csv( 'OUT/ncc_data_baseline_1851_1900_SSP370_monthly.csv' ).reset_index(drop=True)
	ssp585 = pd.read_csv( 'OUT/ncc_data_baseline_1851_1900_SSP585_monthly.csv' ).reset_index(drop=True)

#------------------------------------------------------------------------------
# APP: design
#------------------------------------------------------------------------------
'''
https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/
'''
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = [dbc.themes.DARKLY]
external_stylesheets = [dbc.themes.SPACELAB]
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
server = app.server
#server = Flask(__name__)

app.layout = html.Div([
        
    html.Br(),
    html.H3("Global Temperature Anomaly Timeseries: 65.5 Myr BCE to 2200 CE"),                                            
    html.Br(),
    html.Div([
        
        dbc.Row([

            dbc.Col(html.Div([                    
            ]), 
            width={'size':1}, 
            ),                   


            dbc.Col(html.Div([                    
                html.H6("Choose your Future 2023-2200 CE:"),
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
                html.H6("Choose your start Epoch:"),
                dcc.RadioItems(
                    id="epoch",
                    options=["Age of Mammals", "Interglacials", "Holocene", "Common Era", "Instrumental"],
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

#    html.Div([
#        html.H6(['Michael Taylor, CRU/UEA ', html.A('@climatetinker', href='https://twitter.com/climatetinker'), '' ]), ], style={'marginLeft': 1400, 'marginTop': 20, 'marginBottom': 20}
#	),

    html.Div([
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H2([html.A('Climate Mural for our Times', href='https://crudata.uea.ac.uk/cru/climate-mural/',style={'color':'white', 'text-decoration':'bold'})]),
   ],style={'background-image': 'url(/assets/mural-full.jpg)',
#    ],style={'background-image': 'url(/assets/stripes-cenozoic.jpg)',
           'background-size': '100%',
#           'background-size': 'cover',
           'position': 'fixed',
           'width': '100%',
           'height': '100%',           
           'textAlign': 'center',
           }),

])    
                                   
#],    
#style={'background-image': 'url(/assets/mural-full.jpg)',
#       'background-size': '100%',
#       'background-size': 'cover',
#       'position': 'fixed',
#           'width': '100%',
#           'height': '100%',           
#           }),
#)

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
        df = df.copy()        
    elif value_epoch == "Interglacials":
        df = df[ (df.Year >= -500000) ]
    elif value_epoch == "Holocene":
        df = df[ (df.Year > (2023-11700)) ]
    elif value_epoch == "Common Era":
        df = df[ (df.Year > 0) ]
    elif value_epoch == "Instrumental":
#        df = df[ (df.Year >= 1850) ]
        df = df[ (df.Year >= 1781) ]
        
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
    
    y_climate_analogue = np.ones(len(y)) * y[x<2024][-1]               
            
    p_025 = df['p_025'].values
    p_975 = df['p_975'].values				
                                   
    fig = go.Figure([
        
#        go.Scatter(x=x, y=limits[1]*np.ones_like(x), opacity=0, line_width=0, showlegend=False),
#        go.Scatter(x=x_mod, y=y1, fill="tozeroy", opacity=0.5, connectgaps=False, mode='lines', line_color='indigo'),
#        go.Scatter(x=x, y=limits[0]*np.ones_like(x), opacity=0, line_width=0, showlegend=False),
#        go.Scatter(x=x_mod, y=y2, fill="tozeroy", opacity=0.5, connectgaps=False, mode='lines', line_color='red'),
#        go.Scatter(x=x, y=limits[0]*np.ones_like(x), opacity=0, line_width=0, showlegend=False),
#        go.Scatter(x=x_mod, y=y3, fill="tozeroy", opacity=0.5, connectgaps=False, mode='lines', line_color='orange'),
#        go.Scatter(x=x, y=limits[0]*np.ones_like(x), opacity=0, line_width=0, showlegend=False),
#        go.Scatter(x=x_mod, y=y4, fill="tozeroy", opacity=0.5, connectgaps=False, mode='lines', line_color='blue'),
	
        go.Line(x=x, y=p_025, fill="none", opacity=0.1, connectgaps=False, mode='lines', line=dict(width=0.5), line_color='lightgrey', showlegend=False),
        go.Line(x=x, y=p_975, fill="tonexty", opacity=0.1, connectgaps=False, mode='lines', line=dict(width=0.5), line_color='lightgrey', name='95% c.i.'),
        go.Line(x=x_mod, y=y1, fill="none", opacity=1, connectgaps=False, mode='lines', line=dict(width=3), line_color='indigo', name='> 2°C'),
        go.Line(x=x_mod, y=y2, fill="none", opacity=1, connectgaps=False, mode='lines', line=dict(width=3), line_color='red', name='1.5 - 2°C'),
        go.Line(x=x_mod, y=y3, fill="none", opacity=1, connectgaps=False, mode='lines', line=dict(width=3), line_color='orange', name='0 - 1.5°C'),
        go.Line(x=x_mod, y=y4, fill="none", opacity=1, connectgaps=False, mode='lines', line=dict(width=3), line_color='blue', name='< 0°C'),
        go.Line(x=x, y=y_climate_analogue, fill="none", opacity=1, connectgaps=False, mode='lines', line=dict(width=3), line_color='black', line_dash='dash', name='Climate Analogue(s)'),

    ])
       
#    fig = make_subplots(2, 1, shared_xaxes=True)
#    fig.add_trace( go.Scatter(x=df.Year, y=df.Global), row=1, col=1 )
#    fig.add_trace( go.Scatter(x=df.Year, y=df.Global/2), row=2, col=1 )
#    fig.update_xaxes(row=1, col=1, rangeslider_visible=False)
#    fig.update_xaxes(row=2, col=1, rangeslider_visible=True)
   
    #fig.update_layout(xaxis = dict(rangeslider=dict(visible=True)))
    #fig.update_layout(autosize = True, height=600, width=2000)
    #fig.update_layout(autosize = True)
    
    if use_dark_theme == True:
        fig.update_layout(xaxis = dict(tickfont = dict(size=20), color='white'))
        fig.update_layout(yaxis = dict(tickfont = dict(size=20), color='white'))        	
        fig.update_layout(legend = dict(orientation="h", x=0.05, y=1.15, font = dict(size = 16, color = "white")))            
        fig.update_layout(paper_bgcolor = 'black', plot_bgcolor = 'black' )
#        fig.update_xaxes(title='Year', title_font=dict(size=20), title_font_color='white')    
        fig.update_yaxes(title='Anomaly (from 1851-1900), °C', title_font=dict(size=20), title_font_color="white")    
    else:
        fig.update_layout(xaxis = dict(tickfont = dict(size=20), color='black'))
        fig.update_layout(yaxis = dict(tickfont = dict(size=20), color='black'))
        fig.update_layout(legend = dict(orientation="h", x=0.0, y=-0.15, font = dict(size = 16, color = "black")))            
        fig.update_layout(paper_bgcolor = 'ghostwhite', plot_bgcolor = 'white' )
#        fig.update_xaxes(title='Year', title_font=dict(size=20), title_font_color='black')    
        fig.update_yaxes(title='Anomaly (from 1851-1900), °C', title_font=dict(size=20), title_font_color='black')    

#    fig.update_xaxes(showgrid=False, zeroline = False)
#    fig.update_yaxes(showgrid=False, zeroline = False)
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=50),paper_bgcolor="ghostwhite")
    fig.add_annotation(dict(font=dict(color='black',size=16), x=0.75, y=-0.25, showarrow=False, 
		text="Michael Taylor, CRU/UEA " + "<a href='https://twitter.com/climatetinker' target='_blank'>" + "@climatetinker" + "</a>" + " --- 7 Oct 2023", textangle=0, xanchor='left', xref="paper", yref="paper"))
    fig.add_annotation(dict(font=dict(color='black',size=16), x=0.0, y=1.15, showarrow=False, 
		text = value_epoch + "-2200 CE (" + value_ssp + ")", textangle=0, xanchor='left', xref="paper", yref="paper"))
                                                                                                              
    return fig

#------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
#------------------------------------------------------------------------------


    
