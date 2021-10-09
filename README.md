# Unfallkarte
<img width="1431" alt="screengrab" src="https://user-images.githubusercontent.com/77919093/136674603-6e395f08-954f-4871-8a8f-b9d6fd3fc15f.png">


Eine interaktive Unfallkarte, komplett sortierbar nach eigenen Wünschen und Vorstellungen, schön grafisch dargestellt. Bei Fragen auf die Websote oder eine Mail an [kkx@protonmail.com](mailto:kkx@protonmail.com)

[Karte](https://unfall.herokuapp.com) + [Post](https://skriptum.github.io/blog/projects/2021/02/04/unfallkarte.html) 

## Funktionsweise

Der Unfallatlas des Bundesamtes für Statistik sammelt alle Unfälle in Deutschland und veröffentlicht sie unter einer Open-Data-Lizenz. Die vom Amt veröffentlichte Karte ist leider nicht wunderschön und auch nicht kategoriesierbar. Also habe ich eine App gebaut, die das kann. 

Das script cleaning.py bereitet die riesige Originaldatei auf und sortiert sie nach einer gewünschten Region, im Standardfall Berlin. Diese Datengrundlage wird daraufhin in der dash app genutzt. 

​	*DASH* : Ein python-framework, aufbauend auf *flask*, welches es einfach macht, analytische Web Apps zu bauen.

[Dash-Überblick](https://plotly.com/dash/)

Diese Dash-App lädt die Daten in ein *pandas*-DataFrame und visualisiert sie geografisch mithilfe von Plotly und [Mapbox](mapbox.com). Verschiedene-Dropdownmenüs sortieren den Dataframe und verändern daraufhin die Karte.

Außerdem nutzt die App eine PLZ-Suche, die durch einen weiteren DataFrame und ein Input-Feld aktiviert wird.

Das CSS ist das oft bei Dash-Apps genutzte [CSS](https://codepen.io/chriddyp/pen/bWLwgP.css) von @chriddyp, welches den Bootstrap-Columns ähnelt

## Nachbauen

Um das Ganze selbst nachzubauen, einfach das Repo clonen. (Ich nehme ab hier ein gewisses Verständnis von git und python an).

```bash
git clone https://github.com/skriptum/bundestag.git
cd bundestag/dash 
```

Außerdem wird benötigt ein MapBox API-Key, um das Ganze zu visualiseren. Dafür einfach eine Datei namens *config.ini* erstellen in der Form 

```ini
[mapbox]
api_key = "API-KEY"
```

anschließend in das dash-directory und die App starten

```bash
cd dash
python app.py
```







