#import all needed libraries
import dash
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input,Output

from configparser import ConfigParser
import plotly.express as px
import pandas  as pd
from random import randint
import numpy as np
import plotly.figure_factory as ff

#reading the authentication
config = ConfigParser()
config.read("config.ini")
mapbox = config["mapbox"]
key = mapbox["api_key"]


px.set_mapbox_access_token(key)


#daten einlesen

#unfalldaten
df = pd.read_csv("data/daten-berlin", #sep = ";"
)


#plz-daten
plz = pd.read_csv("data/PLZ.csv", sep = ";")
plz.columns = ["PLZ", "STADT", "lon","lat"]



#maskenbau für die Dropdowns

#beteiligte, value
alle = df.notna() #0
pkw = df["IstPKW"] == 1 #1
bike = df["IstRad"] == 1    #2
fuss = df["IstFuss"] == 1   #3
lkw = df["IstGkfz"] == 1    #4

#verletzungen
tote = df["UKATEGORIE"] == 1
schwerv = df["UKATEGORIE"] == 2 
leichtv = df["UKATEGORIE"] == 3

#straßenzustand
typ1 = df["UTYP1"] == 1 #fahrunfall geschwindigkeit
typ2 = df["UTYP1"] == 2 #abbiegenunfall
typ3 = df["UTYP1"] == 6 #längsverkehr
typ4 = df["UTYP1"] == 5 #ruhender verkehr
typ5 = df["UTYP1"] == 7 # sonsitges

#listen aller zustände
t_liste = [alle, typ1,typ2,typ3,typ4, typ5]
b_liste = [alle, pkw,bike,fuss,lkw]
v_liste = [alle, leichtv, schwerv, tote]

#verschiedene Farbpaletten
colors = [
    px.colors.sequential.Sunsetdark, px.colors.sequential.Tealgrn,
    px.colors.sequential.Oranges, 
    px.colors.sequential.RdPu, px.colors.sequential.PuBu,
    ]




#funktionen für graphen

#changing the whole color template
def c_change(input):
    global color_change
    global color_template
    global font_color
    global hist_color

    if input == "light":
        color_change = ("red")
        color_template = ("light")
        font_color = ("black")
        hist_color = ("#F7F7F7")
    elif input == "dark":
        color_change = ("black")
        color_template = ("dark")
        font_color = ("white") 
        hist_color = ("#31302F")
    elif input == "streets" :
        color_change = ("black")
        color_template = ("streets")
        font_color = ("black")
        hist_color = ("#F4ECE1")

    elif input == "satellite":
        color_change = ("black")
        color_template = ("satellite")
        font_color = ("white")
        hist_color = ("#ADA96E")
c_change("dark")

#generator for map
def figure_generator(df,color_scale = px.colors.sequential.Sunsetdark):

    fig_general = px.scatter_mapbox(
        df, lat = "lat", lon = "lon", color = "USTUNDE",
        hover_name="datum", color_continuous_scale= color_scale,
        custom_data=["datum", "beschreibung"], labels = {"USTUNDE":"Uhrzeit"},
        height=550
        )
    fig_general.update_traces(
        hovertemplate = 
        "%{customdata[0]} <br> %{customdata[1]}"
        )
    fig_general.update_layout(paper_bgcolor=hist_color)

    fig_general.update_layout(font_color=font_color,
        font_family="Open Sans", font_size = 13)

    margins = {"t":0,"l":0,"b":0,"r":0}
    fig_general.update_layout(margin=margins)
    fig_general.update_layout(mapbox= dict(zoom = 9.5))

    fig_general.update_layout(mapbox_style = color_template)
    return fig_general

#the histgram 
def hist_generator(df, color = px.colors.sequential.Tealgrn):

    fig5 = px.histogram(
        df, x = "USTUNDE", 
        color = "USTUNDE",
        color_discrete_sequence= color,
        labels=dict(count = "Anzahl"),
        title = "Unfälle nach Tagszeit 0:00-24:00",
        nbins = 25,
        #autobin = False
        )

    fig5.update_traces(
            hovertemplate = "Anzahl : <b>%{y} </b>",
        )
    fig5.update_traces(autobinx=False, selector=dict(type='histogram'))
    fig5.update_traces(marker_cauto = False, selector=dict(type='histogram'))

    margins = {"t":60,"l":10,"b":10,"r":10}

    fig5.update_layout(
        paper_bgcolor = hist_color,
        font_color=font_color,
        font_family="Open Sans", 
        font_size = 13,
        bargap = 0.2, 
        showlegend = False,
        plot_bgcolor = hist_color,
        margin = margins,
        height = 240,
        xaxis_title = "Uhrzeit",
        yaxis_title = "Anzahl"
    )

    fig5.update_xaxes(showticklabels = True, visible = True, range=[-0.5, 23.5], fixedrange = True, nticks = 25)
    fig5.update_yaxes(showticklabels = True,visible = True, automargin = True)
    return fig5

