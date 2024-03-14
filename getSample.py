from openai import OpenAI


def getVoiceSample(voice, file_text):

    try:

        client = OpenAI()
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=file_text
        )

        # Naming the output file based on the original file path, but with .mp3 extension
        output_file_path = f"samples/{voice}.mp3"
        print(f"getting {output_file_path} sound")

        # Saving the audio to a file
        response.stream_to_file(output_file_path)
        print(f"Generated speech saved to {output_file_path}")
    except Exception as e:
        print(f"Failed to generate speech for {output_file_path}: {e}")


voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
text = "In the silent city, a single rose bloomed on concrete, proof of nature's persistence amidst human abandonment. Hope sprouted anew."

for voice in voices:
    getVoiceSample(voice, text)
