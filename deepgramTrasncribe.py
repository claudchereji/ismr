from deepgram import DeepgramClient, PrerecordedOptions 
 
DEEPGRAM_API_KEY = '37f0a705356f79682f2c0e6248c9eda75073a457' 
 
AUDIO_URL = { 
  'url': 'https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav' 
} 
 
def main(): 
  try: 
    deepgram = DeepgramClient(DEEPGRAM_API_KEY) 
 
    options = PrerecordedOptions(
      model="nova-2", 
      language="en", 
      smart_format=True, 
      punctuate=False, 
    ) 
 
    response = deepgram.listen.prerecorded.v('1').transcribe_url(AUDIO_URL, options) 
    print(response) 
 
  except Exception as e: 
    print(f'Exception: {e}') 
 
if __name__ == '__main__': 
  main()