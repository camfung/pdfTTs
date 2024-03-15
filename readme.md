# PDF to MP3 Converter

## Introduction
This project provides a comprehensive solution for converting PDF documents into MP3 audio files. Utilizing Python, the script transforms text contained within a PDF into spoken word, enabling users to listen to the content of documents. This tool is particularly beneficial for those seeking an auditory learning experience or for anyone looking to consume written content on-the-go.

## How It Works
The process involves several key steps:
1. **PDF to Text Conversion:** The script extracts text from the PDF document using the PyMuPDF library.
2. **Text Chunking:** To facilitate efficient audio conversion, the text is split into manageable chunks, ensuring that each segment does not exceed a predefined character limit.
3. **Text to Speech Conversion:** Each text chunk is then converted to speech using the OpenAI API, producing individual MP3 files.
4. **MP3 Stitching:** Finally, these MP3 files are concatenated into a single MP3 file, creating a continuous audio version of the original PDF document.

## How to Use
To use this tool, follow these steps:
1. Ensure that Python is installed on your system.
2. Install the required Python packages by running `pip install -r requirements.txt`.
3. Place the PDF document you wish to convert in an accessible directory.
4. Add your open ai api key into the .env file
5. Run the program follow the GUI 

## Limitations
- **Language and Voice:** The current implementation uses a single voice model. Variations in language or accent preferences are not supported.
- **Document Formatting:** Complex PDF layouts or documents containing non-text elements (e.g., images, tables) may not be accurately converted.
- **Character Limit:** There is a maximum character limit for each text chunk. Extremely large documents may require significant processing time.

## Use Cases
This tool is ideal for:
- **Learning and Accessibility:** Providing an alternative means for consuming written material, supporting different learning styles and those with visual impairments.
- **Multitasking:** Allowing users to listen to documents while performing other tasks, maximizing productivity.
- **Language Learning:** Assisting in language acquisition by enabling learners to hear the pronunciation of text.

## Conclusion
The PDF to MP3 Converter is a versatile tool designed to bridge the gap between written content and auditory consumption. It leverages powerful libraries and APIs to deliver a seamless conversion process, making it an invaluable asset for educational, professional, and personal use.
