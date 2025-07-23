def get_await_zone(x, y, dx, dy, priority='h'):
    """Функция получения координат возможных зон ожидания;
    Функция возвращает координаты 8-ми прямоугольников в матрице, котрые
     должны быть зарезервированы в топологии под потребности логистики;
     Есть возможность указать приоритетную ориентацию прямоугольников
     (вертикальную/горизрнтальную), они будут первыми в выходных данных"""

    m = []

    # создаём список матриц размерности, согласной приоритетной ориентации
    if priority == 'h':
        m = [[[(y, x) for _ in range(dy)] for _ in range(dx)] for _ in range(4)]
        m.extend([[[(x, y) for _ in range(dx)] for _ in range(dy)] for _ in
                  range(4)])
    elif priority == 'v':
        m = [[[(x, y) for _ in range(dx)] for _ in range(dy)] for _ in range(4)]
        m.extend([[[(y, x) for _ in range(dy)] for _ in range(dx)] for _ in
                  range(4)])

    # заполняем матрицы координатами ячеек
    for i in range(len(m[0])):
        for j in range(len(m[0][0])):
            m[0][i][j] = (y - i, x + j)
            m[1][i][j] = (y - i, x - j)
            m[2][i][j] = (y + i, x + j)
            m[3][i][j] = (y + i, x - j)

    for i in range(len(m[4])):
        for j in range(len(m[4][0])):
            m[4][i][j] = (y - i, x + j)
            m[5][i][j] = (y - i, x - j)
            m[6][i][j] = (y + i, x + j)
            m[7][i][j] = (y + i, x - j)

    # переводим матрицы в список координат
    res = []
    for i in m:
        res.append([])
        for a in i:
            for b in a:
                res[-1].append(b)
    return res


if __name__ == "__main__":
    for e in get_await_zone(0, 0, 2, 3):
        for q in e:
            for p in q:
                print(p, end=" ")
            print()
        print('\n\n\n')
