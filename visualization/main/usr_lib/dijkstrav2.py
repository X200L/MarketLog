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
    dist[start] = 0.0
    for i in range(0, len(unvisited)):
        closest = '0:0'
        for node in unvisited:
            if dist[node] < dist[closest]:
                closest = node
        if dist[closest] == float('inf'):
            return dist, neighbours
        unvisited.pop(unvisited.index(closest))
        visited.append(closest)
        for node in graph[closest]:
            if node in unvisited:
                if dist[node]> dist[closest]+1:
                    dist[node] = dist[closest]+1
                    neighbours[node] = closest
    return dist, neighbours
        


    
