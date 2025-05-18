from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextBrowser

class RulesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Правила игры")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        rules_html = """
        <h1>Правила игры Линии 98</h1>
        <p><b>Цель:</b> Собирать линии из 5 и более шариков одного цвета.</p>
        <p><b>Управление:</b></p>
        <ul>
            <li>Кликните на шарик, чтобы выбрать его</li>
            <li>Кликните на пустую клетку, чтобы переместить шарик</li>
        </ul>
        <p>Шарики можно перемещать только по свободным клеткам.</p>
        """

        text_browser = QTextBrowser()
        text_browser.setHtml(rules_html)
        layout.addWidget(text_browser)