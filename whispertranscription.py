import openai
from pydub import AudioSegment

# Load the audio file
song = AudioSegment.from_mp3("input_audio.mp3")

# Split the audio file into 10-minute segments
ten_minutes = 10 * 60 * 1000
segments = [song[i:i+ten_minutes] for i in range(0, len(song), ten_minutes)]

# Transcribe each segment using the OpenAI API
openai.api_key = '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'

with open("transcriptions.txt", "w") as f:
    for i, segment in enumerate(segments):
        # Export the segment as an MP3 file
        segment.export(f"segment{i}.mp3", format="mp3")
        
        # Transcribe the segment using the OpenAI API
        with open(f"segment{i}.mp3", "rb") as file:
            transcription = openai.Audio.transcribe("whisper-1", file)
            
            # Write the transcription to the text file
            f.write(f"Segment {i+1}:\n{transcription}\n\n")
