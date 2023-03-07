# AudioGagger
Get gagged... voluntarily

![Project logo](https://raw.githubusercontent.com/claudchereji/AudioGagger/main/IMG_0037.PNG](https://raw.githubusercontent.com/claudchereji/AudioGagger/main/IMG_0037_500x500.png)

## Explain the code
This is a script that performs audio transcription using Google Cloud Speech-to-Text API and identifies cuss words in the transcription. It then creates a JSON file with the transcription and time codes for cuss words, and replaces the segments containing cuss words in the audio file with new audio.

The code imports the required libraries, such as json, pydub, and google.cloud.speech_v1p1beta1. It then loads an audio file in MP3 format, checks the number of channels, converts the audio to stereo if it is a mono file, exports the audio file as FLAC, sets the frame rate to 16000 Hz, and exports it again as FLAC. The FLAC file is then uploaded to a Google Cloud Storage bucket.

The Google Cloud Speech-to-Text API is used to transcribe the audio file. The API is set up to recognize FLAC encoding, a sample rate of 16000 Hz, two audio channels, and American English language. The API is also set up to enable word time offsets. The response from the API is then parsed to create a list of dictionaries with information about each word in the transcription.

Next, the script filters the word info list to only include cusswords, and creates a new list with the time codes for each cussword. The script then loads the original audio file, replaces the segments with cusswords with a new audio file, and exports the new audio file. The time codes are used to identify the segments that contain cusswords.



## Google Speech-to-text
This speech to text model uses Googles speech to text api which means... you guessed it! you will need a google cloud bucket for it to work.
until I can find a way to spin up a cloud instance or get whisper working to work on your local machine, this is what it is. 

## But does it even work?
YES! check out the example audio and the result audio to see whats up. currently, I'm suffering from a syncing issue where the overlayed sound effect doesn't line up with every cussword and i feel like thats a google problem. i feel like the time accuracy is not as great as I hoped. it could also be a problem with my code which is the best possibility.

## Will there be updates to the code? 
you bet your a$$ there will!


[example audio](https://raw.githubusercontent.com/claudchereji/AudioGagger/main/example.mp3)


[Result audio](https://raw.githubusercontent.com/claudchereji/AudioGagger/main/result.mp3)
