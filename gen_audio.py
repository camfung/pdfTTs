from main import convert_texts_to_speech, pdf_to_text, split_pdf, split_text_file_into_chunks, stitch_mp3_files


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
