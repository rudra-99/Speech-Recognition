import requests
from api_secrets import API_KEY_ASSEMBLYAI
import time

#uploading the audio file

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcipt_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {'authorization': API_KEY_ASSEMBLYAI}

def upload(filename):
    def read_file(filename, chunk_size = 5242880):
        with open(filename,'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data    
    response = requests.post(upload_endpoint, headers=headers,data=read_file(filename))
    audio_url = response.json()['upload_url']
    return audio_url

#Transcribing
def transcribe(audio_url):
    json = {"audio_url": audio_url}
    response = requests.post(transcipt_endpoint, json=json,headers=headers)
    job_id = response.json()['id']
    return job_id

def poll(transcript_id):
    polling_endpoint = transcipt_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()

def get_transcription_result(audio_url):
    transcript_id = transcribe(audio_url)
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data['error'], 'error'
        print('Waiting 30 seconds ....')
        time.sleep(30)

def save_transcript(audio_url, filename):
    data,error = get_transcription_result(audio_url)
    if error:
        print('ERROR!! ',error)
    else:
        print('########### TRANSCRIPTION RESULT ##########')
        print()
        print(data['text'])
        text_file = filename + ".txt"
        with open(text_file, "w") as f: f.write(data['text'])
        print()
        print("Transcription is Saved Successfully!!!")

