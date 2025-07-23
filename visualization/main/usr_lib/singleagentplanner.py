import json
from pathlib import Path
import usr_lib.dijkstrav2 as dijkstra
import usr_lib.readmaptxt as maptxt
#Инициализация
def drawagentmap(target, agentspaths, pathmap, start, f):
    #pathmap - 2х-мерный массив с картой из двух типов знаков (стена - 1, стеной считаются все клетки, через которые не может проехать робот со стеллажом, и дорога - 0)
    #agentsloc - локации всех агентов кроме текущего в виде 2х-мерного массива
    #target - цель агента
    #start - текущая локация агента
    graph = {}
    path = []
    pathmap[target[0]][target[1]] = '0'
    #print(len(pathmap[10]))
    d = 0
    for i in range(0, len(pathmap)):
        for j in range(0, len(pathmap[i])):
            #print(j)
            graph[(str(i)+':'+str(j))] = []
            #graph[str(f)+str(d)] = []
            if pathmap[i][j] == '0' or pathmap[i][j]=='R' or pathmap[i][j]=='2'  or pathmap[i][j]=='S'  or pathmap[i][j]=='%':
                if pathmap[i+1][j] == '0' or pathmap[i+1][j] == 'R' or pathmap[i+1][j] == 'S' or pathmap[i+1][j] == '%':
                    graph[(str(i)+':'+str(j))].append((str(i+1)+':'+str(j)))
                    #print('connection down')
                if pathmap[i][j+1] == '0' or pathmap[i][j+1] == 'R' or pathmap[i][j+1] == 'S' or pathmap[i][j+1] == '%':
                    graph[(str(i)+':'+str(j))].append((str(i)+':'+str(j+1)))
                    #print('connection right')
                if pathmap[i-1][j] == '0' or pathmap[i-1][j] == 'R'or pathmap[i-1][j] == 'S'or pathmap[i-1][j] == '%':
                    graph[(str(i)+':'+str(j))].append((str(i-1)+':'+str(j)))
                    #graph[(str(i)+':'+str(j))].append(str(f)+str(d))
                    #graph[str(f)+str(d)].append((str(i)+':'+str(j)))
                    #print('connection up')
                if pathmap[i][j-1] == '0' or pathmap[i][j-1] == 'R' or pathmap[i][j-1] == 'S' or pathmap[i][j-1] == '%':
                    graph[(str(i)+':'+str(j))].append((str(i)+':'+str(j-1)))
                #graph[(str(i)+':'+str(j))].append(str(f)+str(d))
                #graph[str(f)+str(d)].append((str(i)+':'+str(j)))
                    #print('connection left')
                d+=1
    #print(graph[str(target[0])+':'+str(target[1])])
    #print('----')
    dist, paths  = dijkstra.dijkstra(start, graph)
    current = str(target[0])+':'+str(target[1])
    path.append(current)
    t=1
    x=0
    while path[-1]!=str(start[0])+':'+str(start[1]):
        currays = paths[current]
        #print(currays)
        for l in range(len(agentspaths)):
            #print('stage1')
            if t<=len(agentspaths[l]):
                #print('stage2')
                if agentspaths[l]:
                    for s in range(len(currays)):
                        #print(str(currays[0])+'?'+str(agentspaths[l][-t]))
                        if agentspaths[l][-t]==currays[0] or currays[0] in path:
                            print(path)
                            print(str(currays[0])+'='+str(agentspaths[l][-t]))
                            currays.pop(0)

        if not(currays):
            return
        if x<len(currays):
        
            if not(currays[x] in path):
                path.append(currays[x])
                current = currays[x]
                x = 0
            else:
                x+=1
        else:
            return
        t+=1

    #print('---')
    #print(path)
    #print('---')
    return path



def startcords(pathmap):
    graph = {}
    w = []
    d = 0
    for i in range(0, len(pathmap)):
        #print(i)
        for j in range(0, len(pathmap[i])):
            #print(j)
            graph[(str(i)+':'+str(j))] = []
            if pathmap[i][j] == '0' or pathmap[i][j]=='R' or pathmap[i][j]=='2'  or pathmap[i][j]=='S'  or pathmap[i][j]=='%':
                if pathmap[i+1][j] == '0' or pathmap[i+1][j] == 'R' or pathmap[i+1][j] == 'S' or pathmap[i+1][j] == '%':
                    graph[(str(i)+':'+str(j))].append((str(i+1)+':'+str(j)))
                    #print('connection down')
                if pathmap[i][j+1] == '0' or pathmap[i][j+1] == 'R' or pathmap[i][j+1] == 'S' or pathmap[i][j+1] == '%':
                    graph[(str(i)+':'+str(j))].append((str(i)+':'+str(j+1)))
                    #print('connection right')
                if pathmap[i-1][j] == '0' or pathmap[i-1][j] == 'R'or pathmap[i-1][j] == 'S'or pathmap[i-1][j] == '%':
                    graph[(str(i)+':'+str(j))].append((str(i-1)+':'+str(j)))
                    #print('connection up')
                if pathmap[i][j-1] == '0' or pathmap[i][j-1] == 'R' or pathmap[i][j-1] == 'S' or pathmap[i][j-1] == '%':
                    graph[(str(i)+':'+str(j))].append((str(i)+':'+str(j-1)))
                    #print('connection left')
                d+=1
            if len(graph[(str(i)+':'+str(j))]) ==3:
                w.append([i,j])
    return w
