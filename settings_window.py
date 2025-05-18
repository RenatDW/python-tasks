from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QDialogButtonBox
from game_logic import Game

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Настройки игры")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Размер поля (5-15):"))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(5, 15)
        self.size_spin.setValue(self.parent.game.grid_size)
        layout.addWidget(self.size_spin)

        layout.addWidget(QLabel("Количество цветов (3-8):"))
        self.colors_spin = QSpinBox()
        self.colors_spin.setRange(3, 8)
        self.colors_spin.setValue(self.parent.game.colors_count)
        layout.addWidget(self.colors_spin)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.apply_settings)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def apply_settings(self):
        new_size = self.size_spin.value()
        new_colors = self.colors_spin.value()
        print(f"Применение настроек: размер={new_size}, цветов={new_colors}")

        if (new_size != self.parent.game.grid_size or
                new_colors != self.parent.game.colors_count):
            self.parent.game = Game(grid_size=new_size, colors=new_colors)
            self.parent.game.save_settings()  # Сохраняем настройки
            self.parent.game_widget.game = self.parent.game
            self.parent.game_widget.update_cell_size()
            self.parent.game.add_random_balls(3)
            self.parent.update_score()
            self.parent.update_next_balls()
            self.parent.game_widget.update()

        self.accept()