def score_function(matrix):
    counter = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                counter += 1


    
    return counter, 0
