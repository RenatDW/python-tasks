import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Сохраняем рекорд при закрытии окна
    def on_exit():
        window.game.save_record()

    app.aboutToQuit.connect(on_exit)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()