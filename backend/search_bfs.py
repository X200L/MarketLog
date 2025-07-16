from collections import deque


def search_bfs(graph, start, flag=False):
    """функция выполняет обход графа из указаной вершины и
    возвращает вершины, достежимые из неё"""

    dst = {}
    for i in graph:
        dst[i] = float('inf')
    dst[start] = 0

    dq = deque([start])
    visited = list()
    visited.append(start)

    while dq:
        v = dq.popleft()
        for i in graph[v]:
            if i not in visited:
                visited.append(i)
                dq.append(i)
                dst[i] = dst[v] + 1

    if flag:
        return dst

    return visited


if __name__ == "__main__":
    data_test = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E'],
        'G': ['Z', 'X'],
        'X': ['Z'],
        'Z': []
    }

    print(search_bfs(data_test, 'A'))