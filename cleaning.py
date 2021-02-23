#%%
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff 

mapbox_token = "pk.eyJ1IjoicHl0aG9ucyIsImEiOiJja2s2dzhmMjcwODM3MndueGR5Y3E4b2QxIn0.09n-pctdAFhEa4NrPbE6MA"
px.set_mapbox_access_token(mapbox_token)

df = pd.read_csv("Unfallorte2019_LinRef.txt",sep = ";")
df.columns

#%%
#general data cleaning

#berlin = 
df = df[df["ULAND"] > 11] 

#leipzig = 
mask1 = df["ULAND"] == 14 #alle säschsischen daten
mask2 = df["UREGBEZ"] == 7
mask3 = df["UKREIS"] == 13
mask4 = df["UGEMEINDE"] == 000
df = df[mask1][mask2][mask3][mask4]


#%%
#drop unimportant columns
df = df.drop(columns=["OBJECTID","UREGBEZ", "UKREIS", "UGEMEINDE","LINREFY", "LINREFX","IstSonstige", "ULAND"])

#rename location columns
df.rename(columns={"YGCSWGS84":"lat"},inplace=True)
df.rename(columns={"XGCSWGS84":"lon"},inplace=True)

#convert location columns from european comma sep values to point separated values
df["lon"] =df["lon"].apply(lambda a: a.replace(",","."))
df["lat"] = df["lat"].apply(lambda a: a.replace(",","."))

#convert location columns to floats
df["lon"] = df["lon"].astype(float)
df["lat"] = df["lat"].astype(float)

#schönere daten und beschreibungen

monate = {
    1:"Januar",2:"Februar",3:"März",4:"April",5:"Mai",
    6:"Juni",7:"Juli",8:"August",9:"September",
    10:"Oktober",11:"November",12:"Dezember"
    }

wochentage = {
    1:"Sonntag",2:"Montag",3:"Dienstag",4:"Mittwoch",5:"Donnerstag",6:"Freitag",7:"Samstag"
    }
arten = {
    1:"Zusammenstoß mit anfahrendem/ anhaltendem/ruhendem Fahrzeug",
    2:"Zusammenstoß mit vorausfahrendem/ wartendem Fahrzeug",
    3:"Zusammenstoß mit seitlich in gleicher Richtung fahrendem Fahrzeug",
    5:"Zusammenstoß mit einbiegendem / kreuzendem Fahrzeug",
    6:"Zusammenstoß zwischen Fahrzeug und Fußgänger",
    7:"Aufprall auf Fahrbahnhindernis",
    8:"Abkommen von Fahrbahn nach rechts",
    9:"Abkommen von Fahrbahn nach links",
    4:"Zusammenstoß mit entgegenkommendem Fahrzeug",
    0:"Unfall anderer Art",
    }
kategorien = {
    1:"Unfall mit Getöteten",
    2:"Unfall mit Schwerverletzten",
    3:"Unfall mit Leichtverletzten",
}

df["datum"] = 0
df["beschreibung"] = 0
df["tag"] = 0

for i in range(len(df.index)):

    monat = df["UMONAT"].iloc[i]
    tag = df["UWOCHENTAG"].iloc[i]
    zeit = df["USTUNDE"].iloc[i]
    art = df["UART"].iloc[i]
    kategorie = df["UKATEGORIE"].iloc[i]

    monat_str = monate[monat]
    tag_str = wochentage[tag]
    art_str = arten[art]
    kategorie_str = kategorien[kategorie]

    str1 = f"{zeit} Uhr,  {tag_str} im {monat_str} 2019 "
    str2 = f"{kategorie_str} " #durch {art_str}"

    df["datum"].iloc[i] = str1
    df["beschreibung"].iloc[i] = str2
    df["tag"].iloc[i] = tag_str


#entferne jetzt ungenutzte reihen
# df = df.drop(columns = ["USTUNDE", "UMONAT", "UWOCHENTAG", "UART", "UKATEGORIE"]) 
#%%
df.to_csv("daten-berlin") 
