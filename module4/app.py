# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 12:31:10 2019

@author: Iden
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Gather data
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?')

soql_man = (soql_url + \
            '$select=spc_common,count(tree_id),health,steward,boroname' +\
            '&$where=boroname=\'Manhattan\'' +\
            '&$group=spc_common,health,steward,boroname').replace(' ', '%20')

soql_queens = (soql_url + \
            '$select=spc_common,count(tree_id),health,steward,boroname' +\
            '&$where=boroname=\'Queens\'' +\
            '&$group=spc_common,health,steward,boroname').replace(' ', '%20')

soql_brook = (soql_url + \
            '$select=spc_common,count(tree_id),health,steward,boroname' +\
            '&$where=boroname=\'Brooklyn\'' +\
            '&$group=spc_common,health,steward,boroname').replace(' ', '%20')

soql_bronx = (soql_url + \
            '$select=spc_common,count(tree_id),health,steward,boroname' +\
            '&$where=boroname=\'Bronx\'' +\
            '&$group=spc_common,health,steward,boroname').replace(' ', '%20')

soql_si = (soql_url + \
            '$select=spc_common,count(tree_id),health,steward,boroname' +\
            '&$where=boroname=\'Staten Island\'' +\
            '&$group=spc_common,health,steward,boroname').replace(' ', '%20')

# Read to data frames
man = pd.read_json(soql_man)
queens = pd.read_json(soql_queens)
brook = pd.read_json(soql_brook)
bronx = pd.read_json(soql_bronx)
si = pd.read_json(soql_si)

# Concat into one big data frame
frames = [man, queens, brook, bronx, si]
nyc = pd.concat(frames)

# Declare function for later use
def clean_up(df, s):
    foo = df.loc[df['steward'] == s]
    l = len(foo)
    g = 0
    f = 0
    p = 0
    
    if l == 3:
        g = foo.loc[foo['health'] == 'Good', 'count_tree_id'].iloc[0]
        f = foo.loc[foo['health'] == 'Fair', 'count_tree_id'].iloc[0]
        p = foo.loc[foo['health'] == 'Poor', 'count_tree_id'].iloc[0]
    else:
        for i in range(0, len(foo)):
            if foo['health'].iloc[i] == "Good":
                g = foo.loc[foo['health'] == 'Good', 'count_tree_id'].iloc[0]
            elif foo['health'].iloc[i] == "Fair":
                f = foo.loc[foo['health'] == "Fair", 'count_tree_id'].iloc[0]
            else:
                p = foo.loc[foo['health'] == "Poor", 'count_tree_id'].iloc[0]
        
    return([g, f, p])

# Get dropdown indicators
boro_ind = nyc['boroname'].unique()
tree_ind = nyc['spc_common'].unique()

app.layout = html.Div([
        html.Div([
                dcc.Dropdown(
                        id = 'borough',
                        options = [{'label':i, 'value':i} for i in boro_ind],
                        value = 'Manhattan'
                        ),
                dcc.Dropdown(
                        id = 'tree',
                        options = [{'label':i, 'value':i} for i in tree_ind],
                        value = 'ash'
                        )
                ]),
                
        dcc.Graph(id = 'indicator-graphic')
])
                
@app.callback(
        Output('indicator-graphic', 'figure'),
        [Input('borough', 'value'),
         Input('tree', 'value')])
def update_graph(borough_name, tree_name):
    dff = nyc.loc[np.logical_and(nyc.boroname == borough_name,
                                 nyc.spc_common == tree_name)]
    
    values = clean_up(dff, '3or4')
    trace1 = go.Bar(
            x = ['Good', 'Fair', 'Poor'],
            y = values,
            name = '3 or 4 Stewards'
            )
    
    values = clean_up(dff, '1or2')
    trace2 = go.Bar(
            x = ['Good', 'Fair', 'Poor'],
            y = values,
            name = '1 or 2 Stewards'
            )
    
    values = clean_up(dff, 'None')
    trace3 = go.Bar(
            x = ['Good', 'Fair', 'Poor'],
            y = values,
            name = 'No Stewards'
            )

    return{
            'data': [trace1, trace2, trace3],
            'layout': go.Layout(
                        xaxis = {'title': 'Health'},
                        yaxis = {'title': 'Tree Count'},
                        barmode = 'stack'
                        )
            }


if __name__ == '__main__':
    app.run_server(debug=True)