from pathlib import Path
import usr_lib.objects as obj
shelves = []
start = []
def readtxtmap(path):
    pathmap = []
    with open(Path(path), "r", encoding="utf-8") as file:
        mapl = file.readlines()  # Возвращает список строк
    for i in range(0,len(mapl)):
        pathmap.append([])
        pathmap[i] = mapl[i].split()
        a = ''
        for j in range(0,len(pathmap[i])):
            a = a + ' '+pathmap[i][j]
            if pathmap[i][j] == '2':
                shelves.append(obj.shelf(i,j))
            if pathmap[i][j] == '%':
                start = [i, j]
        print(a)
    #print(shelves)
    return pathmap, start
