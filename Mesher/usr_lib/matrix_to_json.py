import json


def matrix_to_json(matrix, output_path):
    # функция сохранения графа в json формате

    res = {"road": {}, "type": {}}
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            res["type"][f'{i}:{j}'] = f'{matrix[i][j]}'

    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[i]) - 1):
            if matrix[i][j] in {-1, 2, 4}:
                res["road"][f'{i}:{j}'] = []
                nb = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
                for t in nb:
                    if matrix[t[0]][t[1]] in {-1, 2, 4}:
                        res["road"][f'{i}:{j}'].append(t)

    with open(output_path, 'w') as file:
        json.dump(res, file, indent=4)
