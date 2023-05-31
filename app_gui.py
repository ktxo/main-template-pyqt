import os
import sys
from PyQt6.QtWidgets import (
QMainWindow,
    QApplication,
    QWidget,
    QFileDialog,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QStatusBar, QLabel, QFrame, QLineEdit, QDialog, QDialogButtonBox, QListWidget,

)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt,QSize

import requests

import _about as about
#---------------------------------------------------------------------------
# Global vars
#---------------------------------------------------------------------------
def resource_path(resource_path):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, resource_path)
    else:
        return resource_path

#---------------------------------------------------------------------------
#   Dummy Class
#---------------------------------------------------------------------------
class DBQuote():
    def __init__(self):
        pass
    @staticmethod
    def quote() -> (str, str):
        return "asas", "author"

class QuoteDialog(QDialog):
    def __init__(self, parent = None):
        super(QuoteDialog, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.setWindowTitle("Random quote")
        self.resize(200,200)
        self.lbl_quote_a = QLabel()
        self.lbl_quote = QLabel()

        layout.addWidget(self.lbl_quote)
        layout.addWidget(self.lbl_quote_a)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        quote = None
        try:
            res = requests.get("https://zenquotes.io/api/random", timeout=1)
            resj = res.json()
            quote = {"quote": resj[0]["q"], "author": resj[0]["a"]}
        except:
            pass
        if quote:
            self.lbl_quote.setText(quote.get("quote"))
            self.lbl_quote_a.setText(quote.get("author"))
        else:
            self.lbl_quote.setText(f"Got some error :-(")


#---------------------------------------------------------------------------
#   GUI
#---------------------------------------------------------------------------
APP_TITLE="PyQT6 app basic"
APP_SIZE= (500,400)
APP_VERSION= "1.0.0"
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle(APP_TITLE)
        self.setFixedSize(QSize(*APP_SIZE))
        self.setWindowIcon(QIcon(resource_path("images/app.ico")))

        # Layout
        # VerticalLayout with 4 widgets:
        #   HorizontalLayout
        #       - label with image
        #       - label with image
        # - Button
        # - Button
        # - Label
        lbl_img1 = QLabel()
        lbl_img1.setScaledContents(True)
        lbl_img1.resize(10, 20)
        lbl_img1.setPixmap(QPixmap(resource_path("images/img1.jpg")).scaled(100,100, Qt.AspectRatioMode.KeepAspectRatio))

        lbl_img2 = QLabel()
        lbl_img2.setScaledContents(True)
        lbl_img2.resize(10, 20)
        lbl_img2.setPixmap(QPixmap(resource_path("images/img2.png")).scaled(100,100, Qt.AspectRatioMode.KeepAspectRatio))

        bt1 = QPushButton('&Dummy button')
        bt1.setToolTip("Open a Dialog and show a random quote")
        # bt1.setFixedSize(200, 30)
        bt1.clicked.connect(self.open_quote_dialog)

        bt2 = QPushButton('&Open file')
        bt2.setToolTip("Open a FileDialog and stat from file")
        #bt2.setFixedSize(200, 30)
        bt2.clicked.connect(self.open_file_dialog)

        bt3 = QPushButton('E&xit')
        bt3.setToolTip("Exit")
        #bt3.setFixedSize(200, 30)
        bt3.clicked.connect(self.exit)

        self.lst_file = QListWidget()

        frame_h = QFrame()
        frame_h.setFrameStyle(QFrame.Shape.Box)
        layout_h = QHBoxLayout(frame_h)
        layout_h.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout_h.addStretch()
        layout_h.addWidget(lbl_img1)
        layout_h.addStretch()
        layout_h.addWidget(lbl_img2)


        layout_v = QVBoxLayout()
        layout_v.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout_v.addWidget(frame_h)
        layout_h.addStretch()
        layout_v.addWidget(bt1)
        layout_v.addWidget(bt2)
        layout_v.addWidget(bt3)
        layout_v.addWidget(self.lst_file)
        layout_v.addStretch()

        widget = QWidget()
        widget.setLayout(layout_v)
        self.setCentralWidget(widget)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Dummy appp objects
        self.quote = DBQuote()
        self.show()
        self.show_message(f"Starting app v{about.__version__} ({about.__date__}) from {os.getcwd()}")


    def show_message(self, message:str, msecs=0):
        """Wrapper to write a message in StatusBar"""
        self.status_bar.showMessage(message, msecs)

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(os.getcwd())
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilters(["All Files (*)", "Excel Files (*.xlsx)", "Images (*.png *.jpg)"])
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            if filename:
                self.update_info(filename)

    def exit(self):
        self.close()

    def update_info(self, filename):
        self.lst_file.clear()
        stats = os.stat(filename)
        stats_ = {"filename": filename}
        stats_.update({k: getattr(stats, k) for k in dir(stats) if k.startswith('st_')})
        for k,v in stats_.items():
            self.lst_file.addItem(f"{k}={v}")
        self.show_message(f"File {filename}")

    def open_quote_dialog(self, filename):
        dlg = QuoteDialog(self)
        result = dlg.exec()
        if result:
            self.show_message(f"Pressed OK")
        else:
            self.show_message(f"Pressed CANCEL")
        # dlg = SearchDialog(self)
        # result = dlg.exec()
        # if result and self.current_row:
        #     self.status_bar.showMessage(f"Archivo {self.current_row['filename']} {self.current_row['created_at']}")
        #

if __name__ == '__main__':
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec())