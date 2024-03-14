from pydub import AudioSegment


def stitch_mp3_files(file_paths, output_file_path):
    # Load the first MP3 file
    combined = AudioSegment.from_mp3(file_paths[0])

    # Concatenate the rest of the MP3 files
    for file_path in file_paths[1:]:
        next_audio = AudioSegment.from_mp3(file_path)
        combined += next_audio

    # Export the combined audio to a new file
    combined.export(output_file_path, format="mp3")


file_paths = [f"mp3/output_part{num}.mp3" for num in range(1, 4)]
output_file_path = 'AiTextch7-1.mp3'
stitch_mp3_files(file_paths, output_file_path)
