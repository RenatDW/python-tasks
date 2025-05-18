from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QDialogButtonBox
from game_logic import Game  # Добавляем импорт класса Game


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Настройки игры")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Размер поля
        layout.addWidget(QLabel("Размер поля (5-15):"))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(5, 15)
        self.size_spin.setValue(self.parent.game.grid_size)
        layout.addWidget(self.size_spin)

        # Количество цветов
        layout.addWidget(QLabel("Количество цветов (3-8):"))
        self.colors_spin = QSpinBox()
        self.colors_spin.setRange(3, 8)
        self.colors_spin.setValue(self.parent.game.colors_count)
        layout.addWidget(self.colors_spin)

        # Кнопки
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.apply_settings)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def apply_settings(self):
        """Применяет новые настройки и перезапускает игру"""
        new_size = self.size_spin.value()
        new_colors = self.colors_spin.value()

        if (new_size != self.parent.game.grid_size or
                new_colors != self.parent.game.colors_count):
            self.parent.game = Game(grid_size=new_size, colors=new_colors)
            self.parent.game_widget.cell_size = 600 // new_size
            self.parent.game_widget.game = self.parent.game
            self.parent.game_widget.update_cell_size()  # Добавленный метод
            self.parent.game.add_random_balls(5)
            self.parent.update_score()
            self.parent.game_widget.update()

        self.accept()