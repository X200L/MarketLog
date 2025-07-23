import json


def matrix_to_json(matrix, output_path):
    # функция сохранения дорог графа в json формате

    res = {"road": {}, "type": {}}

    # заполняем тип каждой ячейки матрицы
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            res["type"][f'{i}:{j}'] = f'{matrix[i][j]}'

    # строим граф дорог
    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[i]) - 1):

            # если ячейка - не препятствие
            if matrix[i][j] in {-1, 2, 4}:
                res["road"][f'{i}:{j}'] = []
                nb = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]

                # проверяем её соседей
                for t in nb:
                    # если ячейка - дорога/операционная зона/зона ожидания
                    if matrix[t[0]][t[1]] in {-1, 2, 4}:
                        res["road"][f'{i}:{j}'].append(t)

                    # если ячейка - зарядка
                    if (matrix[t[0]][t[1]] == 3 and matrix[i][j]
                            in {-1, 2, 3, 4}):
                        res["road"][f'{i}:{j}'].append(t)

    # записываем данные в json
    with open(output_path, 'w') as file:
        json.dump(res, file, indent=4)
