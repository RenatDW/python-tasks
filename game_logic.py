import random
import json
import os
from typing import List, Tuple, Optional

class Game:
    def __init__(self, grid_size: int = 9, colors: int = 5):
        self.grid_size = grid_size
        self.colors_count = colors
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.next_balls = []
        self.selected_ball = None
        self.score = 0
        self.record = self.load_record()  # Загружаем рекорд при инициализации
        self.generate_next_balls(3)

    def generate_next_balls(self, count: int):
        self.next_balls = [random.randint(1, self.colors_count) for _ in range(count)]

    def add_random_balls(self, count: int) -> bool:
        empty_cells = [(x, y) for x in range(self.grid_size)
                       for y in range(self.grid_size) if self.grid[x][y] == 0]

        if not empty_cells:
            return False

        for _ in range(min(count, len(empty_cells))):
            x, y = random.choice(empty_cells)
            self.grid[x][y] = random.randint(1, self.colors_count)
            empty_cells.remove((x, y))
        return True

    @property
    def is_new_record(self) -> bool:
        """Проверяет, побит ли текущий рекорд"""
        return self.score > self.record

    @staticmethod
    def get_record_path() -> str:
        """Возвращает абсолютный путь к файлу рекордов"""
        try:
            dir_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            # Если __file__ недоступен, используем домашнюю директорию
            dir_path = os.path.expanduser("~")
        record_path = os.path.join(dir_path, 'lines98_record.json')
        print(f"Путь к файлу рекордов: {record_path}")
        return record_path

    def load_record(self) -> int:
        """Загружает рекорд из файла"""
        try:
            if os.path.exists(self.get_record_path()):
                with open(self.get_record_path(), 'r') as f:
                    data = json.load(f)
                    record = data.get('record', 0)
                    print(f"Загружен рекорд: {record}")
                    return record
            else:
                print("Файл рекордов не найден")
        except Exception as e:
            print(f"Ошибка загрузки рекорда: {e}")
        return 0
    def save_record(self):
        """Сохраняет рекорд только если он побит"""
        if self.is_new_record:
            self.record = self.score  # Обновляем рекорд сразу
            try:
                with open(self.get_record_path(), 'w') as f:
                    json.dump({'record': self.record}, f)
                print(f"Рекорд {self.record} успешно сохранён")
            except Exception as e:
                print(f"Ошибка сохранения рекорда: {e}")

    @property
    def is_game_over(self) -> bool:
        """Проверяет, остались ли свободные клетки"""
        return all(cell != 0 for row in self.grid for cell in row)

    @staticmethod
    def is_valid_position(x: int, y: int, grid_size: int) -> bool:
        """Проверяет, что координаты в пределах поля"""
        return 0 <= x < grid_size and 0 <= y < grid_size

    def deselect_ball(self) -> None:
        """Снимает выделение с шарика"""
        self.selected_ball = None

    def select_ball(self, x: int, y: int) -> None:
        """Выбирает шарик для перемещения"""
        if self.is_valid_position(x, y, self.grid_size) and self.grid[x][y] != 0:
            self.selected_ball = (x, y)

    def move_ball(self, x: int, y: int) -> bool:
        """Перемещает выбранный шарик"""
        if not self.selected_ball or self.grid[x][y] != 0:
            return False

        start_x, start_y = self.selected_ball
        if not self._find_path(start_x, start_y, x, y):
            return False

        self.grid[x][y] = self.grid[start_x][start_y]
        self.grid[start_x][start_y] = 0
        self.selected_ball = None

        if not self._check_lines(x, y):
            self.add_random_balls(3)
        return True

    def _find_path(self, start_x: int, start_y: int, end_x: int, end_y: int) -> bool:
        """Поиск пути (алгоритм BFS)"""
        from collections import deque
        queue = deque()
        queue.append((start_x, start_y))
        visited = set()
        visited.add((start_x, start_y))

        while queue:
            x, y = queue.popleft()
            if (x, y) == (end_x, end_y):
                return True

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (self.is_valid_position(nx, ny, self.grid_size) and
                    self.grid[nx][ny] == 0 and
                    (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return False

    def _check_lines(self, x: int, y: int) -> bool:
        """Проверяет линии из 5+ шариков в 4 направлениях (→, ↓, ↘, ↙)"""
        color = self.grid[x][y]
        if color == 0:
            return False

        directions = [
            (1, 0),  # Горизонталь →
            (0, 1),  # Вертикаль ↓
            (1, 1),  # Диагональ ↘
            (1, -1)  # Диагональ ↙
        ]

        balls_to_remove = set()
        total_removed = False

        for dx, dy in directions:
            line = [(x, y)]

            # Проверяем в одну сторону
            nx, ny = x + dx, y + dy
            while self.is_valid_position(nx, ny, self.grid_size) and self.grid[nx][ny] == color:
                line.append((nx, ny))
                nx += dx
                ny += dy

            # Проверяем в противоположную сторону
            nx, ny = x - dx, y - dy
            while self.is_valid_position(nx, ny, self.grid_size) and self.grid[nx][ny] == color:
                line.append((nx, ny))
                nx -= dx
                ny -= dy

            # Если линия длиной 5+ — добавляем в набор на удаление
            if len(line) >= 5:
                balls_to_remove.update(line)
                total_removed = True

        if total_removed:
            for bx, by in balls_to_remove:
                self.grid[bx][by] = 0
            self.score += len(balls_to_remove) * 10
            return True

        return False