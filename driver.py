import os
import fitz  # Import the PyMuPDF library

# Drafting the initial version of the code to split a text file into smaller files of 4000 characters without splitting words.


def split_text_file_into_chunks(file_path, max_chars=4000):
    """
    Splits the content of a text file into smaller files each containing up to max_chars characters without splitting words.

    Args:
    - file_path (str): The path to the input text file.
    - max_chars (int): Maximum number of characters for each smaller file. Default is 4000.

    Returns:
    - None: Creates smaller files in the same directory as the input file.
    """
    # Initialize variables
    chunk = []  # Temporarily holds words for the current chunk
    chunk_size = 0  # Current size of the chunk
    file_counter = 1  # Counter for the output file names

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

# Note: Calls to the function and any additional code needed to fully test and use this function will be added after further discussion and refinement.


def pdf_to_text(pdf_path, txt_path):
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


# Example usage
pdf_path = "/AiTextch7-3.pdf"
txt_path = "output.txt"  # Specify the path where you want to save the text file
pdf_to_text(pdf_path, txt_path)
split_text_file_into_chunks(txt_path)
