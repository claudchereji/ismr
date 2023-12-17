

import subprocess
import os
import json
from pydub import AudioSegment
import time
import tkinter as tk
from tkinter import filedialog
import os
from moviepy.editor import VideoFileClip, AudioFileClip
from tkinter import ttk


# Record the start time
start_time = time.time()

def is_cussword(word):
    # List of cusswords
    cusswords = ['arse', 'arsehead', 'arsehole', 'ass', 'asshole', 'bastard', 'bastards', 'bitch', 'bitch.', 'bitch,', 
                 'bloody', 'bollocks', 'brotherfucker', 'Fuck', 'bugger', 'bullshit', 
                 "shit's", "Shit's", 'shit,', 'shit.', 'Shit,', 'Shit.' 'child-fucker', 
                 'Christ on a bike', 'dipshit', 'Dipshit', 'shitter', 'shitter,', 'shitter.', 'dipshit.', 
                 'Dipshit.', 'dipshit,', 'Dipshit,', 'cock', 'cocksucker', 'crap', 'cunt', 
                 'damn', 'damn it', 'dick', 'dickhead', 'dyke', 'fatherfucker', 'frigger', 'fuck', 
                 'fucker', 'goddamn', 'godsdamn', 'hell', 'holy-shit', "holy-hell", 'horseshit', 
                 'shit', 'Jesus Christ', 'Jesus H. Christ', 'Jesus Harold  Christ', 
                 'Jesus Mary and Joseph', 'dicks','Dicks', 'kike', 'motherfucker', 'Nigga', 'nigga', "nigga's", 'niggas','nigra', 'piss', 
                 'prick', 'pussy', 'Shitty', 'shitty', 'shity', 'ass', 'shite', 'sisterfucker', 'slut', "shit.",
                 'son of a bitch', "shitty,", 'son of a whore', 'sweet Jesus', 'twat', 'wanker', 
                 "bullshit", "fucking", "Fucking","fucking,", "fuckin", "fuckin,", "asshole", "shit?","asshole,", 
                 "asshole.", "bullshit", "bullshit,", "bullshit.", "whore", "whore,", 
                 "Fuck", "whore.", "Fuck You", "Fuck You.", "Fuck You,", "Shit", "Piss off", 
                 "Dick head", "Asshole", "Son of a bitch", "Bastard", 'Bastards', "Bitch", 'big-ass', 'big-ass,', 
                 'big-ass.', 'Big-ass', 'Big-ass,', 'Big-ass.', "Damn", "Dumb",	
                 "Bimbo", "Piss",	"Jerk",	"Stupid", "Wimp", "Lame", "Idiot", "Fool", "Retard",	
                 "Loser",	"Pain in the Neck", "Rubbish",	"Shag",	"Wanker", "Taking a Piss", "Twat", 
                 ]
    # Check if the word is in the list of cusswords
    return word in cusswords



# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Prompt the user to select audio or video
choice = tk.messagebox.askquestion("Audio or Video", "Do you want to process a video file?")

