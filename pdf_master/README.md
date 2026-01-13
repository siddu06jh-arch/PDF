# PDF Master Converter

PDF Master is a Flask web application that allows users to upload PDF files and convert them into various formats, including Word documents, plain text, and images. The application provides a simple user interface for file uploads and downloads.

## Features

- Upload PDF files for conversion.
- Convert PDFs to Word documents (.docx).
- Extract text from PDFs and save it as plain text (.txt).
- Convert PDF pages to images and download them as a ZIP file.

## Project Structure

```
pdf_master
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── .gitignore              # Files and directories to ignore by Git
├── README.md               # Project documentation
├── uploads                 # Temporary storage for uploaded PDFs
├── outputs                 # Storage for converted output files
├── templates               # HTML templates
│   └── index.html         # User interface template
├── static                  # Static files (CSS, JS)
│   ├── css
│   │   └── styles.css      # CSS styles
│   └── js
│       └── main.js         # JavaScript code
├── tests                   # Unit tests
│   └── test_app.py         # Tests for the application
└── Dockerfile              # Instructions for building a Docker image
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pdf_master
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your web browser and navigate to `http://localhost:10000` to access the application.

## Usage

1. Upload a PDF file using the provided form.
2. Select the desired output format (Word, text, or images).
3. Click the "Convert" button to process the file.
4. Download the converted file once the processing is complete.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.