# DALL-E 3 Image Generator

Generate stunning images directly from your desktop with the DALL-E 3 Image Generator. This Python-based application leverages the powerful OpenAI's DALL-E 3 model through a user-friendly graphical interface built with PyQt5. Simply input your prompt, and let the magic of AI bring your imagination to life.

## Features

- **Simple and Intuitive GUI**: Easy-to-navigate graphical user interface for seamless operation.
- **Asynchronous Image Generation**: Utilizes background processing to keep the application responsive.
- **Real-time Progress Feedback**: Includes a progress bar to indicate the image generation process.
- **High-quality Image Output**: Generates 1024x1024 resolution images based on your textual prompt.
- **Image Download**: Save the generated images to your local system with a click.

## Prerequisites

- Python 3.x
- PyQt5
- OpenAI API Key

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install the required Python packages:

```bash
pip install PyQt5 requests openai
```

3. Clone this repository or download the `main.py` file to your local machine.

## Usage

1. Launch the application by running:

```bash
python main.py
```

2. Enter your OpenAI API Key and your desired prompt in the respective fields.
3. Click the "Generate Image" button to start the process.
4. Once the image is generated, it will be displayed within the application window. You have the option to download the image by clicking the "Download Image" button.

## Customization

Feel free to dive into the code to customize the application to your liking. The `main.py` script is well-commented to help you understand and modify the functionality.

## License

This project is open-source and available under the MIT License.
