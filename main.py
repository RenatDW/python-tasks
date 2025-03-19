import sys




def main():
    matrix = parse_file('input3.txt')
    if not matrix or not check_consistency(matrix):
        print("Файл пуст или содержит некорректные данные.")
        return

    change_column_positions(matrix)

    save_in_file(matrix)

def change_column_positions(matrix):
    if not matrix or not matrix[0]:
        return

    index_min = 0
    index_max = 0
    value_min = sys.maxsize
    value_max = -sys.maxsize - 1

    for j in range(len(matrix[0])):
        column_sum = get_column_sum(matrix, j)
        if column_sum < value_min:
            index_min = j
            value_min = column_sum
        if column_sum > value_max:
            index_max = j
            value_max = column_sum

    for i in range(len(matrix)):
        matrix[i][index_min], matrix[i][index_max] = matrix[i][index_max], matrix[i][index_min]


def get_column_sum(matrix, column_index):
    return sum(row[column_index] for row in matrix)

def check_consistency(matrix):
    first_row_length = len(matrix[0])
    for row in matrix:
        if len(row) != first_row_length:
            return False
    return True

def parse_file(filename):
    matrix = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        row = list(map(int, line.split()))
                        matrix.append(row)
                    except ValueError:
                        print(f"Некорректная строка в файле: {line}")
                        continue
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")

    return matrix


def save_in_file(matrix):
    if not matrix:
        print("Нет данных для сохранения.")
        return

    with open("output.txt", "w") as file:
        for row in matrix:
            file.write(" ".join(map(str, row)) + "\n")


if __name__ == '__main__':
    main()