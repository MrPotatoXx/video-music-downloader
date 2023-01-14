# -*- coding: utf-8 -*-
import os
from PyQt6 import QtWidgets, QtGui
import yt_dlp


# Create a new class called "Downloader" that inherits from QWidget
class Downloader(QtWidgets.QWidget):
    def __init__(self):
        # Initialize the parent class
        super().__init__()
        # Call the function to create the UI elements
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

        # Create a grid layout to organize the UI elements
        self.layout = QtWidgets.QGridLayout(self)
        # Add the UI elements to the grid layout
        self.layout.addWidget(self.url_label, 0, 0)
        self.layout.addWidget(self.url_input, 0, 1)
        self.layout.addWidget(self.format_label, 1, 0)
        self.layout.addWidget(self.format_combo, 1, 1)
        self.layout.addWidget(self.path_label, 2, 0)
        self.layout.addWidget(self.path_input, 2, 1)
        self.layout.addWidget(self.path_button, 2, 2)
        self.layout.addWidget(self.download_button, 3, 1)

        # Set the grid layout as the layout for the widget
        self.setLayout(self.layout)

        # Connect the "clicked" signal of the download button to the "download" function
        self.download_button.clicked.connect(self.download)
        # Connect the "clicked" signal of the path button to the "selectPath" function
        self.path_button.clicked.connect(self.selectPath)

        # Set the title and icon of the window
        self.setWindowTitle("Downloader")
        self.setWindowIcon(QtGui.QIcon("./resources/ico.ico"))
        # Set the minimum and maximum size of the window
        self.setMinimumSize(400, 150)
        self.setMaximumSize(500, 100)
        # Show the window
        self.show()

    def download(self):

        # Get the URL from the input field
        url = self.url_input.text()
        # Get the selected format from the dropdown menu
        fmt = self.format_combo.currentText()

        # Map the user-friendly format to the format used by youtube-dl
        if fmt == "Audio":
            fmt = "bestaudio"
        elif fmt == "Video":
            fmt = "best"

        # Get the download path from the input field
        path = self.path_input.text()

        # If no path is provided, use the current directory
        if not path:
            path = "."

        # Create a new YoutubeDL object with the selected format and output template
        downloader = yt_dlp.YoutubeDL({"format": fmt, "outtmpl": os.path.join(path, "%(title)s.%(ext)s")})
        # Start the download
        result = downloader.download([url])

        # Check the result of the download
        # 0 means success
        if result == 0:
            QtWidgets.QMessageBox.information(self, "Download completed", "The file has been downloaded successfully")
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "An error occurred during download")


    def selectPath(self):
        # Open a file dialog to select a directory
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select download folder")

        # If a directory is selected, update the path input field
        if path:
            self.path_input.setText(path)

if __name__ == "__main__":
    # Create a new QApplication
    app = QtWidgets.QApplication([])
    # Create a new Downloader window
    window = Downloader()

    # Start the event loop
    app.exec()