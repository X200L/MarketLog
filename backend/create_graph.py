from collections import defaultdict
from backend.search_bfs import search_bfs


def create_graph(vertex_list, start_cell):
    # функция построения графа связных ячеек, достежимых из операционной зоны

    """функция принимает на вход список всех вершин, координаты
     операционной зоны и путь выходного файла"""

    graph = defaultdict(list)

    for i in vertex_list:
        for j in vertex_list:
            if i != j:
                if (abs(i[0] - j[0]) * abs(i[1] - j[1]) == 0 and
                        abs(i[0] - j[0]) + abs(i[1] - j[1]) == 1):
                    graph[i].append(j)

    true_vertex = search_bfs(graph, start_cell)
    result_graph = defaultdict(list)
    for i in true_vertex:
        result_graph[i] = graph[i]

    return result_graph


if __name__ == "__main__":
    pass