import json
from pathlib import Path
import usr_lib.dijkstra as dijkstra
import usr_lib.readmaptxt
#Инициализация
def drawagentmap(target, agentspaths, pathmap, start, f):
    #pathmap - 2х-мерный массив с картой из двух типов знаков (стена - 1, стеной считаются все клетки, через которые не может проехать робот со стеллажом, и дорога - 0)
    #agentsloc - локации всех агентов кроме текущего в виде 2х-мерного массива
    #target - цель агента
    #start - текущая локация агента
    graph = {}
    pathmap[target[0]][target[1]] = '0'
    #print(len(pathmap[10]))
    for i in range(0, len(pathmap)):
        #print(i)
        for j in range(0, len(pathmap[i])):
            #print(j)
            graph[(str(i)+':'+str(j))] = []
            if pathmap[i][j] == '0':
                #print('loc: '+str(pathmap[i][j]))
                if pathmap[i][j] == '17:29':
                    print('test')
                if pathmap[i+1][j] == '0':
                    graph[(str(i)+':'+str(j))].append((str(i+1)+':'+str(j)))
                    #print('connection down')
                if pathmap[i][j+1] == '0':
                    graph[(str(i)+':'+str(j))].append((str(i)+':'+str(j+1)))
                    #print('connection right')
                if pathmap[i-1][j] == '0':
                    graph[(str(i)+':'+str(j))].append((str(i-1)+':'+str(j)))
                    #print('connection up')
                if pathmap[i][j-1] == '0':
                    graph[(str(i)+':'+str(j))].append((str(i)+':'+str(j-1)))
                    #print('connection left')
    #print(graph)
    return dijkstra.dijkstra(graph,str(start[0])+':'+str(start[1]),str(target[0])+':'+str(target[1]), agentspaths, f)