if choice == 'no':
    # Prompt the user to select an audio file
    input_audio_file = filedialog.askopenfilename(title="Select Audio File", filetypes=(("Audio Files", "*.mp3"), ("All Files", "*.*")))

    # Check if the user selected a file
    if input_audio_file:
        print(f"\n\nSelected audio file: {input_audio_file}\n\n")
    else:
        print("No audio file selected.")

    # Replace "output_directory" with the desired directory for the output JSON file
    output_directory = "/home/claud/Desktop/audio gagger"

    # Check if the JSON file already exists
    json_file_path = os.path.join(output_directory, f"{os.path.splitext(input_audio_file)[0]}.json")
    if not os.path.exists(json_file_path):
        # Construct the command
        command = ["whisperx", input_audio_file, "--compute_type", "int8", "--output_format", "json", "--output_dir", output_directory]

        # Run the command
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
    else:
        print("JSON file already exists. Skipping subprocess.\n\n")

    # Load the JSON file
    with open("input.json", "r") as json_file:
        data = json.load(json_file)

    # Extract the cussword segments and corresponding time codes
    cussword_segments = data["segments"]

    # Create a list to store time codes
    cussword_time_codes = []

    # Load the JSON data
    with open('input.json') as f:
        data = json.load(f)

    # Load the audio file
    audio = AudioSegment.from_file(input_audio_file)

    # Initialize the total duration change
    total_duration_change = 0

    print("Censoring cusswords...\n\n")

    # Replace cusswords with an insert audio segment
    for segment in data["segments"]:
        segment_start = segment["start"]
        segment_end = segment["end"]

        for word_info in segment["words"]:
            if 'start' not in word_info:
                continue  # Skip this word if it doesn't have a 'start' key

            word = word_info["word"]
            word_start = word_info["start"]
            word_end = word_info["end"]

            if is_cussword(word):
                # Append the time codes as a tuple
                cussword_time_codes.append((word_start, word_end))
                # print(f"I found a cussword between {word_start} and {word_end} seconds")

                # Load the insert audio segment
                insert_audio = AudioSegment.from_file("censor.mp3")

                # Convert the start and end times to milliseconds
                word_start_ms = int((word_start + total_duration_change) * 1000)
                word_end_ms = int((word_end + total_duration_change) * 1000)

                # Slice the original audio into three segments
                before_cussword = audio[:word_start_ms]
                cussword = audio[word_start_ms:word_end_ms]
                after_cussword = audio[word_end_ms:]

                # Update the total duration change
                def split_insert_audio(total_duration_change, insert_audio, split_time, cussword_duration_ms):
                    # Convert the split time and cussword duration to milliseconds
                    split_time_ms = int(split_time * 1000)
                    cussword_duration_ms = int(word_end_ms - word_start_ms)

                    # Trim the insert audio to match the cussword duration
                    insert_audio = insert_audio[:cussword_duration_ms]

                    # Update the total duration change
                    total_duration_change += (cussword_duration_ms - len(insert_audio)) / 1000

                    return total_duration_change, insert_audio

                # Define the missing variables
                split_time = 0.5  # Replace with the desired split time
                cussword_duration_ms = int(word_end_ms - word_start_ms)

                # Replace the cussword segment with the insert audio
                total_duration_change, insert_audio = split_insert_audio(total_duration_change, insert_audio, split_time, cussword_duration_ms)
                audio = before_cussword + insert_audio + after_cussword

    # Get the name of the input audio file
    input_audio_filename = os.path.basename(input_audio_file)

    # Remove the file extension
    input_audio_filename = os.path.splitext(input_audio_filename)[0]

    # Export the new audio file with the same name as the input audio file
    output_audio_filename = f"{input_audio_filename}_censored.mp3"
    audio.export(output_audio_filename, format="mp3")
    print("Done!\n\n")

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    elapsed_time = elapsed_time / 60

    # Print the result
    print(f"Script took {elapsed_time} minutes to run.")

