from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSpacerItem, QSizePolicy, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QColor, QBrush, QPixmap
from game_logic import Game

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        settings = Game.load_settings()
        self.game = Game(grid_size=settings['grid_size'], colors=settings['colors'])
        self.init_ui()
        self.game.add_random_balls(3)
        self.update_next_balls()

    def init_ui(self):
        self.setWindowTitle("Линии 98")
        screen = QApplication.primaryScreen().availableGeometry()
        window_width = int(500)
        window_height = int(600)
        self.setGeometry(
            (screen.width() - window_width) // 2,
            (screen.height() - window_height) // 2,
            window_width,
            window_height
        )
        self.setMinimumSize(400, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        top_panel = QHBoxLayout()
        main_layout.addLayout(top_panel)

        score_panel = QVBoxLayout()
        self.score_label = QLabel(f"Счёт: {self.game.score}")
        self.score_label.setFont(QFont('Arial', 20, QFont.Bold))
        self.score_label.setAlignment(Qt.AlignLeft)
        score_panel.addWidget(self.score_label)

        self.record_label = QLabel(f"Рекорд: {self.game.record}")
        self.record_label.setFont(QFont('Arial', 16))
        self.record_label.setAlignment(Qt.AlignLeft)
        self.record_label.setStyleSheet("color: black;")
        score_panel.addWidget(self.record_label)

        top_panel.addLayout(score_panel)
        top_panel.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

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

        next_balls_panel = QHBoxLayout()
        next_balls_panel.addWidget(QLabel("Следующие:"))
        self.next_ball_labels = []
        for _ in range(3):
            ball_label = QLabel()
            ball_label.setFixedSize(30, 30)
            self.next_ball_labels.append(ball_label)
            next_balls_panel.addWidget(ball_label)

        main_layout.addLayout(next_balls_panel)
        self.game_widget = GameWidget(self.game, self)
        main_layout.addWidget(self.game_widget)

    def update_next_balls(self):
        colors = [
            QColor(255, 0, 0),
            QColor(0, 255, 0),
            QColor(0, 0, 255),
            QColor(255, 255, 0),
            QColor(255, 0, 255),
        ]
        for i, ball in enumerate(self.game.next_balls[:3]):
            pixmap = QPixmap(30, 30)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setBrush(QBrush(colors[ball - 1]))
            painter.setPen(Qt.black)
            painter.drawEllipse(5, 5, 20, 20)
            painter.end()
            self.next_ball_labels[i].setPixmap(pixmap)
        print(f"Обновлены next_balls в UI: {self.game.next_balls[:3]}")

    def new_game(self):
        current_grid_size = self.game.grid_size
        current_colors = self.game.colors_count
        self.game = Game(grid_size=current_grid_size, colors=current_colors)
        self.game_widget.game = self.game
        self.game.add_random_balls(3)
        self.update_score()
        self.update_next_balls()
        self.record_label.setText(f"Рекорд: {self.game.record}")  # Update record label
        self.game_widget.update_cell_size()
        self.game_widget.update()

    def update_score(self):
        self.score_label.setText(f"Счёт: {self.game.score}")
        self.update_next_balls()
        # Update record if a new record is set
        if self.game.is_new_record:
            self.game.save_record()  # Save new record immediately
            self.record_label.setText(f"Рекорд: {self.game.score}")
            self.record_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.record_label.setText(f"Рекорд: {self.game.record}")
            self.record_label.setStyleSheet("color: black; font-weight: normal;")
        print(f"Обновлён рекорд в UI: {self.game.record}")

    def show_settings(self):
        from settings_window import SettingsWindow
        settings_window = SettingsWindow(self)
        settings_window.exec_()

    def show_rules(self):
        from rules_window import RulesWindow
        rules_window = RulesWindow(self)
        rules_window.exec_()

    def show_game_over(self):
        if self.game.is_new_record:
            self.game.save_record()
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
        else:
            self.close()

class GameWidget(QWidget):
    def __init__(self, game: Game, parent: MainWindow):
        super().__init__(parent)
        self.game = game
        self.parent_window = parent
        self.cell_size = 0
        self.update_cell_size()

    def update_cell_size(self):
        widget_size = min(self.width(), self.height())
        self.cell_size = max(30, min(120, widget_size // self.game.grid_size))
        print(f"Обновлён cell_size: {self.cell_size} для grid_size={self.game.grid_size}")
        self.update()

    def resizeEvent(self, event):
        self.update_cell_size()
        super().resizeEvent(event)

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
            QColor(255, 0, 0),
            QColor(0, 255, 0),
            QColor(0, 0, 255),
            QColor(255, 255, 0),
            QColor(255, 0, 255),
        ]
        for x in range(self.game.grid_size):
            for y in range(self.game.grid_size):
                if self.game.grid[x][y] != 0:
                    color = colors[self.game.grid[x][y] - 1]
                    painter.setBrush(QBrush(color))
                    ball_size = max(int(self.cell_size * 0.8), 10)
                    offset = (self.cell_size - ball_size) // 2
                    painter.drawEllipse(
                        x * self.cell_size + offset,
                        y * self.cell_size + offset,
                        ball_size,
                        ball_size
                    )
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
        if self.game.selected_ball == (x, y):
            self.game.deselect_ball()
            self.update()
            return
        if self.game.grid[x][y] != 0:
            self.game.select_ball(x, y)
            self.update()
            return
        if self.game.selected_ball:
            start_x, start_y = self.game.selected_ball
            if not self.game._find_path(start_x, start_y, x, y):
                QMessageBox.information(self, "Невозможно переместить",
                                        "Нет пути к выбранной клетке!")
                return
            if self.game.move_ball(x, y):
                self.parent_window.update_score()
                if self.game.is_game_over:
                    self.parent_window.show_game_over()
        self.update()