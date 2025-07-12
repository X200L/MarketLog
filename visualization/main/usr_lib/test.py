from pathlib import Path
def readtxtmap():
    pathmap = []
    with open(Path("../visualization/main/usr_lib/map.txt"), "r", encoding="utf-8") as file:
        mapl = file.readlines()  # Возвращает список строк
    for i in range(0,len(mapl)):
        pathmap.append([])
        pathmap[i] = mapl[i].split()
        a = ''
        for j in range(0,len(pathmap[i])):
            a = a + ' '+pathmap[i][j]
        print(a)
    return pathmap
