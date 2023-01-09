# -*- coding: utf-8 -*-
import os
import subprocess
from PyQt5 import QtWidgets

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

        vbox = QtWidgets.QVBoxLayout()

        vbox.addWidget(self.url_label)
        vbox.addWidget(self.url_input)
        vbox.addWidget(self.format_label)
        vbox.addWidget(self.format_combo)

        hbox = QtWidgets.QHBoxLayout()

        hbox.addWidget(self.path_label)
        hbox.addWidget(self.path_input)
        hbox.addWidget(self.path_button)
        hbox.addWidget(self.download_button)

        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.download_button.clicked.connect(self.download)
        self.path_button.clicked.connect(self.selectPath)

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

    app.exec_()
