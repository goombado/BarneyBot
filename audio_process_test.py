import os
import requests
import time
import subprocess
import json


wit_token = 'huh'
url = 'https://api.wit.ai/speech?v=20200716'
header = {
    'Authorization': f'Bearer {wit_token}',
    'Content-Type': 'audio/wav'
}

channel_id = input('channel id: ')
user_id = input('user id: ')
 

subprocess.Popen(['node', 'barney_voice_helper.js', '-c', channel_id, '-u', user_id])

i = 1
base_path = os.path.join(f'user_audio_recordings', f'{user_id}')


while True:
    while True:
        try:
            complete = open(f'{base_path}/completed/completed_{i}', 'r')
            complete.close()
            break
        except:
            continue
    try:
        file_name = f'{user_id}_{i}'
        subprocess.call(['ffmpeg', '-f', 's16le', '-ar', '96.0k', '-ac', '1', '-i', f'{base_path}\\recordings\\{file_name}', f'{base_path}\\converted\\{file_name}.wav'])
        f = open(f'{base_path}/converted/{file_name}.wav', 'rb')
        data = f.read()
        resp = requests.post(url, data=data, headers=header) #wit_client.speech(f, {'Content-Type': 'audio/wav'})
        print('\n\n\n')
        print(json.loads(resp.text)["text"])
        print('\n\n\n')
        os.remove(f'{base_path}/completed/completed_{i}')
        os.remove(f'{base_path}/recordings/{file_name}')
        os.remove(f'{base_path}/converted/{file_name}.wav')
        i += 1
    except:
        i += 1