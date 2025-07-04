from collections import deque


def bfs(graph, start):
    """функция выполняет обход графа из указаной вершины и
    возвращает вершины, достежимые из неё"""

    dq = deque([start])
    visited = set()
    visited.add(start)

    while dq:
        v = dq.popleft()
        for i in graph[v]:
            if i not in visited:
                visited.add(i)
                dq.append(i)

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

    print(bfs(data_test, 'A'))
