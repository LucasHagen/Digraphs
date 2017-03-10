from digraph import *
import re
from tkinter import *
import tkinter.filedialog as filedialog

print("Project for the 'Graph Theory and Combinatorial Analysis'")
print("Students/Authors: Lucas Hagen, Andy Ruiz e Leonardo Bombardelli\n")

window = Tk()
fileName =  filedialog.askopenfilename(initialdir = "/",title = "Select graph file",filetypes = (("Txt files","*.txt"),("all files","*.*")))
window.destroy()

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
