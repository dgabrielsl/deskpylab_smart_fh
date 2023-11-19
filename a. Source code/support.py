import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from plyer import notification
import webbrowser

class Support():
    def get_docs(self):
        def addw(tag,txt,lyt):
            if tag == 'h':
                label = QLabel(txt)
                label.setStyleSheet('padding: 5px; background-color: #fff; font-size: 13px; font-weight: 800; border: 1px solid #000; border-radius: 3px;')
                lyt.addWidget(label)
            if tag == 'p':
                label = QLabel(txt)
                label.setStyleSheet('font-size: 11px;')
                lyt.addWidget(label)

        dialog = QDialog(self)
        dialog.setWindowTitle('DeskPy - Docs')
        dialog.setMinimumWidth(768)
        dialog.setMaximumWidth(768)
        dialog.setContentsMargins(30,30,30,30)
        dlglyt = QVBoxLayout()
        dialog.setLayout(dlglyt)

        h1 = QLabel('Documentación')
        h1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h1.setStyleSheet('padding: 15px; margin-bottom: 10px; background: #204038; color: #FFF; border: 3px ridge #222; border-radius: 5px; font-size: 16px; font-weight: 600;')
        dlglyt.addWidget(h1)

        addw('h','Manual de uso',dlglyt)
        htmldocs = QPushButton('https://dgabrielsl.github.io/support_smart/')
        htmldocs.setStyleSheet('padding: 12px; background: #24B; color: #FFF; font-size: 16px; border: none; border-radius: 5px;')
        htmldocs.setCursor(Qt.CursorShape.PointingHandCursor)
        htmldocs.clicked.connect(lambda:webbrowser.open('https://dgabrielsl.github.io/support_smart/'))
        dlglyt.addWidget(htmldocs)

        sep = QLabel('')
        sep.setStyleSheet('padding: 5px;')
        dlglyt.addWidget(sep)

        addw('h','Código fuente',dlglyt)
        gitlab = QPushButton('https://github.com/dgabrielsl/deskpy_smart')
        gitlab.setStyleSheet('padding: 12px; background: #24B; color: #FFF; font-size: 16px; border: none; border-radius: 5px;')
        gitlab.setCursor(Qt.CursorShape.PointingHandCursor)
        gitlab.clicked.connect(lambda:webbrowser.open('https://github.com/dgabrielsl/deskpy_smart'))
        dlglyt.addWidget(gitlab)
        dlglyt.addStretch()
        dialog.exec()

    def get_updt(self):
        webbrowser.open('https://github.com/dgabrielsl/deskpy_smart')

    def get_lstf(self):
        try: os.startfile(self.sys_path.text())
        except Exception as e: notification.notify(title = f'DeskPy - Open last folder',message = f'Hint: {e.__class__}\nPor favor configure el directorio de trabajo primero.',timeout = 5)