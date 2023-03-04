from pydub import AudioSegment
from time_codes import time_codes

# Load the audio file
audio = AudioSegment.from_file("input_audio.mp3")

# Loop over the time codes and replace the segments with the new audio
for start_time, end_time in time_codes:
    # Define the audio file you want to insert
    insert_audio = AudioSegment.from_file("insert_audio.mp3")

    # Replace the segment with the new audio
    audio = audio[:start_time] + insert_audio + audio[end_time:]

# Export the new audio file
audio.export("output_audio.mp3", format="mp3")
