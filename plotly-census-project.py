import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc,Input,Output,dash_table,Dash,html
import dash_bootstrap_components as dbc
import dash_bootstrap_templates as dbt

add_css = "https://cdn.jsdelivr.net/gh/AnnMariew/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__,external_stylesheets=[dbc.themes.DARKLY,add_css])

df = pd.read_csv(r"C:\Users\ASUS\Downloads\India.csv")

list_of_states = list(df["State"].unique())
list_of_states.insert(0,"Overall India")

dbt.load_figure_template("DARKLY")
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label="Map Analysis",id="tab1",children=[
            html.H3(id="title",style={"text-align":"center"}),
            dbc.Row([
                dbc.Col([
                    html.P("Select Any State From Below"),
                    dcc.Dropdown(id="select-state",
                                 options=list_of_states,
                                 value="Overall India",
                                 className="dbc"),
                    html.Br(),
                    html.P("Select Primary Attribute"),
                    dcc.Dropdown(id="select-primary",
                                 options=(df.select_dtypes(include="number").iloc[:,3:]).columns,
                                 value="Population",
                                 className="dbc"),
                    html.Br(),
                    html.P("Select Secondary Attribute"),
                    dcc.Dropdown(id="select-secondary",
                                 options=(df.select_dtypes(include="number").iloc[:,3:]).columns,
                                 value="Male",
                                 className="dbc")
                ],width=3),
                dbc.Col(children=[dcc.Graph(id="graph"),
                                  html.P("Color indicate Primay Attribute -  & - Size of marker indicate Secondary Attribute")],width=6)
            ])
        ],className="dbc"),
        dcc.Tab(label="Graph Analysis",id="tab2",children=[
            html.H3(id="title2",style={"text-align":"center"}),
            dbc.Row([
                dbc.Col([
                    html.P("Select Any State From Below"),
                    dcc.Dropdown(id="state",
                                 options=list_of_states,
                                 value="Overall India",
                                 className="dbc"),
                    html.Br(),
                    html.P("Select Primary Parameter"),
                    dcc.Dropdown(id="primary_attribute",
                                 options=(df.select_dtypes(include="number").iloc[:,3:]).columns,
                                 value="Population",
                                 className="dbc")
                ],width=3),
                dbc.Col(dcc.Graph(id="graph2"),width=6)
            ])
        ])
    ],className="dbc")
])

@app.callback(Output("title","children"),Output("graph","figure"),
              [Input("select-state","value"),Input("select-primary","value"),Input("select-secondary","value")])
def chose(state,primary,secondary):
    
    title = f"{state} with {primary} and {secondary} Analysis"
    if state == "Overall India":
        fig = px.scatter_mapbox(df,lat="Latitude",lon="Longitude",mapbox_style="open-street-map",
                            color=primary,size=secondary,zoom=3,height=525,width=700,hover_name="District")
    else:
        fig = px.scatter_mapbox(df[df["State"] == state],lat="Latitude",lon="Longitude",mapbox_style="open-street-map",
                            color=primary,size=secondary,zoom=4.5,hover_name="District")
    
    return title,fig

@app.callback(Output("title2","children"),Output("graph2","figure"),
              [Input("state","value"),Input("primary_attribute","value")])
def chose2(scatter_state,scatter_primary):
    
    title = f"{scatter_state} with {scatter_primary} Analysis"
    if scatter_state == "Overall India":
        temp_df = df.groupby("State")[scatter_primary].sum().sort_values(ascending=False).head(7)
        fig = px.bar(temp_df,x=temp_df.index,y=temp_df.values,width=750,height=450).update_yaxes(title=scatter_primary)
    else:
        temp_df = df.query(f"State == '{scatter_state}'").sort_values(scatter_primary,ascending=False).head(7)
        fig = px.bar(temp_df,x=temp_df["District"],y=temp_df[scatter_primary]) 
        
    return title,fig

if __name__ == "__main__":
    app.run(jupyter_mode="tab",debug=True,port=2050)