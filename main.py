import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QProgressBar, QFileDialog, QDesktopWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from openai import OpenAI
import requests
from datetime import datetime
import os

class ImageGenerationThread(QThread):
    finished = pyqtSignal(bytes)
    error = pyqtSignal(str)

    def __init__(self, api_key, prompt_text):
        super().__init__()
        self.api_key = api_key
        self.prompt_text = prompt_text

    def run(self):
        client = OpenAI(api_key=self.api_key)
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=self.prompt_text,
                size="1024x1024",
                quality="standard",
                n=1
            )
            image_url = response.data[0].url
            img_data = requests.get(image_url).content
            self.finished.emit(img_data)
        except Exception as e:
            self.error.emit(str(e))

class DalleGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("DALL-E 3 Image Generator")
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width() * 0.50, screen.height() * 0.50)

        window = self.geometry()
        self.move((screen.width() - window.width()) / 2, (screen.height() - window.height()) / 2)


        layout = QVBoxLayout()

        self.api_key_entry = QLineEdit(self)
        self.api_key_entry.setEchoMode(QLineEdit.Password)
        self.api_key_entry.setPlaceholderText("Enter your OpenAI API Key here")
        layout.addWidget(self.api_key_entry)

        self.prompt_entry = QLineEdit(self)
        self.prompt_entry.setPlaceholderText("Enter the prompt for the image generation here")
        layout.addWidget(self.prompt_entry)

        self.generate_button = QPushButton("Generate", self)
        self.generate_button.clicked.connect(self.generate_image)
        layout.addWidget(self.generate_button)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.error_label = QLabel(self)
        self.error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_label)

        self.progress = QProgressBar(self)
        self.progress.setRange(0, 0)
        self.progress.hide()
        layout.addWidget(self.progress)

        self.download_button = QPushButton("Download Image", self)
        self.download_button.clicked.connect(self.download_image)
        self.download_button.hide()  # Hide the download button initially
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def generate_image(self):
        self.progress.show()
        api_key = self.api_key_entry.text()
        prompt_text = self.prompt_entry.text()

        self.thread = ImageGenerationThread(api_key, prompt_text)
        self.thread.finished.connect(self.on_image_generated)
        self.thread.error.connect(self.on_image_error)
        self.thread.start()

    def on_image_generated(self, img_data):
        pixmap = QPixmap()
        pixmap.loadFromData(img_data)
        self.image_label.setPixmap(pixmap.scaled(self.width() * 0.75, self.height() * 0.75, Qt.KeepAspectRatio))
        self.progress.hide()
        self.download_button.show()  # Show the download button when the image is loaded
        self.image_data = img_data  # Save the image data for downloading

    def on_image_error(self, error_message):
        self.error_label.setText(f"Error: {error_message}")
        self.progress.hide()

    def download_image(self):
        if hasattr(self, 'image_data'):
            default_dir = os.path.expanduser('~/Downloads')
            default_filename = f"generated_image_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            save_path, _ = QFileDialog.getSaveFileName(self, 'Save Image', 
                                                       os.path.join(default_dir, default_filename), 
                                                       'Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)')
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(self.image_data)

def main():
    app = QApplication(sys.argv)
    ex = DalleGenerator()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
