from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSpacerItem, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QColor, QBrush, QPixmap

from game_logic import Game


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = Game()  # Стандартные параметры 9x9, 5 цветов
        self.init_ui()
        self.game.add_random_balls(3)

    def init_ui(self):
        self.setWindowTitle("Линии 98")
        self.setFixedSize(600, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Верхняя панель с информацией
        top_panel = QHBoxLayout()
        main_layout.addLayout(top_panel)

        # Левая часть - счёт и рекорд
        score_panel = QVBoxLayout()

        # Надпись "Счёт"
        self.score_label = QLabel(f"Счёт: {self.game.score}")
        self.score_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.score_label.setAlignment(Qt.AlignLeft)
        score_panel.addWidget(self.score_label)

        # Надпись "Рекорд"
        self.record_label = QLabel(f"Рекорд: {self.game.record}")
        self.record_label.setFont(QFont('Arial', 10))
        self.record_label.setAlignment(Qt.AlignLeft)
        self.record_label.setStyleSheet("color: black;")
        score_panel.addWidget(self.record_label)

        top_panel.addLayout(score_panel)

        # Гибкий разделитель
        top_panel.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Правая часть - кнопки
        buttons_panel = QHBoxLayout()

        btn_new_game = QPushButton("Новая игра")
        btn_new_game.clicked.connect(self.new_game)
        buttons_panel.addWidget(btn_new_game)

        btn_settings = QPushButton("Настройки")
        btn_settings.clicked.connect(self.show_settings)
        buttons_panel.addWidget(btn_settings)

        btn_rules = QPushButton("Правила")
        btn_rules.clicked.connect(self.show_rules)
        buttons_panel.addWidget(btn_rules)

        top_panel.addLayout(buttons_panel)

        # Панель "Следующие шарики"
        next_balls_panel = QHBoxLayout()
        next_balls_panel.addWidget(QLabel("Следующие:"))

        self.next_ball_labels = []
        for _ in range(3):  # Показываем 3 следующих шарика
            ball_label = QLabel()
            ball_label.setFixedSize(30, 30)
            self.next_ball_labels.append(ball_label)
            next_balls_panel.addWidget(ball_label)

        main_layout.addLayout(next_balls_panel)  # Исправлено: используем main_layout вместо layout

        # Игровое поле
        self.game_widget = GameWidget(self.game, self)
        main_layout.addWidget(self.game_widget)

        self.update_next_balls()  # Первоначальное обновление


    def update_next_balls(self):
        """Обновляет отображение следующих шариков"""
        colors = [
            QColor(255, 0, 0),  # Красный
            QColor(0, 255, 0),  # Зеленый
            QColor(0, 0, 255),  # Синий
            QColor(255, 255, 0),  # Желтый
            QColor(255, 0, 255),  # Фиолетовый
        ]

        for i, ball in enumerate(self.game.next_balls[:3]):  # Показываем первые 3
            pixmap = QPixmap(30, 30)
            pixmap.fill(Qt.transparent)

            painter = QPainter(pixmap)
            painter.setBrush(QBrush(colors[ball - 1]))
            painter.setPen(Qt.black)
            painter.drawEllipse(5, 5, 20, 20)
            painter.end()

            self.next_ball_labels[i].setPixmap(pixmap)

    def new_game(self):
        """Начинает новую игру"""
        self.game = Game()
        self.game_widget.game = self.game
        self.game.add_random_balls(3)
        self.update_score()
        self.update_next_balls()  # Обновляем отображение
        self.game_widget.update()

    def update_score(self):
        """Обновляет отображение счёта и следующих шариков"""
        self.score_label.setText(f"Счёт: {self.game.score}")
        self.update_next_balls()  # Обновляем после каждого хода

        # Подсветка нового рекорда
        if self.game.is_new_record:
            self.record_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            # Убираем !important, просто явно указываем стиль
            self.record_label.setStyleSheet("color: black; font-weight: normal;")  # Изменено

    def show_settings(self):
        """Показывает окно настроек"""
        from settings_window import SettingsWindow
        settings_window = SettingsWindow(self)
        settings_window.exec_()

    def show_rules(self):
        """Показывает окно правил"""
        from rules_window import RulesWindow
        rules_window = RulesWindow(self)
        rules_window.exec_()


    def show_game_over(self):
        """Показывает сообщение об окончании игры"""
        if self.game.is_new_record:
            self.game.save_record()  # Сохраняем рекорд перед показом сообщения
            message = f"Новый рекорд! {self.game.score}"
        else:
            message = f"Игра окончена! Счёт: {self.game.score}\nРекорд: {self.game.record}"

        msg = QMessageBox()
        msg.setWindowTitle("Конец игры")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText("Новая игра")
        msg.button(QMessageBox.No).setText("Выход")

        result = msg.exec_()
        if result == QMessageBox.Yes:
            self.new_game()


class GameWidget(QWidget):
    def __init__(self, game: Game, parent: MainWindow):
        super().__init__(parent)
        self.game = game
        self.parent_window = parent
        self.update_cell_size()  # Вычисляем размер клетки

    def update_cell_size(self):
        """Обновляет размер клетки при изменении размера поля"""
        self.cell_size = 600 // self.game.grid_size
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_grid(painter)
        self.draw_balls(painter)

    def draw_grid(self, painter):
        painter.setPen(Qt.gray)
        for i in range(self.game.grid_size + 1):
            painter.drawLine(0, i * self.cell_size,
                             self.game.grid_size * self.cell_size, i * self.cell_size)
            painter.drawLine(i * self.cell_size, 0,
                             i * self.cell_size, self.game.grid_size * self.cell_size)

    def draw_balls(self, painter):
        colors = [
            QColor(255, 0, 0),  # Красный
            QColor(0, 255, 0),  # Зеленый
            QColor(0, 0, 255),  # Синий
            QColor(255, 255, 0),  # Желтый
            QColor(255, 0, 255),  # Фиолетовый
        ]

        for x in range(self.game.grid_size):
            for y in range(self.game.grid_size):
                if self.game.grid[x][y] != 0:
                    color = colors[self.game.grid[x][y] - 1]
                    painter.setBrush(QBrush(color))
                    painter.drawEllipse(
                        x * self.cell_size + 5,
                        y * self.cell_size + 5,
                        self.cell_size - 10,
                        self.cell_size - 10
                    )

                # Выделение выбранного шарика
                if self.game.selected_ball == (x, y):
                    painter.setBrush(Qt.NoBrush)
                    painter.setPen(QColor(0, 180, 0))
                    painter.drawRect(
                        x * self.cell_size + 2,
                        y * self.cell_size + 2,
                        self.cell_size - 4,
                        self.cell_size - 4
                    )
                    painter.setPen(Qt.gray)

    def mousePressEvent(self, event):
        x = event.x() // self.cell_size
        y = event.y() // self.cell_size

        if not self.game.is_valid_position(x, y, self.game.grid_size):
            return

        # Если клик на уже выделенный шарик - снимаем выделение
        if self.game.selected_ball == (x, y):
            self.game.deselect_ball()
            self.update()
            return

        # Если клик на другой шарик - выделяем его
        if self.game.grid[x][y] != 0:
            self.game.select_ball(x, y)
            self.update()
            return

        # Если клик на пустую клетку и есть выделенный шарик

        if self.game.selected_ball:
            start_x, start_y = self.game.selected_ball
            if not self.game._find_path(start_x, start_y, x, y):
                QMessageBox.information(self, "Невозможно переместить",
                                        "Нет пути к выбранной клетке!")
                return

            if self.game.move_ball(x, y):
                self.parent_window.update_score()  # Это теперь обновит и шарики
                if self.game.is_game_over:
                    self.parent_window.show_game_over()


        self.update()