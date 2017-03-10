from digraph import *
import re

print("Project for the 'Graph Theory and Combinatorial Analysis'")
print("Students/Authors: Lucas Hagen, Andy Ruiz e Leonardo Bombardelli\n")
fileName = input("Type the name of the file you would like to analyze: ")

try:
    f = open(fileName, "r") # Abre o arquivo
    print("Loading '" + fileName + "':")
    text = f.read() # Carrega o buffer do arquivo
    f.close()

    graph = Digraph().importFromText(text) # Carrega o grafo a partir do buffer do arquivo

    print("\nDigraph Components: " + str(graph.getSCComponents()).replace("'", "")) # Exibe os componentes

    tpSort = graph.topologicalSorting() # Carrega o ordenamento Topológico
    if tpSort != None:
        print("Topological Sorting: " + str(tpSort).replace("'", "").replace("[", "").replace("]", ""))
    else:
        print("Topological Sorting: this digraph has no topological sorting because it is ciclic!")
except Exception:
    print("Error: could not open/find file!")
