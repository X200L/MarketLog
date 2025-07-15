from collections import deque


def route_builder(input_graph, start, finish):
    visited = {start: None}

    dq = deque([start])
    last = start

    while dq:
        v = dq.popleft()

        if v in finish:
            last = v
            break

        for i in input_graph[v]:
            if i not in visited:
                visited[i] = v
                dq.append(i)

    path = []
    tmp = last
    if tmp in visited:
        while tmp is not None:
            path.append(tmp)
            tmp = visited[tmp]

        path.reverse()
        return path

    return None


if __name__ == "__main__":
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    print(route_builder(graph, 'A', ['F', 'E', 'C']))
