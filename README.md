# Audio Gagger

Audio Gagger is a Python script that takes an input audio file, identifies and extracts segments containing offensive language, and replaces those segments with a censor beep sound. This tool utilizes the [WhisperX](https://github.com/example/whisperx) library for audio transcription and manipulation, as well as the [PyDub](https://github.com/jiaaro/pydub) library for audio processing.

## Prerequisites

Before using Audio Gagger, ensure you have the following dependencies installed:

- [WhisperX](https://github.com/example/whisperx) library
- [PyDub](https://github.com/jiaaro/pydub) library

You can install the required libraries using the following commands:

```bash
pip install whisperx pydub
```

## Usage

1. Replace the placeholder audio file (`input.mp3`) with the path to your desired audio file.
2. Set the output directory by modifying the `output_directory` variable.
3. Replace the `censor.mp3` file with your preferred censor beep sound.

```python
# Replace "input.mp3" with the actual path to your audio file
input_audio_file = "path/to/your/audio/file.mp3"

# Replace "output_directory" with the desired directory for the output JSON file
output_directory = "/path/to/output/directory"

# Replace "censor.mp3" with your censor beep sound file
insert_audio = AudioSegment.from_file("path/to/censor/beep.mp3")
```

4. Run the script:

```bash
python audio_gagger.py
```

The script will transcribe the audio using WhisperX, identify offensive language segments, and replace them with the censor beep sound. The output audio will be saved as `output_audio.mp3` in the specified output directory.

**Note:** Make sure to adjust the list of cusswords in the code to match your specific use case.
