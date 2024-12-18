import sys
import os
import json
from deepgram import DeepgramClient, PrerecordedOptions
from pydub import AudioSegment
import time
import argparse

# Configure DeepGram
DEEPGRAM_API_KEY = '613ed3d56c772f2f197adbe532f9bdb82a4b4a06'

def is_cussword(word):
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
    return word in cusswords

def process_audio(input_file, output_dir='output', censor_file='censor.mp3'):
    print(f"\nProcessing: {input_file}")
    start_time = time.time()

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize Deepgram
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    # Get transcription
    print("Transcribing audio...")
    with open(input_file, 'rb') as audio:
        payload = { 'buffer': audio }
        options = PrerecordedOptions(
            smart_format=True,
            model="nova-2",
            language="en-US"
        )
        
        response = deepgram.listen.prerecorded.v('1').transcribe_file(payload, options)

    # Load the audio files
    try:
        audio = AudioSegment.from_file(input_file)
        censor_sound = AudioSegment.from_file(censor_file)
    except Exception as e:
        print(f"Error loading audio files: {e}")
        return

    print("Censoring offensive language...")
    total_duration_change = 0
    censor_count = 0

    # Process each word in the transcription
    for word_data in response.results.channels[0].alternatives[0].words:
        if is_cussword(word_data.word):
            censor_count += 1
            word_start = float(word_data.start)
            word_end = float(word_data.end)
            
            # Convert times to milliseconds
            word_start_ms = int((word_start + total_duration_change) * 1000)
            word_end_ms = int((word_end + total_duration_change) * 1000)
            
            # Slice the audio
            before_cussword = audio[:word_start_ms]
            after_cussword = audio[word_end_ms:]
            
            # Prepare censor sound
            censor_duration = word_end_ms - word_start_ms
            insert_audio = censor_sound[:censor_duration]
            
            # Combine audio segments
            audio = before_cussword + insert_audio + after_cussword
            
            # Update timing
            total_duration_change += (censor_duration - len(insert_audio)) / 1000

    # Generate output filename
    output_filename = os.path.join(output_dir, 
                                 f"{os.path.splitext(os.path.basename(input_file))[0]}_censored.mp3")
    
    # Export censored audio
    print(f"Exporting censored audio to: {output_filename}")
    audio.export(output_filename, format="mp3")
    
    # Show statistics
    elapsed_time = (time.time() - start_time) / 60
    print(f"\nProcess completed:")
    print(f"- Words censored: {censor_count}")
    print(f"- Processing time: {elapsed_time:.2f} minutes")
    print(f"- Output saved to: {output_filename}")

def main():
    parser = argparse.ArgumentParser(description='Audio censoring tool using Deepgram')
    parser.add_argument('input_file', help='Path to input audio file')
    parser.add_argument('--output-dir', default='output',
                      help='Output directory (default: ./output)')
    parser.add_argument('--censor-sound', default='censor.mp3',
                      help='Path to censor sound file (default: ./censor.mp3)')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found")
        return
    
    if not os.path.exists(args.censor_sound):
        print(f"Error: Censor sound file '{args.censor_sound}' not found")
        return

    process_audio(args.input_file, args.output_dir, args.censor_sound)

if __name__ == '__main__':
    main()