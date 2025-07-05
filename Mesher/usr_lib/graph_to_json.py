import json


def graph_to_json(graph, output_path):
    # функция сохранения графа в json формате

    tmp_graph = {}
    for i in graph:
        tmp_graph[f'{i[0]}:{i[1]}'] = list(
            map(lambda c: f'{c[0]}:{c[1]}', graph[i]))

    with open(output_path, 'w') as file:
        json.dump(tmp_graph, file, indent=4)
