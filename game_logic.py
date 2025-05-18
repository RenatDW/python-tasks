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
        self.record = self.load_record()
        self.generate_next_balls(3)

    def generate_next_balls(self, count: int):
        self.next_balls = [random.randint(1, self.colors_count) for _ in range(count)]
        print(f"Сгенерированы новые next_balls: {self.next_balls}")

    def add_random_balls(self, count: int) -> bool:
        """Places random balls and checks for lines. Returns True if lines were removed."""
        empty_cells = [(x, y) for x in range(self.grid_size)
                       for y in range(self.grid_size) if self.grid[x][y] == 0]
        if not empty_cells:
            print("Нет пустых клеток для добавления шариков")
            return False

        added = 0
        colors_to_use = self.next_balls[:min(count, len(self.next_balls))]
        if len(colors_to_use) < count:
            colors_to_use.extend([random.randint(1, self.colors_count) for _ in range(count - len(colors_to_use))])

        for color in colors_to_use[:min(count, len(empty_cells))]:
            x, y = random.choice(empty_cells)
            self.grid[x][y] = color
            empty_cells.remove((x, y))
            added += 1
        print(f"Добавлено {added} шариков с цветами: {colors_to_use[:added]}")

        # Check the entire grid for lines after placing balls
        lines_removed = self.check_full_grid()
        # Always regenerate next_balls, whether lines were removed or not
        self.generate_next_balls(3)
        return lines_removed

    @property
    def is_new_record(self) -> bool:
        return self.score > self.record

    @staticmethod
    def get_record_path() -> str:
        try:
            dir_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            dir_path = os.path.expanduser("~")
        record_path = os.path.join(dir_path, 'lines98_record.json')
        print(f"Путь к файлу рекордов: {record_path}")
        return record_path

    @staticmethod
    def get_settings_path() -> str:
        try:
            dir_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            dir_path = os.path.expanduser("~")
        settings_path = os.path.join(dir_path, 'lines98_settings.json')
        print(f"Путь к файлу настроек: {settings_path}")
        return settings_path

    def load_record(self) -> int:
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
        if self.is_new_record:
            self.record = self.score
            try:
                with open(self.get_record_path(), 'w') as f:
                    json.dump({'record': self.record}, f)
                print(f"Рекорд {self.record} успешно сохранён")
            except Exception as e:
                print(f"Ошибка сохранения рекорда: {e}")

    @classmethod
    def load_settings(cls) -> dict:
        try:
            if os.path.exists(cls.get_settings_path()):
                with open(cls.get_settings_path(), 'r') as f:
                    data = json.load(f)
                    print(f"Загружены настройки: {data}")
                    return data
            else:
                print("Файл настроек не найден")
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
        return {'grid_size': 9, 'colors': 5}

    def save_settings(self):
        try:
            with open(self.get_settings_path(), 'w') as f:
                json.dump({'grid_size': self.grid_size, 'colors': self.colors_count}, f)
            print(f"Настройки сохранены: grid_size={self.grid_size}, colors={self.colors_count}")
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    @property
    def is_game_over(self) -> bool:
        return all(cell != 0 for row in self.grid for cell in row)

    @staticmethod
    def is_valid_position(x: int, y: int, grid_size: int) -> bool:
        return 0 <= x < grid_size and 0 <= y < grid_size

    def deselect_ball(self) -> None:
        self.selected_ball = None

    def select_ball(self, x: int, y: int) -> None:
        if self.is_valid_position(x, y, self.grid_size) and self.grid[x][y] != 0:
            self.selected_ball = (x, y)

    def move_ball(self, x: int, y: int) -> bool:
        if not self.selected_ball or self.grid[x][y] != 0:
            return False
        start_x, start_y = self.selected_ball
        if not self._find_path(start_x, start_y, x, y):
            return False
        self.grid[x][y] = self.grid[start_x][start_y]
        self.grid[start_x][start_y] = 0
        self.selected_ball = None
        # Check the entire grid for lines after the move
        if not self.check_full_grid():
            # If no lines were removed, place random balls and check again
            self.add_random_balls(3)
        else:
            self.generate_next_balls(3)  # Update next_balls if lines were removed
        return True

    def _find_path(self, start_x: int, start_y: int, end_x: int, end_y: int) -> bool:
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

    def check_full_grid(self) -> bool:
        """Проверяет всё поле на наличие линий из 5+ шариков одного цвета."""
        balls_to_remove = set()
        total_removed = False

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y] != 0:
                    lines = self._check_lines(x, y)
                    if lines:
                        balls_to_remove.update(lines)
                        total_removed = True

        if total_removed:
            for bx, by in balls_to_remove:
                self.grid[bx][by] = 0
            self.score += len(balls_to_remove) * 10
            print(f"Удалено {len(balls_to_remove)} шариков, начислено {len(balls_to_remove) * 10} очков")
        return total_removed

    def _check_lines(self, x: int, y: int) -> set:
        """Проверяет линии, проходящие через клетку (x, y), возвращает множество шариков для удаления."""
        color = self.grid[x][y]
        if color == 0:
            return set()

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        balls_to_remove = set()

        for dx, dy in directions:
            line = [(x, y)]
            nx, ny = x + dx, y + dy
            while self.is_valid_position(nx, ny, self.grid_size) and self.grid[nx][ny] == color:
                line.append((nx, ny))
                nx += dx
                ny += dy
            nx, ny = x - dx, y - dy
            while self.is_valid_position(nx, ny, self.grid_size) and self.grid[nx][ny] == color:
                line.append((nx, ny))
                nx -= dx
                ny -= dy
            if len(line) >= 5:
                balls_to_remove.update(line)

        return balls_to_remove