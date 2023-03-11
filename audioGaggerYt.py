import json
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
import subprocess
import os 


# Set the URL of the video
url = input('\n\nEnter the url of the video that you want a transcript from: \n\n')

# Specify the download directory
download_dir = '.'

# Make sure the download directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Download the audio in mp3 format
audio_file = os.path.join(download_dir, 'audio.mp3')
subprocess.run(['yt-dlp', '--extract-audio', '--audio-format', 'mp3', '-o', audio_file, url])

# Load the MP3 audio file
mp3_file = AudioSegment.from_file("audio.mp3", format="mp3")

# Load the audio file
audio = AudioSegment.from_file("audio.mp3")

# Check the number of channels
channels = audio.channels
if channels == 1:
    # Convert to stereo
    audio = audio.set_channels(2)

# Export the audio file as FLAC
audio.export("audio.flac", format="flac")

audio_file = AudioSegment.from_file("audio.flac", format="flac")
audio_file = audio_file.set_frame_rate(16000)
audio_file.export("audio1.flac", format="flac")

# Run the gsutil command to copy the local file to the GCS bucket
subprocess.run(["gsutil", "cp", "audio1.flac", "gs://flac-file/"])

cusswords = ['arse', 'arsehead', 'arsehole', 'ass', 'asshole', 'bastard', 'bitch', 
             'bloody', 'bollocks', 'brotherfucker', 'bugger', 'bullshit', 'child-fucker', 
             'Christ on a bike', 'Christ on a cracker', 'cock', 'cocksucker', 'crap', 'cunt', 
             'damn', 'damn it', 'dick', 'dickhead', 'dyke', 'fatherfucker', 'frigger', 'fuck', 
             'fucker', 'goddamn', 'godsdamn', 'hell', 'holy-shit', "holy hell", 'horseshit', 
             'shit', 'Jesus Christ', 'Jesus H. Christ', 'Jesus Harold  Christ', 
             'Jesus Mary and Joseph', 'kike', 'motherfucker', 'nigga', 'nigra', 'piss', 
             'prick', 'pussy', 'shitty', 'shity', 'ass', 'shite', 'sisterfucker', 'slut', 
             'son of a bitch', 'son of a whore', 'sweet Jesus', 'twat', 'wanker', 
             "bullshit", "fucking", "asshole", "bullshit", "whore", "Fuck You", "Shit", "Piss off", 
             "Dick head", "Asshole", "Son of a bitch", "Bastard", "Bitch", "Damn", "Dumb",	
             "Bimbo", "Piss",	"Jerk",	"Stupid", "Wimp", "Lame", "Idiot", "Fool", "Retard",	
             "Loser",	"Pain in the Neck", "Rubbish",	"Shag",	"Wanker", "Taking a Piss", "Twat", 
             "Bollocks",	"Bugger",	"Choad",	"Crikey",	"Bloody Hell", "Bloody Oaf", 
             "Root", "Get Stuffed", "Bugger Me", "Crazy", "Creepy", "Clown", "Weird"]


client = speech.SpeechClient()

# Set the URI of the audio file in Google Cloud Storage
uri = "gs://flac-file/audio1.flac"

# Create a RecognitionAudio object with the URI
audio = speech.RecognitionAudio(uri=uri)

# Set the RecognitionConfig
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
    sample_rate_hertz=16000,
    audio_channel_count=2,
    language_code="en-US",
    enable_word_time_offsets=True,
)

# Use LongRunningRecognize to transcribe the audio file
operation = client.long_running_recognize(config=config, audio=audio)

# Wait for the operation to complete and get the response
response = operation.result(timeout=500)

# Create a list to store the word info for each word in the response
word_info_list = []

# Loop through each result in the response
for result in response.results:
    # Loop through each word_info in the alternative's words list
    for word in result.alternatives[0].words:
        # Calculate the start and end times in nanoseconds
        start_time = int(word.start_time.total_seconds() * 10**9)
        end_time = int(word.end_time.total_seconds() * 10**9)
        
        # Create a dictionary to store the word info
        word_info = {
            "word": word.word,
            "start_time": start_time,
            "end_time": end_time
        }
        
        # Append the word info dictionary to the word_info_list
        word_info_list.append(word_info)
        # inside the for loop that filters the word_info_list to only include cusswords
        if word.word in cusswords:
            print(f"{word} is a cussword")
        else:
            continue


# Create a dictionary to store the entire transcript and the word info list
transcript_dict = {
    #"transcript": response.results[0].alternatives[0].transcript,
    "word_info_list": word_info_list
}

# Convert the dictionary to a JSON string
transcript_json = json.dumps(transcript_dict)

# Write the response to a JSON file
with open("response.json", "w") as f:
    json.dump(transcript_dict, f)

# read the JSON file and parse it into a dictionary
with open("response.json") as f:
    response_dict = json.load(f)

# filter the word_info_list to only include cusswords
cussword_info_list = []
for word_info in response_dict["word_info_list"]:
    if word_info["word"] in cusswords:
        cussword_info_list.append(word_info)

# Load the audio file
audio = AudioSegment.from_file("audio.mp3")

# iterate over the filtered cussword info list
time_codes = []
for word_info in cussword_info_list:
    start_t_code = word_info["start_time"]
    end_t_code = word_info["end_time"]

    start_t_ms = start_t_code // 1000000
    end_t_ms = end_t_code // 1000000

    # Convert time codes to seconds
    start_time_sec = start_t_ms / 1000
    end_time_sec = end_t_ms / 1000

    # Append the time codes as a tuple to the list
    time_codes.append((start_time_sec, end_time_sec))

# Loop over the time codes and replace the segments with the new audio
for start_time, end_time in time_codes:
    # Define the audio file you want to insert
    insert_audio = AudioSegment.from_file("insert_audio.mp3")

    # Replace the segment with the new audio
    audio = audio[:start_time * 1000] + insert_audio + audio[end_time * 1000:]
    # inside the for loop that replaces audio segments
        # Print the segment start time, end time, and insert audio duration
    print(f"Replacing audio segment from {start_time} to {end_time}")


# Export the new audio file
audio.export("output_audio.mp3", format="mp3")
