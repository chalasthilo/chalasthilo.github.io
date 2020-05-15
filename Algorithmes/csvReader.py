import csv
import sys

csv.field_size_limit(sys.maxsize)

def importCSV(fichier : str, separateur = ";"):
    tCSV = csv.DictReader(open(fichier,'r'), delimiter = separateur)
    return [ dict(ligneDuTableau) for ligneDuTableau in tCSV]

def exportCSV(tableau : list, fichier : str):
    header = tableau[0].keys()
    fichierCSV = csv.DictWriter(open(fichier, 'w'), fieldnames = header)
    fichierCSV.writeheader()
    for ligne in tableau:
        try :
            fichierCSV.writerow(ligne)
        except IndexError:
            print("Le tableau est vide")
            break
    return None

def filtrerLigne(tableau : list, critere : str, valeur : str):
    return [tableau[i] for i in range(len(tableau)) if tableau[i][critere] == valeur]
'''
def filtrerColonne(tableau : list, listeCriteres : str):
    filtrerTableau = []
    for dico in tableau:
        dicofiltrer = {}
        for critere in listeCriteres:
            dicofiltrer[critere] = dico[critere]
        filtrerTableau.append(dicofiltrer)
    return filtrerTableau
'''
def filtrerColonne(tableau : list, listeCriteres : str):
    return [{critere : dico[critere] for critere in listeCriteres} for dico in tableau]

def triTable(tableau: list, critere: str, decroissant = False):
    return sorted(tableau, key=lambda k: k[critere], reverse=decroissant)





#table = importCSV("exemple.csv")

#print(table)
#print(table[0])
#print(table[1])
#print(table[0]["Nom"])
#print(filtrerLigne(table, "Francais", "14"))
#$print(superfiltrerColonne(table, ["Nom", "Science"]))