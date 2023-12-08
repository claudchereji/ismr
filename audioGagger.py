import subprocess
import os
import json
from pydub import AudioSegment

def is_cussword(word):
    # List of cusswords
    cusswords = ['arse', 'arsehead', 'arsehole', 'ass', 'asshole', 'bastard', 'bitch', 
                 'bloody', 'bollocks', 'brotherfucker', 'bugger', 'bullshit', 'child-fucker', 
                 'Christ on a bike', 'Christ on a cracker', 'cock', 'cocksucker', 'crap', 'cunt', 
                 'damn', 'damn it', 'dick', 'dickhead', 'dyke', 'fatherfucker', 'frigger', 'fuck', 
                 'fucker', 'goddamn', 'godsdamn', 'hell', 'holy-shit', "holy hell", 'horseshit', 
                 'shit', 'Jesus Christ', 'Jesus H. Christ', 'Jesus Harold  Christ', 
                 'Jesus Mary and Joseph', 'kike', 'motherfucker', 'Nigga', 'nigga', "nigga's", 'niggas','nigra', 'piss', 
                 'prick', 'pussy', 'Shitty', 'shitty', 'shity', 'ass', 'shite', 'sisterfucker', 'slut', 
                 'son of a bitch', 'son of a whore', 'sweet Jesus', 'twat', 'wanker', 
                 "bullshit", "fucking", "fuckin", "asshole", "bullshit", "whore", "Fuck You", "Shit", "Piss off", 
                 "Dick head", "Asshole", "Son of a bitch", "Bastard", "Bitch", "Damn", "Dumb",	
                 "Bimbo", "Piss",	"Jerk",	"Stupid", "Wimp", "Lame", "Idiot", "Fool", "Retard",	
                 "Loser",	"Pain in the Neck", "Rubbish",	"Shag",	"Wanker", "Taking a Piss", "Twat", 
                 "Bollocks",	"Bugger",	"Choad",	"Crikey",	"Bloody Hell", "Bloody Oaf", 
                 "Root", "Get Stuffed", "Bugger Me", "Crazy", "Creepy", "Clown", "Weird"]
    # Check if the word is in the list of cusswords
    return word in cusswords

# Replace "examples/sample01.wav" with the actual path to your WAV file
input_audio_file = "input.mp3"

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
    print("JSON file already exists. Skipping subprocess.")

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

            # Load the insert audio segment
            insert_audio = AudioSegment.from_file("censor.mp3")

            # Convert the start and end times to milliseconds
            word_start_ms = int((word_start + total_duration_change) * 1000)
            word_end_ms = int((word_end + total_duration_change) * 1000)

            # Slice the original audio into three segments
            before_cussword = audio[:word_start_ms]
            cussword = audio[word_start_ms:word_end_ms]
            after_cussword = audio[word_end_ms:]

            # Replace the cussword segment with the insert audio
            audio = before_cussword + insert_audio + after_cussword

            # Update the total duration change
            total_duration_change += len(insert_audio) / 1000 - (word_end - word_start)

# Export the new audio file
audio.export("output_audio.mp3", format="mp3")
