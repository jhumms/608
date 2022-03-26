''' In this module we’ll be looking at data from the New York City tree census:
https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh
This data is collected by volunteers across the city, and is meant to catalog information about every single tree in the city.
Build a dash app for a arborist studying the health of various tree species (as defined by the variable ‘spc_common’) across each borough (defined by the variable ‘borough’). This arborist would like to answer the following two questions for each species and in each borough:
What proportion of trees are in good, fair, or poor health according to the ‘health’ variable ?
Are stewards (steward activity measured by the ‘steward’ variable) having an impact on the health of trees? 


http://jhumms.pythonanywhere.com/ '''

import pandas as pd
import numpy as np

trees = pd.read_csv("https://data.cityofnewyork.us/resource/uvpi-gqnh.csv")
trees_q1 = trees[['spc_common','health','boroname','steward']]
trees_q1['spc_common'].fillna('Unknown',inplace = True)
trees_q1.dropna(inplace = True)

trees_q1["steward"] = trees_q1["steward"].replace("1or2", "1-2", regex=True)
trees_q1["steward"] = trees_q1["steward"].replace("3or4", "3-4", regex=True)
trees_q1["steward"] = trees_q1["steward"].replace("4orMor", "4+", regex=True)
trees_q1["steward"] = trees_q1["steward"].replace("None", "0", regex=True)
trees_q1["steward"] = trees_q1["steward"].replace(np.nan, "0", regex=True)





tree_options = set(trees_q1['spc_common'])



borough_options = set(trees_q1['boroname'])




import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output


app = dash.Dash()


app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Tree Health in NYC', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),
    
     html.H2(id = 'H2-1', children = 'What proportion of trees are in good, fair, or poor health according to the ‘health’ variable?', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),


    dcc.Dropdown( id = 'dropdown',
        options = [
            {'label':i, 'value':i} for i in tree_options],
        value = 'ginkgo'),
    
    dcc.Dropdown( id = 'dropdown2',
        options = [
            {'label':i, 'value':i} for i in borough_options],
        value = 'Queens'),
    
    
    dcc.Graph(id = 'bar_plot'),
    
    
    
    html.H2(id = 'H2-2', children = 'Are stewards (steward activity measured by the ‘steward’ variable) having an impact on the health of trees?', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),
    
    dcc.Graph(id = 'bar_plot2'),
    ])
    
    
@app.callback([Output(component_id='bar_plot', component_property= 'figure'),
              Output(component_id='bar_plot2', component_property= 'figure')],
              [Input(component_id='dropdown', component_property= 'value'),
                Input(component_id='dropdown2', component_property= 'value')])

def graph_update(dropdown_value, dropdown2_value):
        
    l = trees_q1.loc[(trees_q1['spc_common'] == '{}'.format(dropdown_value)) & ((trees_q1['boroname'] == '{}'.format(dropdown2_value)))]
    
    
    bar_plot = px.bar((l.groupby(['health'])['health'].count() / len(l) *100)) 
    
                    
    
    bar_plot.update_layout(title = print(dropdown2_value, " Treehealth" ),
                      xaxis_title = dropdown2_value,
                      yaxis_title = 'Percent Contribution'
                      )
    
    bar_plot2 = px.bar(l, x = 'steward', color = 'health') 
    
    bar_plot2.update_layout(title = print(dropdown2_value, " Treehealth" ),
                      xaxis_title = dropdown2_value,
                      yaxis_title = 'Percent Contribution'
                      )
    
    
    return[bar_plot,bar_plot2]  



if __name__ == '__main__': 
    app.run_server()

