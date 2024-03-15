import os
import sys
import fitz  # Import the PyMuPDF library
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment

load_dotenv()


def split_pdf(pdf_path, from_page, to_page):
    """
    Splits a PDF file, creating a new PDF file from a specified range of pages.

    This function opens a PDF file from the given path, extracts a range of pages specified
    by the from_page and to_page parameters, and saves the extracted pages into a new PDF file. 
    The path of the newly created PDF file is then returned.

    Parameters:
    - pdf_path (str): The path to the PDF file to be split.
    - from_page (int): The starting page number for the split (zero-based indexing).
    - to_page (int): The ending page number for the split (zero-based indexing). 
      The page corresponding to this number will be included in the split.

    Returns:
    - str: The path to the newly created PDF file containing the specified page range.

    Raises:
    - Exception: If any error occurs during the opening, splitting, or saving of the PDF file.

    Note:
    The `fitz` module, part of PyMuPDF, is used for handling PDF operations.
    """
    try:
        doc = fitz.open(pdf_path)
        split_doc = fitz.open()
        split_doc.insert_pdf(doc, from_page=from_page, to_page=to_page)

        output_path = "pdfs/temp_split_pdf.pdf"
        split_doc.save(output_path)
        return output_path
    except Exception as e:
        print(e)


def pdf_to_text(pdf_path, txt_path):
    """
    Converts a PDF file to a text file.

    Args:
    - pdf_path (str): The path to the input PDF file.
    - txt_path (str): The path where the output text file will be saved.
    """
    with fitz.open(pdf_path) as doc:
        with open(txt_path, "w") as txt_file:
            for page in doc:
                text = page.get_text()
                txt_file.write(text)


def split_text_file_into_chunks(file_path, max_chars=4000):
    """
    Splits the content of a text file into smaller files each containing up to max_chars characters without splitting words.

    Args:
    - file_path (str): The path to the input text file.
    - max_chars (int): Maximum number of characters for each smaller file. Default is 4000.

    Returns:
    - list: Paths to the generated smaller text files.
    """
    chunk = []
    chunk_size = 0
    file_counter = 1
    output_files = []

    output_dir = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path, 'r') as file:
        for word in file.read().split():
            word_size = len(word) + 1

            if chunk_size + word_size > max_chars:
                output_file_path = os.path.join(
                    output_dir, f"{base_name}_part{file_counter}.txt")
                with open(output_file_path, 'w') as output_file:
                    output_file.write(' '.join(chunk))
                output_files.append(output_file_path)

                chunk = []
                chunk_size = 0
                file_counter += 1

            chunk.append(word)
            chunk_size += word_size

        if chunk:
            output_file_path = os.path.join(
                output_dir, f"{base_name}_part{file_counter}.txt")
            with open(output_file_path, 'w') as output_file:
                output_file.write(' '.join(chunk))
            output_files.append(output_file_path)

    return output_files


def convert_texts_to_speech(file_paths):
    """
    Takes an array of file paths, reads the text from each file, and uses the OpenAI API
    to convert the text to speech, saving each output as a new .mp3 file.

    Args:
    - file_paths (list of str): Paths to the text files to be converted.

    Returns:
    - None
    """
    client = OpenAI()

    mp3_paths = []
    for file_path in file_paths:
        # Read the text from the file
        try:
            with open(file_path, "r") as file:
                file_text = file.read()
        except FileNotFoundError:
            print(f"File {file_path} not found. Skipping.")
            continue

        # Generate speech from the text
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=file_text
            )

            # Naming the output file based on the original file path, but with .mp3 extension
            output_file_path = str(Path(file_path).with_suffix('.mp3'))
            mp3_paths.append(output_file_path)

            # Saving the audio to a file
            response.stream_to_file(output_file_path)
            print(f"Generated speech saved to {output_file_path}")
        except Exception as e:
            print(f"Failed to generate speech for {file_path}: {e}")
    return mp3_paths


def stitch_mp3_files(file_paths, output_file_path):
    """
    Concatenates multiple MP3 files into a single MP3 file.

    Args:
    - file_paths (list of str): Paths to the MP3 files to be concatenated.
    - output_file_path (str): Path where the output MP3 file will be saved.
    """
    combined = AudioSegment.from_mp3(file_paths[0])

    for file_path in file_paths[1:]:
        next_audio = AudioSegment.from_mp3(file_path)
        combined += next_audio

    combined.export(output_file_path, format="mp3")


def gen_audio(pdf_path, output_mp3_path, output_file_name, pdf_from, pdf_to):
    """
    Main function to convert a PDF file to an MP3 file.

    Args:
    - pdf_path (str): Path to the input PDF file.
    - output_mp3_path (str): Path where the output MP3 file will be saved.
    """
    try:
        # split pdf by page
        split_pdf_file_path = split_pdf(pdf_path, pdf_from, pdf_to)
        # Convert PDF to text
        txt_path = split_pdf_file_path.replace('.pdf', '.txt')
        pdf_to_text(split_pdf_file_path, txt_path)

        # Split the text file into chunks
        chunk_files = split_text_file_into_chunks(txt_path)

        # Convert text chunks to speech (MP3)
        mp3_files = convert_texts_to_speech(chunk_files)
        # mp3_files = ["mp3/output_part1.mp3"]

        # Stitch the MP3 files into a single file
        output_file_path = f"{output_mp3_path}/{output_file_name}.mp3"
        stitch_mp3_files(mp3_files, output_file_path)
        return output_file_path
    except Exception as e:
        raise e


def calculate_price_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            num_characters = len(content)
            price_cents = (num_characters / 1000000) * 1500
            return price_cents
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_price(pdf_path, pdf_from, pdf_to):
    """
    Main function to convert a PDF file to an MP3 file.

    Args:
    - pdf_path (str): Path to the input PDF file.
    - output_mp3_path (str): Path where the output MP3 file will be saved.
    """
    try:
        # split pdf by page
        split_pdf_file_path = split_pdf(pdf_path, pdf_from, pdf_to)
        # Convert PDF to text
        txt_path = split_pdf_file_path.replace('.pdf', '.txt')
        pdf_to_text(split_pdf_file_path, txt_path)

        # Split the text file into chunks
        chunk_files = split_text_file_into_chunks(txt_path)
        total_price = 0
        for file in chunk_files:
            with open(file, 'r') as f:
                total_price += calculate_price_from_file(file)

        return total_price
    except Exception as e:
        raise e
