import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QProgressBar, QFileDialog, QDesktopWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from openai import OpenAI
import requests
from datetime import datetime
import os

# This class is a QThread that generates an image using OpenAI's DALL-E 3 model
class ImageGenerationThread(QThread):
    finished = pyqtSignal(bytes)  # Signal emitted when the image generation is finished
    error = pyqtSignal(str)  # Signal emitted when there is an error

    def __init__(self, api_key, prompt_text):
        super().__init__()
        self.api_key = api_key  # OpenAI API key
        self.prompt_text = prompt_text  # Prompt text for the image generation

    def run(self):
        client = OpenAI(api_key=self.api_key)
        try:
            # Generate the image
            response = client.images.generate(
                model="dall-e-3",
                prompt=self.prompt_text,
                size="1024x1024",
                quality="standard",
                n=1
            )
            image_url = response.data[0].url
            img_data = requests.get(image_url).content
            self.finished.emit(img_data)  # Emit the finished signal with the image data
        except Exception as e:
            self.error.emit(str(e))  # Emit the error signal with the error message

# This class is a QWidget that provides the UI for the DALL-E 3 image generator
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

        # Create the API key entry field
        self.api_key_entry = QLineEdit(self)
        self.api_key_entry.setEchoMode(QLineEdit.Password)
        self.api_key_entry.setPlaceholderText("Enter your OpenAI API Key here")
        layout.addWidget(self.api_key_entry)

        # Create the prompt entry field
        self.prompt_entry = QLineEdit(self)
        self.prompt_entry.setPlaceholderText("Enter the prompt for the image generation here")
        layout.addWidget(self.prompt_entry)

        # Create the generate button
        self.generate_button = QPushButton("Generate", self)
        self.generate_button.clicked.connect(self.generate_image)
        layout.addWidget(self.generate_button)

        # Create the image label
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # Create the error label
        self.error_label = QLabel(self)
        self.error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_label)

        # Create the progress bar
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 0)
        self.progress.hide()
        layout.addWidget(self.progress)

        # Create the download button
        self.download_button = QPushButton("Download Image", self)
        self.download_button.clicked.connect(self.download_image)
        self.download_button.hide()  # Hide the download button initially
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    # This method is called when the generate button is clicked
    def generate_image(self):
        self.progress.show()
        api_key = self.api_key_entry.text()
        prompt_text = self.prompt_entry.text()

        # Start the image generation thread
        self.thread = ImageGenerationThread(api_key, prompt_text)
        self.thread.finished.connect(self.on_image_generated)
        self.thread.error.connect(self.on_image_error)
        self.thread.start()

    # This method is called when the image generation is finished
    def on_image_generated(self, img_data):
        pixmap = QPixmap()
        pixmap.loadFromData(img_data)
        self.image_label.setPixmap(pixmap.scaled(self.width() * 0.75, self.height() * 0.75, Qt.KeepAspectRatio))
        self.progress.hide()
        self.download_button.show()  # Show the download button when the image is loaded
        self.image_data = img_data  # Save the image data for downloading

    # This method is called when there is an error in the image generation
    def on_image_error(self, error_message):
        self.error_label.setText(f"Error: {error_message}")
        self.progress.hide()

    # This method is called when the download button is clicked
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