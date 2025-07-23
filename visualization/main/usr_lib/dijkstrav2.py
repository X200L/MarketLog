def dijkstra (startin, graph):
    #start - String(name of the start node)
    #graph - dict{"x:y":["x1:y1","x2:y2"]}
    #dist - dict{"x:y":0, "x1:y1":1}
    #Initialization
    start = str(startin[0])+':'+str(startin[1])
    dist = {}
    neighbours = {}
    visited = []
    unvisited = []
    closest = start
    unvisited = list(graph.keys())
    for node in graph:
        dist[node] = float('inf')
        neighbours[node]=[]
    dist[start] = 0.0
    for i in range(0, len(unvisited)):
        closest = '0:0' #всегда является стеной, соответственно расстояние всегда бесконечно
        for node in unvisited:
            if dist[node] < dist[closest]:  #Ищем непосещенную вершину с наименьшим расстоянием
                closest = node
        if dist[closest] == float('inf'):   #Если расстояние до ближайшей вершины бесконечно, значит проход заблокирован со всех сторон, завершаемся с ошибкой
            return dist, neighbours
        unvisited.pop(unvisited.index(closest)) #Сразу удаляем вершину из непосещенных и добавляем в посещенные
        visited.append(closest)
        for node in graph[closest]: #Берем вершину из соседей текущей
            #if node in unvisited:   
                if dist[node]> dist[closest]+1:
                    dist[node] = dist[closest]+1
                    neighbours[node].insert(0, closest)
                #print(neighbours[node])
                else:
                    neighbours[node].append(closest)
    return dist, neighbours
        


    
