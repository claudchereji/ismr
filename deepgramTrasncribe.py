from deepgram import DeepgramClient, PrerecordedOptions

# The API key we created in step 3
DEEPGRAM_API_KEY = '613ed3d56c772f2f197adbe532f9bdb82a4b4a06'

# Replace with your file path
PATH_TO_FILE = '/Users/claudiuchereji/Documents/ismr/ismr/Napoleon Hill - Interview with the devil.mp3'

def main():
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    with open(PATH_TO_FILE, 'rb') as buffer_data:
        payload = { 'buffer': buffer_data }

        options = PrerecordedOptions(
            smart_format=True, model="nova-2", language="en-US"
        )

        response = deepgram.listen.prerecorded.v('1').transcribe_file(payload, options)
        print(response.to_json(indent=4))

if __name__ == '__main__':
    main()