else:
    # Prompt the user to select a video file
    input_video_file = filedialog.askopenfilename(title="Select Video File", filetypes=(("Video Files", "*.mp4"), ("All Files", "*.*")))

    # Check if the user selected a file
    if input_video_file:
        print(f"\n\nSelected video file: {input_video_file}\n\n")
    else:
        print("No video file selected.")

    # TODO: Add code to process video
    clip1 = VideoFileClip(input_video_file)

    # Get the name of the input video file
    input_video_filename = os.path.basename(input_video_file)

    #Check if an audio file with the same name as the input video file exists
    if os.path.exists(f"{input_video_filename}_audio.mp3"):
        clip1_audio = f"{os.path.splitext(input_video_filename)[0]}.mp4_audio.mp3"
        print("Audio file already exists. Skipping subprocess.\n\n")
    else:
        #Extract audio from video
        clip1_audio = clip1.audio.write_audiofile(f"{input_video_filename}_audio.mp3")

    # Replace "output_directory" with the desired directory for the output JSON file
    output_directory = "/home/claud/Desktop/audio gagger"

    clip1_audio = f"{os.path.splitext(input_video_filename)[0]}.mp4_audio.mp3"

    # Check if a JSON file already exists
    json_file_path = os.path.join(output_directory, f"{os.path.splitext(clip1_audio)[0]}.json")
    if not os.path.exists(json_file_path):
        # Construct the command
        command = ["whisperx", clip1_audio, "--compute_type", "int8", "--output_format", "json", "--output_dir", output_directory]

        # Run the command
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
    else:
        print("JSON file already exists. Skipping subprocess.\n\n")

    # Load the JSON file
    json_file_path = f"{os.path.splitext(clip1_audio)[0]}.json"
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    # Extract the cussword segments and corresponding time codes
    cussword_segments = data["segments"]

    # Create a list to store time codes
    cussword_time_codes = []

    # Load the JSON data
    with open(json_file_path) as f:
        data = json.load(f)

    # Load the audio file
    audio = AudioSegment.from_file(clip1_audio)

    # Initialize the total duration change
    total_duration_change = 0

    print("Censoring cusswords...\n\n")

    # Replace cusswords with an insert audio segment
    for segment in data["segments"]:
        segment_start = segment["start"]
        segment_end = segment["end"]

        for word_info in segment["words"]:
            if 'start' not in word_info:
                continue  # Skip this word if it doesn't have a 'start' key

            word = word_info["word"]
            word_start = word_info["start"]
            word_end = word_info["end"]

            if is_cussword(word):
                # Append the time codes as a tuple
                cussword_time_codes.append((word_start, word_end))
                # print(f"I found a cussword between {word_start} and {word_end} seconds")

                # Load the insert audio segment
                insert_audio = AudioSegment.from_file("censor.mp3")

                # Convert the start and end times to milliseconds
                word_start_ms = int((word_start + total_duration_change) * 1000)
                word_end_ms = int((word_end + total_duration_change) * 1000)

                # Slice the original audio into three segments
                before_cussword = audio[:word_start_ms]
                cussword = audio[word_start_ms:word_end_ms]
                after_cussword = audio[word_end_ms:]

                # Update the total duration change
                def split_insert_audio(total_duration_change, insert_audio, split_time, cussword_duration_ms):
                    # Convert the split time and cussword duration to milliseconds
                    split_time_ms = int(split_time * 1000)
                    cussword_duration_ms = int(word_end_ms - word_start_ms)

                    # Trim the insert audio to match the cussword duration
                    insert_audio = insert_audio[:cussword_duration_ms]

                    # Update the total duration change
                    total_duration_change += (cussword_duration_ms - len(insert_audio)) / 1000

                    return total_duration_change, insert_audio

                # Define the missing variables
                split_time = 0.5  # Replace with the desired split time
                cussword_duration_ms = int(word_end_ms - word_start_ms)

                # Replace the cussword segment with the insert audio
                total_duration_change, insert_audio = split_insert_audio(total_duration_change, insert_audio, split_time, cussword_duration_ms)
                audio = before_cussword + insert_audio + after_cussword


    # Export the new audio file with the same name as the input audio file
output_audio_filename = f"{clip1_audio}_censored.mp3"
audio.export(output_audio_filename, format="mp3")
print("Done censoring your video!\n\n")


audio_final = AudioFileClip(output_audio_filename)

print("Overlaying censored audio now...\n\n")
# Replace clip1 audio with censored audio
clip1 = clip1.set_audio(audio_final)

print("Exporting censored video now...\n\n")
clip1.write_videofile(f"{input_video_filename}_censored.mp4")

    # Record the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

elapsed_time = elapsed_time / 60

# Print the result
print(f"Script took {elapsed_time} minutes to run.")

