#Importation des librairies
import folium
from Donnees import *
#import pandas
import time
#Importation de tous les fichiers CSV grace a importCSV
print("IMPORTING Emissions")
co2emissions = importCSV("nation.1751_2014.csv",",")
print("Emissions: IMPORTED")
print("IMPORTING ISO data")
countryISO = importCSV("ISO.csv",",")
print("ISO data: IMPORTED")
print("IMPORTING Country outlines")
countryoutlinescsv = importCSV("Pointsfrontierespays.csv",",")
print("Country Outlines: IMPORTED")
#On convertit les contours des pays en strings de geoJSON
print("CONVERTING Country Outlines")
countryoutlines = geojson_formater(countryoutlinescsv)
#del(countryoutlinescsv)
print("Country Outlines: CONVERTED")
print("#"*128)
#On initialise la carte folium
print("Generating Map")
m = folium.Map(location=[0, 0], zoom_start=2)
#On prepare les donnees d'emissions en leur ajoutant les codes ISO alpha-3 et on recupere seulement les donnees voulues
print("PREPARING data (applying iso codes to emissions data + minor modifications")
emissiondata = dataprep(co2emissions)
print("data: PREPARED")
#On separe les donnees necessaires pour creer la carte choroplethe
print("EXTRACTING data for Choropleth")
emissions2014 = co2percapitadata(emissiondata)
print("data: EXTRACTED")
#On calcule les couleurs pour chaque pays
print("APPLYING colors")
coloredemissions = color(emissions2014, "CO2")
print("colors: APPLIED")
#On regroupe les donnees par pays pour les grphiques
print("GROUPING data by country")
bycountryemissions = bycountrydata(emissiondata)
print("data: GROUPED")
#On ajoute les couches geoJSON pour chaque pays en precisant la couleur
print("GENERATING: Choropleth")
for country in range(len(coloredemissions)):
    outline = ""
    #On associe le pays a son element geoJSON
    for i in countryoutlines:
        if str(i[32:35]) == coloredemissions[country]["ISO"]:
            outline = i[0:len(i)-2]
            break
    if outline:
        #On definit la couche geoJSON et sa couleur
        colored_country = folium.Choropleth(
            outline,
            name = coloredemissions[country]["ISO"],
            fill_color = coloredemissions[country]["Color"],
            fill_opacity = 0.8
        )
        #On definit le graphique Vega qui sera associe au pays
        graph = JSONtemplate(bycountryemissions, coloredemissions[country]["ISO"])
        #On definit le popup qui sera ajoute au pays
        popup = folium.Popup().add_child(folium.VegaLite(graph))
        #On ajoute le popup a la couche geoJSON
        popup.add_to(colored_country)
        #On ajoute la couche geoJSON sur la carte
        colored_country.add_to(m)
    print(coloredemissions[country]["Color"])
    print(coloredemissions[country]["ISO"]+" ADDED")
print("Choropleth: GENERATED")
#folium.GeoJson(
#    countries,
#    name = "geojson"
#).add_to(m)
'''
folium.Choropleth(
    geo_data=countries,
    name="choropleth",
    data=emissions2014,
    columns=["ISO","CO2"],
    key_on="feature.ISO_A3",
    fill_color="OrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="CO2 emissions 2014 (Thousand Metric Tons)"
).add_to(m)
'''
print("Map: GENERATED")
#On sauvegarde la carte
print("SAVING: Map")
m.save("map.html")
print("SAVED: Map under map.html")