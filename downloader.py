# -*- coding: utf-8 -*-
import os
import subprocess
from PyQt6 import QtWidgets, QtGui


class Downloader(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.url_label = QtWidgets.QLabel("URL:", self)
        self.url_input = QtWidgets.QLineEdit(self)
        self.format_label = QtWidgets.QLabel("Format:", self)
        self.format_combo = QtWidgets.QComboBox(self)
        self.format_combo.addItems(["Audio", "Video"])
        self.download_button = QtWidgets.QPushButton("Download", self)
        self.path_label = QtWidgets.QLabel("Download path:", self)
        self.path_input = QtWidgets.QLineEdit(self)
        self.path_button = QtWidgets.QPushButton("...", self)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.url_label, 0, 0)
        self.layout.addWidget(self.url_input, 0, 1)
        self.layout.addWidget(self.format_label, 1, 0)
        self.layout.addWidget(self.format_combo, 1, 1)
        self.layout.addWidget(self.path_label, 2, 0)
        self.layout.addWidget(self.path_input, 2, 1)
        self.layout.addWidget(self.path_button, 2, 2)
        self.layout.addWidget(self.download_button, 3, 1)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.layout)
        self.setLayout(self.main_layout)

        self.download_button.clicked.connect(self.download)
        self.path_button.clicked.connect(self.selectPath)

        self.setWindowTitle("Downloader")
        self.setWindowIcon(QtGui.QIcon("./resources/ico.ico"))
        self.setMinimumSize(400, 150)
        self.setMaximumSize(500, 100)
        self.show()

    def download(self):

        url = self.url_input.text()
        fmt = self.format_combo.currentText()

        if fmt == "Audio":
            fmt = "bestaudio"
        elif fmt == "Video":
            fmt = "best"

        path = self.path_input.text()

        if not path:
            path = "."

        result = subprocess.run(["yt-dlp", "--format", fmt, "--output", os.path.join(path, "%(title)s.%(ext)s"), url])

        if result.returncode == 0:
            QtWidgets.QMessageBox.information(self, "Download completed", "The file has been downloaded successfully")
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "An error occurred during download")

    def selectPath(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select download folder")

        if path:
            self.path_input.setText(path)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Downloader()

    app.exec()