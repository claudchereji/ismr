# Audio Transcription and Explicit Language Detection using Google Cloud Speech-to-Text API

## Overview

This script leverages the Google Cloud Speech-to-Text API to perform audio transcription while also identifying and timestamping instances of explicit language within the transcription. The result is stored in a JSON file that contains the transcription with corresponding time codes for explicit language. Additionally, the script replaces segments of the audio file containing explicit language with a cleaner version of the audio.

## How it Works

### Dependencies

This script requires several Python libraries, including `json`, `pydub`, and `google.cloud.speech_v1p1beta1`.

### Audio Processing

1. The script begins by loading an audio file in MP3 format.
2. It checks the number of audio channels and converts mono audio to stereo if necessary.
3. The audio is exported as FLAC format with a 16000 Hz frame rate.
4. The FLAC file is then uploaded to a Google Cloud Storage bucket.

### Transcription

1. The Google Cloud Speech-to-Text API is configured to recognize FLAC encoding, a 16000 Hz sample rate, two audio channels, and American English language. Word time offsets are enabled.
2. The API transcribes the audio file, providing a response that is parsed into a list of dictionaries containing information about each word in the transcription.

### Explicit Language Detection

1. The script filters the word info list to include only instances of explicit language.
2. A new list is created with time codes for each instance of explicit language.

### Audio Replacement

1. The original audio file is loaded.
2. Segments of the audio containing explicit language are replaced with cleaner audio.
3. The new audio is exported, with time codes used to identify segments with explicit language.

## Google Speech-to-Text API

This script utilizes Google's Speech-to-Text API, which requires access to a Google Cloud Storage bucket for operation.

## Known Issues

- There is a syncing issue where the overlayed sound effect may not line up perfectly with every instance of explicit language. This may be attributed to a limitation in the Google Cloud API's time accuracy.
- While the script is functional, further updates and improvements are planned to enhance its performance.

Thank you for using this audio transcription and explicit language detection tool. We welcome any contributions and feedback to help make this script even better.
