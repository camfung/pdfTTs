import os
import sys
import fitz  # Import the PyMuPDF library
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment

# Assuming the OpenAI setup and dotenv are correctly configured
# Load environment variables for OpenAI API
load_dotenv()

# Function to convert PDF to text


def split_pdf(pdf_path, from_page, to_page):
    try:
        doc = fitz.open(pdf_path)
        split_doc = fitz.open()
        split_doc.insert_pdf(doc, from_page=from_page, to_page=to_page)
        output_path = "pdfs/temppdf.pdf"
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
    # Open the PDF file
    with fitz.open(pdf_path) as doc:
        # Open the text file for writing
        with open(txt_path, "w") as txt_file:
            # Iterate through each page of the PDF
            for page in doc:
                # Extract text from the current page
                text = page.get_text()
                # Write the extracted text to the text file
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
    # Initialize variables
    chunk = []  # Temporarily holds words for the current chunk
    chunk_size = 0  # Current size of the chunk
    file_counter = 1  # Counter for the output file names
    output_files = []  # Store paths of the output files

    # Define the directory and base name for the output files
    output_dir = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path, 'r') as file:
        for word in file.read().split():
            # Adding 1 for the space that will join the words
            word_size = len(word) + 1

            # Check if adding this word exceeds the max_chars limit
            if chunk_size + word_size > max_chars:
                # Save the current chunk to a file
                output_file_path = os.path.join(
                    output_dir, f"{base_name}_part{file_counter}.txt")
                with open(output_file_path, 'w') as output_file:
                    output_file.write(' '.join(chunk))
                output_files.append(output_file_path)

                # Reset the chunk and increment the file counter
                chunk = []
                chunk_size = 0
                file_counter += 1

            # Add the word to the chunk and update the chunk size
            chunk.append(word)
            chunk_size += word_size

        # Save the last chunk if there are any words left
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
    # Load the first MP3 file
    combined = AudioSegment.from_mp3(file_paths[0])

    # Concatenate the rest of the MP3 files
    for file_path in file_paths[1:]:
        next_audio = AudioSegment.from_mp3(file_path)
        combined += next_audio

    # Export the combined audio to a new file
    combined.export(output_file_path, format="mp3")

# Main function to orchestrate the PDF to MP3 conversion process


def main(pdf_path, output_mp3_path):
    """
    Main function to convert a PDF file to an MP3 file.

    Args:
    - pdf_path (str): Path to the input PDF file.
    - output_mp3_path (str): Path where the output MP3 file will be saved.
    """
    # Convert PDF to text
    txt_path = pdf_path.replace('.pdf', '.txt')
    pdf_to_text(pdf_path, txt_path)

    # Split the text file into chunks
    chunk_files = split_text_file_into_chunks(txt_path)

    # Convert text chunks to speech (MP3)
    mp3_files = convert_texts_to_speech(chunk_files)

    # Stitch the MP3 files into a single file
    stitch_mp3_files(mp3_files, output_mp3_path)

    print(f"Conversion complete. The MP3 file is saved at {output_mp3_path}")


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