#hexbin graph
def hexbinner(df, c):
    fig = ff.create_hexbin_mapbox(
            df, lat = "lat", lon = "lon", nx_hexagon=20,
            opacity = 0.5, min_count=1, title = "Unfallverteilung",
            show_original_data=True, 
            original_data_marker=dict(size=2, opacity=0.4, color="black"),
            color_continuous_scale= c)

    margins = {"t":0,"l":0,"b":0,"r":0}

    fig.update_layout(
        margin = margins,
        paper_bgcolor = "#F7F7F7",
        mapbox = {"zoom": 10},
        mapbox_style = color_template)
    return fig





# start of the app mit meta_tags für Resizing bei kleineren Bildschirmen
app = dash.Dash(__name__, title = "Unfallkarte", update_title="Lade Daten...", meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server

#generelles statisches App layout
app.layout = html.Div(children = [

    html.Div(className="row", children=[

        #this is the left side for the user controls

        html.Div(className="four columns div-user-controls",children=[

            

            html.A(className = "div-logo", href = f"https://skriptum.github.io", 
                target= "_blank", children = [html.B("Home")]
            ),
            html.Div(className = "twelve columns", children = [html.Br()]),

            html.H1("INTERAKTIVE UNFALLKARTE", style = {"color": font_color}),

            dcc.Markdown(
                """ Täglich passieren auf unseren Straßen unzählige Unfälle mit Personenschaden.
                    Hier können mehr sie die Unfälle vor ihrer Haustür erfahren, als auch interaktiv alle Unfälle 
                    nach ihren eigenen Kategorien filtern.   
                 """
            ),
            html.Br(),

            html.Div( children = [
                html.Div(className = "", id = "outputplz", children = ["lädt"]),

                html.Div(className = "div-for-dropdown",children = [
                    dcc.Input(
                        id = "inputplz", type = "number", placeholder = "Postleitzahl eingeben", 
                         debounce = True, className = "div-for-slider",
                        style = {"background-color": "#1a1919", "color": "white"},
                        ),
                ]),
            ]),

            #html.P("Beteiligte Fahrzeugarten",style = {"font-size": 15}),
            #Beteiligte
            html.Div(className = "div-for-dropdown", children = [
                dcc.Dropdown(id = "selector", options = [
                    {'label': 'Alle Fahrzeugarten', 'value': 0},
                    {'label': 'Unfälle mit Fahrradfahrern', 'value': 1},
                    {'label': 'Unfälle mit PKW', 'value': 2},
                    {'label': 'Unfälle mit Fussgägngern', 'value': 3},
                    {'label': 'Unfälle mit LKWs', "value" : 4},
                    ],
                    clearable = False,
                    value = 0,
                    searchable = False),
            ]),
            #html.P("Grad der menschlichen Schäden",style = {"font-size": 15}),
            #verletzte
            html.Div(className = "div-for-dropdown", children = [
                dcc.Dropdown(id = "verletzt", options = [
                    {'label': "Alle Schäden", 'value': 0 },
                    {'label': "Leichtverletzte", 'value': 1 },
                    {'label': 'Schwerverletzte', 'value': 2},
                    {'label': 'Getötete', 'value': 3},
                    
                    ],
                    clearable = False,
                    value = 0,
                    searchable = False),
            ],),

            #html.P("Unfalltyp",style = {"font-size": 15}),
            #straßenzustand
            html.Div(className = "div-for-dropdown", children = [
                dcc.Dropdown(id = "typus", options = [
                    {'label': "Alle Unfalltypen", 'value': 0 },
                    {'label': "Geschwindigkeitsübertreten", 'value': 1 },
                    {'label': "Abbiegeunfall", 'value': 2 },
                    {"label": "U. mit fahrendem Fahrzeug", 'value': 3 },
                    {'label': "U. mit ruhendem Fahrzeug", 'value': 4 },
                    {"label": "Sonstige", 'value': 5}
                    
                    ],
                    clearable = False,
                    value = 0,
                    searchable = False),
            ],),

            #html.P("Darstellung",style = {"font-size": 15}),
            #straßenzustand
            html.Div(className = "div-for-dropdown", children = [
                dcc.Dropdown(id = "farbe", options = [
                    {'label': "Helle Karte", 'value': "light" },
                    {'label': "Dunkle Karte", 'value': "dark" },
                    {"label": "Straßenkarte", 'value': "streets"},
                    {'label': "Satellitenkarte", 'value': "satellite"}
                    
                    ],
                    clearable = False,
                    value = "light",
                    searchable = False),
            ],),

            html.H1(id = "output_zahl"),

            dcc.Markdown(
                children=[
                    "Quelle: [Statistisches Bundesamt, Datenstand 2019](https://unfallatlas.statistikportal.de/_opendata2020.html)"
                ]
            ),
            html.Br(),

        ]),

        #this is the right side for the graphs and tabs
        
        html.Div(className="eight columns div-for-charts",children=[ 

            dcc.Tabs(id = "tabben", children = [ #der Tabs Behälter

                dcc.Tab(id = "eins", label = "Karte", children = [
                    html.Div(className = "row", children = [
                        html.Div(children = [
                            dcc.Graph(id="map-graph",
                            style = {"height": 550}, config = {"displaylogo": False},
                            ),
                        ]),
                    ]),


                    dcc.Graph(id="histogram",
                    config = {'displayModeBar': False, "responsive": False},
                    style = {"height": 250}
                    ),
                    
                    
                ], selected_className = "tab_select_style", className = "tab_normal_style",
                ),


                dcc.Tab(label = "Vergleich", children = [

                    html.Div(className = "hexbin", children = [
                        dcc.Graph(id = "hexbin",
                            style = {"height": 800}, config = {"displaylogo": False} , 
                        )
                    ]),


                ], selected_className = "tab_select_style", className = "tab_normal_style",),

            ], 
            colors = { "primary": "red"}, mobile_breakpoint = 0, 
            ), 
        ]),
  

    ]),
])





#interactivity of the web app

@app.callback(
    dash.dependencies.Output("output_zahl", "children"),
    dash.dependencies.Output("histogram", "figure"),
    dash.dependencies.Output("map-graph", "figure"),
    dash.dependencies.Output("outputplz", "children"),
    dash.dependencies.Output("hexbin", "figure"),

    dash.dependencies.Input("typus", "value"),
    dash.dependencies.Input("selector", "value"),
    dash.dependencies.Input("verletzt", "value"),
    dash.dependencies.Input("farbe", "value"),
    dash.dependencies.Input("inputplz", "value"),
)

def update_graph(typ_val, b_val, v_val, f_val, num_val):

    #generating both figures
    c = colors[b_val]

    t_mask = t_liste[typ_val]
    b_mask = b_liste[b_val]
    v_mask = v_liste[v_val]
    c_change(f_val)

    data = df[b_mask][v_mask][t_mask]

    if len(data) == 0:
        d = {"lat": 52.520008, "lon": 13.404954, "datum": "ERROR", "beschreibung": "Keine Daten zu dieser Konfiguration verfügbar", "USTUNDE": 24, "UWOCHENTAG": 0} 
        data = pd.DataFrame(data= d, index = [0])

    fig = figure_generator(data, c)

    hist  = hist_generator(data, c)

    hex = hexbinner(data, c)



    #finding out the number of datapoints
    zahl = len(data)
    anzahl = "Unfälle der Kombination: " + str(zahl)

    if zahl == 1:
        anzahl = "Gab es zum Glück nicht in der gewählten Kombination"

    #turning PLZ to mask
    mask = plz["PLZ"] == num_val
    plz_data = plz[mask]

    if len(plz_data) == 1:
        lati = plz_data.lat.values.item()
        long = plz_data.lon.values.item()
        fig.update_layout(
            mapbox = {
            'center': {'lon': long, 'lat': lati},
            "zoom":13}
            )
        text = "PLZ: " + plz[mask]["STADT"]
    
    else:
        text = "PLZ: (andere) eingeben"


    return anzahl, hist, fig, text, hex





#definitions for running
if __name__ == "__main__":
    app.run_server(debug = True)

