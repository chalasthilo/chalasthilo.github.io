from csvReader import *
import math

co2emissions = importCSV("nation.1751_2014.csv",",")
countryISO = importCSV("ISO.csv",",")


def dataprep(data: list):
    def ISO(country: str):
        def maximize(word: str):
            mini = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
            maxi = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
            endword = ""
            for letter in range(len(word)):
                charfound = False
                i = 0
                while not charfound:
                    if word[letter] == mini[i]:
                        endword += maxi[i]
                        charfound = True
                    elif i >= 25:
                        endword += word[letter]
                        charfound = True
                    i += 1
            return endword
        namefound = False
        cnt = 0
        while not namefound:
            if maximize(countryISO[cnt]["name"]) == country:
                return countryISO[cnt]["alpha-3"]
            elif cnt + 1 >= len(countryISO):
                print('ERROR: '+country)
                return 'ERROR: '+country
            cnt += 1
    temp = []
    lastNation = ""
    lastISO = ""
    for i in co2emissions:
        tdict = {}
        tdict["Nation"] = i["Nation"]
        if i["Nation"] == lastNation:
            tdict["ISO"] = lastISO
        else: 
            lastISO = ISO(i["Nation"])
            tdict["ISO"] = lastISO
            lastNation = i["Nation"]
        tdict["Year"] = i["Year"]
        tdict["CO2 (Tons*1000)"] = i["Total CO2 emissions from fossil-fuels and cement production (thousand metric tons of C)"]
        tdict["CO2/Capita (Tons)"] = i["Per capita CO2 emissions (metric tons of carbon)"]
        temp.append(tdict)
        print("Values for "+tdict["Nation"]+" on year "+tdict["Year"]+": PREPARED")
    return temp

def bycountrydata(data: list):
    groupeddata = {}
    lastISO = data[0]["ISO"]
    print("GROUPING: "+lastISO)
    values = []
    for datapoint in data:
        if lastISO != datapoint["ISO"]:
            groupeddata[lastISO] = values
            print("GROUPED: "+lastISO)
            values = []
            lastISO = datapoint["ISO"]
            print("GROUPING: "+lastISO)
        values.append({"Year":datapoint["Year"], "Total_CO2":datapoint["CO2 (Tons*1000)"], "CO2/Cap": datapoint["CO2/Capita (Tons)"]})
    groupeddata[lastISO] = values
    print("GROUPED: "+lastISO)
    return groupeddata

def JSONtemplate(data: dict, iso: str):
    print("Template for "+iso)
    JSON = {
        "data": {
            "values": data[iso]
        },
        "encoding": {
            "x": {
                "field": "Year",
                "axis": {"format": "%Y", "title": None},
                "type": "temporal",
                "timeUnit": "year"
            }
        },
        "layer": [
            {
                "mark": {"stroke": "#ff0000", "type": "line"},
                "encoding": {
                    "y": {
                        "field": "Total_CO2",
                        "type": "quantitative",
                        "axis": {"title": "Emissions CO2 Totales (milliers de Tonnes)", "titlecolor":"#ff0000"}
                    }
                }
            },
            {
                "mark": {"stroke": "#0000ff", "type": "line"},
                "encoding": {
                    "y": {
                        "field": "CO2/Cap",
                        "type": "quantitative",
                        "axis": {"title": "Emissions de CO2 par habitant (Tonnes)", "titlecolor":"#0000ff"}
                    }
                }
            }            
        ],
        "resolve": {"scale": {"y": "independent"}}
    }
    return JSON

def co2percapitadata(data: list):
    percapita2014 = []
    for datapoint in data:
        if datapoint["Year"] == "2014":
            percapita2014.append({"ISO": datapoint["ISO"], "CO2": datapoint["CO2/Capita (Tons)"]})
    return percapita2014

def color(data:list,field:str):
    maxval = 0
    minval = 9**9
    basecolor = (255, 255, 255)
    countrycolors = []
    #On cherche les valeurs minimales et maximales
    for i in data:
        try:
            if float(i[field]) > maxval:
                maxval = float(i[field])
            if float(i[field]) < minval:
                minval = float(i[field])
        except:
            print("No Data")
    maxval += 0.001
    #On parcourt les valeurs des pays
    for i in data:
        value = 0
        try:
            #On fait un produit en croix pour tranformer la valeur/la valeur maximale en la valeur/255 
            value = math.floor((((float(i[field])-minval))*255)/maxval)
            #On utilise la valeur sur 255 pour definir un rouge plus ou moins vif
            valcolor = [basecolor[0], basecolor[1]-value, basecolor[2]-value]
        except:
            #Si il  n'y a pas de donnee on met du gris
            valcolor = [128,128,128]
        def hexcolor(rgbcolor:list):
            #On transforme la couleur d'un tuple RGB a une couleur en hexadecimal (ex: #ff56a5)
            return "#"+str(hex(rgbcolor[0]))[2:4]+str(hex(rgbcolor[1]))[2:4]+str(hex(rgbcolor[2]))[2:4]
        countrycolors.append({"ISO": i["ISO"],"Value": i["CO2"] ,"Color": hexcolor(valcolor)})
    return countrycolors

#{ "type": "Feature", "ISO_A3": "ABW", "geometry": { "type": "MultiPolygon", "coordinates": [ [ [ [ -69.996937628999916, 12.577582098000036 ] ] ] ] } },

def geojson_formater(data: list):
    geojson = []
    line = ""
    lineempty = True
    for polygon in range(len(data)):
        if lineempty:
            print("FORMATING "+data[polygon]["ISO_A3"])
            line = '{ "type": "Feature", "ISO_A3": "'+data[polygon]["ISO_A3"]+'", "geometry": { "type": "MultiPolygon", "coordinates": [ '
            lineempty = False
        try:
            if data[polygon+1]["Polygon"] == '0':#data[polygon]["ISO_A3"] != data[polygon+1]["ISO_A3"]:
                line += data[polygon]["Coordinates"]+' ] } }, '
                geojson.append(line)
                lineempty = True
                line = ''
                print(data[polygon]["ISO_A3"]+": FORMATED")
            else:
                line += data[polygon]["Coordinates"]+', '
        except IndexError:
                line += data[polygon]["Coordinates"]+' ] } }, '
                geojson.append(line)
    return geojson
