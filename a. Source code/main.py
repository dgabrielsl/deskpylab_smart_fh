import os
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
from plyer import notification
from deskpy_smart import PDF
from support import Support

os.system('cls')

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()
        self.page()
        self.show()

    def init(self):
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)))
        self.setWindowTitle('DeskPy')
        self.setMinimumWidth(900)
        self.setMinimumHeight(500)
        # self.showMaximized()
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        tb_docs = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)), 'Documentación', self)         # tb: Go to github documentation page.
        tb_updt = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)), 'Buscar actualizaciones', self)         # tb: Search for updates by web-scrapping.
        tb_lstf = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirLinkIcon)), 'Ir al directorio de trabajo', self)      # tb: Open last folder proccesed.
        tb_docs.setShortcuts(['F1','Ctrl+H'])
        tb_updt.setShortcuts(['F2','Ctrl+U'])
        tb_lstf.setShortcuts(['F3','Ctrl+O'])
        tb_docs.triggered.connect(lambda:Support.get_docs(self))
        tb_updt.triggered.connect(lambda:Support.get_updt(self))
        tb_lstf.triggered.connect(lambda:Support.get_lstf(self))
        toolbar.addAction(tb_docs)
        toolbar.addSeparator()
        toolbar.addSeparator()
        toolbar.addAction(tb_updt)
        toolbar.addSeparator()
        toolbar.addSeparator()
        toolbar.addAction(tb_lstf)

    def page(self):
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(30,15,30,15)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # Header.
        h1 = QLabel('DeskPy')
        h1.setMaximumHeight(100)
        h1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h1.setStyleSheet('padding: 15px; margin-bottom: 10px; background: #204038; color: #FFF; border-radius: 5px; font-size: 16px; font-weight: 600;')
        self.layout.addWidget(h1)
        h2 = QLabel('Procesamiento de documentos')
        h2.setStyleSheet('margin-bottom: 10px; color: #888; font-weight: 400;')
        h2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(h2)

        # File dialog management.
        self.sys_path = QLineEdit()
        self.sys_path.setReadOnly(True)
        self.sys_path.setPlaceholderText('Seleccionar directorio de trabajo')
        self.layout.addWidget(self.sys_path)
        self.one_fldr = QPushButton('Uno')
        self.one_fldr.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder)))
        self.one_fldr.setCursor(Qt.CursorShape.PointingHandCursor)
        self.one_fldr.clicked.connect(self.filedialog)
        self.mul_fldr = QPushButton('Grupo')
        self.mul_fldr.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder)))
        self.mul_fldr.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mul_fldr.clicked.connect(self.filedialog)
        self.mul_fldr.setDisabled(True)
        self.sys_lnch = QPushButton('Todo')
        self.sys_lnch.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder)))
        self.sys_lnch.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sys_lnch.clicked.connect(self.filedialog)
        wrap_1 = QHBoxLayout()
        wrap_1.addWidget(self.one_fldr)
        wrap_1.addWidget(self.mul_fldr)
        wrap_1.addWidget(self.sys_lnch)
        wrap_1.setContentsMargins(0,5,0,10)
        self.editf_id = QLineEdit()
        self.editf_id.setPlaceholderText('Identificación')
        self.editf_id.setMaximumWidth(170)
        self.editf_id_bt = QPushButton()
        self.editf_id_bt.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack)))
        self.editf_id_bt.setCursor(Qt.CursorShape.PointingHandCursor)
        self.editf_id_bt.clicked.connect(self.clear_field_id)
        self.editf_fn = QLineEdit()
        self.editf_fn.setPlaceholderText('Nombre y apellidos')
        self.editf_fn.setContentsMargins(9,0,0,0)
        self.editf_fn_bt = QPushButton()
        self.editf_fn_bt.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack)))
        self.editf_fn_bt.setCursor(Qt.CursorShape.PointingHandCursor)
        self.editf_fn_bt.clicked.connect(self.clear_field_fn)
        self.one_fldr.setStyleSheet('padding: 12px 5px;')
        self.mul_fldr.setStyleSheet('padding: 12px 5px;')
        self.sys_lnch.setStyleSheet('padding: 12px 5px;')
        self.editf_id_bt.setStyleSheet('background: none; border: none;')
        self.editf_fn_bt.setStyleSheet('background: none; border: none;')
        wrap_2 = QHBoxLayout()
        wrap_2.addWidget(self.editf_id)
        wrap_2.addWidget(self.editf_id_bt)
        wrap_2.addWidget(self.editf_fn)
        wrap_2.addWidget(self.editf_fn_bt)
        self.crud_read = QPushButton('Leer')
        self.crud_read.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)))
        self.crud_read.setStyleSheet('padding: 10px; border: 1px solid #CCC; border-radius: 2px;')
        self.crud_read.setCursor(Qt.CursorShape.PointingHandCursor)
        self.crud_read.clicked.connect(self.read_next)
        self.crud_read.setDisabled(True)
        self.crud_create = QPushButton('Procesar')
        self.crud_create.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekForward)))
        self.crud_create.setStyleSheet('padding: 10px; border: 1px solid #CCC; border-radius: 2px;')
        self.crud_create.setCursor(Qt.CursorShape.PointingHandCursor)
        self.crud_create.clicked.connect(self.fitem)
        self.crud_create.setDisabled(True)
        self.crud_auto = QPushButton('Auto')
        self.crud_auto.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton)))
        self.crud_auto.setStyleSheet('padding: 10px; border: 1px solid #CCC; border-radius: 2px;')
        self.crud_auto.setCursor(Qt.CursorShape.PointingHandCursor)
        self.crud_auto.clicked.connect(self.auto_pilot)
        self.crud_auto.setDisabled(True)
        self.editf_id_bt.setShortcut('F6')
        self.editf_fn_bt.setShortcut('F7')
        self.sys_lnch.setShortcut('F5')
        self.crud_read.setShortcut('Space')
        self.crud_create.setShortcut('Return')
        self.crud_auto.setShortcut('Ctrl+Return')
        wrap_3 = QHBoxLayout()
        wrap_3.addWidget(self.crud_read)
        wrap_3.addWidget(self.crud_create)
        wrap_3.addWidget(self.crud_auto)
        wrap_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wrap_3.setContentsMargins(0,20,0,0)
        self.h3 = QLabel('Expedientes procesados:')
        self.h3.setStyleSheet('margin: 10px 0; color: #888; font-weight: 400;')
        self.textarea = QPlainTextEdit()
        self.textarea.setPlaceholderText('Ready to use...')
        self.textarea.setReadOnly(True)
        self.layout.addLayout(wrap_1)
        self.layout.addLayout(wrap_2)
        self.layout.addLayout(wrap_3)
        self.layout.addWidget(self.h3)
        self.layout.addWidget(self.textarea)
        self.layout.addStretch()

    def filedialog(self):
        self.bt_sender = self.sender().text()
        self.workspace = QFileDialog.getExistingDirectory()
        self.workspace += '/'
        if self.workspace == '/': self.workspace = ''
        self.sys_path.setText(self.workspace)
        self.textarea.appendPlainText(f'Directorio configurado correctamente.')
        self.crud_read.setDisabled(False)
        self.crud_auto.setDisabled(False)
        self.flist()

    def flist(self):
        self.tree = []
        try:
            list_workspace = os.listdir(self.workspace)
            for leaf in list_workspace:
                self.tree.append(f'{self.workspace}{leaf}')
            self.counter = 0
            if self.bt_sender == 'Uno':
                self.textarea.appendPlainText('Expediente escaneado correctamente.')
                self.textarea.appendPlainText(f'Procesando un expediente...')
            elif self.bt_sender == 'Grupo':
                self.textarea.appendPlainText('Grupo de expedientes escaneados correctamente.')
                self.textarea.appendPlainText(f'Cantidad de expedientes seleccionados: {len(self.tree)}')
            elif self.bt_sender == 'Todo':
                self.textarea.appendPlainText('Directorio escaneado correctamente.')
                self.textarea.appendPlainText(f'Sub-directorios a procesar: {len(self.tree)}')
        except Exception as e: notification.notify(title=f'DeskPy',message=f'Hint: {e.__class__}\nLa ruta o carpeta a escanear no existe o no ha sido configurada, por favor configure una ruta válida.',timeout=5)

    def read_next(self):
        try:
            if self.bt_sender == 'Uno':
                self.working_folder = self.sys_path.text()
                PDF.pdf_srch_text(self)
            elif self.bt_sender == 'Grupo': pass
            elif self.bt_sender == 'Todo':
                self.working_folder = self.tree[self.counter]
                PDF.pdf_srch_text(self)
            self.editf_id.setText(self.result_id)
            self.editf_fn.setText(self.result_fn)
            self.crud_read.setDisabled(True)
            self.crud_create.setDisabled(False)
            self.textarea.appendPlainText(f'\n{self.result_id} {self.result_fn} expediente listo para procesar...')
        except IndexError as e: notification.notify(title=f'DeskPy',message=f'Hint: {e.__class__}\nNo hay más carpetas por procesar en el directorio {self.sys_path.text()}.',timeout=5)
        except Exception as e: notification.notify(title=f'DeskPy',message=f'Hint: {e.__class__}\n{e}.',timeout=5)

    def fitem(self):
            try:
                subf = self.tree[self.counter]
                subf = subf.split('/')
                subf = f'../{subf[-3]}/{subf[-2]}/{subf[-1]}'
                if self.bt_sender == 'Uno': self.textarea.appendPlainText(f'\tProcesando... {subf}')
                else:
                    self.textarea.appendPlainText(f'\tProcesando... {self.counter+1}/{len(self.tree)} || {subf}')
                    self.h3.setText(f'Expedientes procesados ({self.counter+1}/{len(self.tree)}):')
                self.counter += 1
                self.crud_read.setDisabled(False)
                self.crud_create.setDisabled(True)
                try:
                    edit_fields_upper = []
                    edit_fields_upper.append(self.editf_id.text().upper())
                    edit_fields_upper.append(self.editf_fn.text().upper())
                    self.editf_id.setText(edit_fields_upper[0])
                    self.editf_fn.setText(edit_fields_upper[1])
                    PDF.app_deploy(self)
                    self.editf_id.setText('')
                    self.editf_fn.setText('')
                except Exception as e: print(e)
                if len(self.tree) == self.counter:
                    self.textarea.appendPlainText('\nExpediente/directorio de carpetas completado.')
                    self.crud_read.setDisabled(True)
                    self.crud_auto.setDisabled(True)
                    notification.notify(title=f'DeskPy',message='No hay más carpetas por procesar.',timeout=5)
            except: self.textarea.appendPlainText('***No hay más carpetas por procesar***')

    def auto_pilot(self):
        while True:
            self.crud_read.click()
            self.crud_create.click()
            if len(self.tree) == self.counter: break

    def clear_field_id(self):
        self.editf_id.setText('')
        self.editf_id.setFocus()

    def clear_field_fn(self):
        self.editf_fn.setText('')
        self.editf_fn.setFocus()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
            QToolBar{background: #fff;}
            QLineEdit{padding: 4px; color: #444; background-color: #fff; border: 1px solid #797; border-radius: 5px;}
            QPlainTextEdit{color: #00ff00; font-family: Monotype; background-color: #000; border: 1px solid #797; border-radius: 5px;}
            QPushButton:hover{background: #fff;}
        """)
    win = Main()
    sys.exit(app.exec())