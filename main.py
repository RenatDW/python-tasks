import os
from collections import defaultdict

class Line:
    def __init__(self, a, b, c, index):
        self.a = a
        self.b = b
        self.c = c
        self.index = index  # Индекс линии в исходном списке

    def get_key(self):
        # Нормализуем коэффициенты (a, b), чтобы пропорциональные линии имели одинаковый ключ
        # Например, 2x + 4y + 5 = 0 → (1, 2), 3x + 6y + 7 = 0 → (1, 2)
        gcd_val = gcd(self.a, self.b)
        return (self.a // gcd_val, self.b // gcd_val)

def gcd(a, b):
    # Наибольший общий делитель (для нормализации)
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def read_lines_from_file(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for idx, line in enumerate(file):
            line = line.strip()
            if not line:
                continue  # Пропускаем пустые строки
            parts = list(map(int, line.split()))
            if len(parts) != 3:
                raise ValueError(f"Неверный формат строки: {line}")
            a, b, c = parts
            lines.append(Line(a, b, c, idx))
    return lines

def find_max_parallel_lines(lines):
    if not lines:
        return []

    # Группируем линии по их нормализованному ключу (a, b)
    groups = defaultdict(list)
    for line in lines:
        key = line.get_key()
        groups[key].append(line.index)

    # Находим группу с максимальным количеством линий
    max_group = max(groups.values(), key=len)
    return max_group

def task_three(input_file):
    try:
        lines = read_lines_from_file(input_file)
        if not lines:
            print("Файл пуст или содержит некорректные данные.")
            return []

        max_parallel_indices = find_max_parallel_lines(lines)
        print(f"Наибольшее множество параллельных линий (индексы): {max_parallel_indices}")
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
    # Пример вызова для тестового файла input01.txt
    task_three("input.txt")