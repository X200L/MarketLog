import json
from pathlib import Path
import usr_lib.objects as obj
s = []
size = []
def createmap():    
    dots = []
    with open(Path("../visualization/graph/data.json"), "r", encoding="utf-8") as file:
        data = json.load(file)
    for i in range(0, data["length"]):
        dots.append([])
        for j in range(0, data["width"]):
            dots[i].append("")
            if data['properties'][str(j)+':'+str(i)][3]==1:
                dots[i][j] = "#"
            elif data['properties'][str(j)+':'+str(i)][0]==1:
                dots[i][j] = "@"
                s.append(obj.shelf(j,i))
            elif data['properties'][str(j)+':'+str(i)][1]==1:
                dots[i][j] = "$"
            elif data['properties'][str(j)+':'+str(i)][2]==1:
                dots[i][j] = "E"
            else:
                dots[i][j] = " "
    size = [data['width'], data['length']]
    """for i in range(0,len(dots)):
        print(dots[i])
        print("")"""
    return dots, size


        