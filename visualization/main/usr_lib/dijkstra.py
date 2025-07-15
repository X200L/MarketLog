#import json
#from pathlib import Path
#Инициализация
def sortdict(unsorted):
    sorted_dict = {k: v for k, v in sorted(unsorted.items(), key=lambda item: item[1])}
    return sorted_dict
def dijkstra (graph, start, target):
    queue = []
    distances = {}
    parents = {}
    path = []
    paths = {}
    for i in range(0,len(graph)):
        distances[list(graph.keys())[i]] = float('inf')
        parents[list(graph.keys())[i]] = []
    distances[start] = 0
    #print(distances[start])
    bfs = []
    bfs.append(start)
    queue.append(start)
    while bfs:
        for i in range(0, len(graph[bfs[0]])):
            if not(graph[bfs[0]][i] in queue):
                #print(bfs)
                queue.append(graph[bfs[0]][i])
                bfs.append(graph[bfs[0]][i])
        bfs.pop(0)
    #print(queue)
    for i in range(0, len(queue)):
        for j in range(0,len(graph[queue[i]])):
            distance = distances[queue[i]] +1
            #print(i)
            #print(distances[queue[i]])
            if distances[graph[queue[i]][j]] > distance:
                distances[graph[queue[i]][j]] = distance
                parents[graph[queue[i]][j]].append(queue[i])
                #print(parents)
                for c in range(0,len(parents[queue[i]])):
                    parents[graph[queue[i]][j]].append(parents[queue[i]][c])
                
    #print(sortdict(distances))
    #print(parents)
    return parents[target]
"""with open(Path("../visualization/main/graph/data.json"), "r", encoding="utf-8") as file:
    data = json.load(file)
print(dijkstra(data['graph'], input('start: '), '0:0'))"""