from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os

# Assume the OpenAI client and dotenv are already correctly set up and configured


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

            # Saving the audio to a file
            response.stream_to_file(output_file_path)
            print(f"Generated speech saved to {output_file_path}")
        except Exception as e:
            print(f"Failed to generate speech for {file_path}: {e}")


def main():
    file_paths = [
        "output_part2.txt",
        "output_part3.txt"
    ]
    convert_texts_to_speech(file_paths)


if __name__ == "__main__":
    main()
