import os
from collections import defaultdict
import math


class Line:
    def __init__(self, a, b, c, index):
        self.a = a
        self.b = b
        self.c = c
        self.index = index  # Индекс линии в исходном списке

    def get_key(self):
        # Нормализуем коэффициенты (a, b)
        gcd_val = math.gcd(self.a, self.b)
        if gcd_val == 0:
            return (0, 0)
        return (self.a // gcd_val, self.b // gcd_val)


def read_lines_from_file(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for idx, line in enumerate(file):
            line = line.strip()
            if not line:
                continue
            parts = list(map(int, line.split()))
            if len(parts) != 3:
                raise ValueError(f"Неверный формат строки: {line}")
            a, b, c = parts
            lines.append(Line(a, b, c, idx))
    return lines


def find_max_parallel_lines(lines):
    if not lines:
        return []

    groups = defaultdict(list)
    for line in lines:
        key = line.get_key()
        groups[key].append(line.index)

    max_group = max(groups.values(), key=len)
    return max_group


def write_results_to_file(output_path, indices, input_file):
    with open(output_path, 'w') as f:
        f.write(f"Результат анализа файла: {input_file}\n")
        f.write(f"Найдено {len(indices)} параллельных линий\n")
        f.write("Индексы линий: " + ", ".join(map(str, indices)) + "\n")
        f.write("\nПодробная информация:\n")
        for idx in indices:
            line = lines[idx]
            f.write(f"Линия {idx}: {line.a}x + {line.b}y + {line.c} = 0\n")


def task_three(input_file, output_file="output.txt"):
    try:
        global lines  # Делаем доступным для write_results_to_file
        lines = read_lines_from_file(input_file)
        if not lines:
            print("Файл пуст или содержит некорректные данные.")
            return []

        max_parallel_indices = find_max_parallel_lines(lines)

        print(f"Наибольшее множество параллельных линий (индексы): {max_parallel_indices}")
        write_results_to_file(output_file, max_parallel_indices, input_file)
        print(f"Результаты записаны в файл: {output_file}")

        return max_parallel_indices

    except FileNotFoundError:
        print(f"Файл {input_file} не найден.")
        return []
    except ValueError as e:
        print(f"Ошибка в данных: {e}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


if __name__ == '__main__':
    input_file = "input.txt"
    output_file = "output.txt"

    # Создаем пример входного файла, если его нет
    if not os.path.exists(input_file):
        with open(input_file, 'w') as f:
            f.write("1 2 3\n")
            f.write("2 4 5\n")
            f.write("3 6 7\n")
            f.write("1 1 1\n")
            f.write("2 2 2\n")

    task_three(input_file, output_file)