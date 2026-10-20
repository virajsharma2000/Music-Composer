import streamlit as st
import soundfile as sf
import numpy as np
import requests
import json

st.title('AI powered pianoist')
st.header('Generate piano music without musician')

music_description = st.text_input('Enter music description:')
duration = st.text_input('Enter duration(in mins):')
file_name = st.text_input('Enter file name:')

syntax = "[{'frequency':frequency, 'decay_rate':decay_rate, 'initial-amplitude':amplitude, 'secs':time_in_secs}]. Give the json removing all the unnecessary explaination. The music must be returned in exact syntax without any replacement. The and decay rate of each should be medium and noticable. If the music requested is in rap, the decay should be high"
api_key = st.secrets['API_KEY']

if st.button('Compose Music'):
 system_prompt = f'Create a music tone in json of {music_description}, the syntax should be {syntax}. The duration of the music should be atleast {duration} minutes'
 payload = {"contents":[{"parts":[{"text":system_prompt}]}]}

 response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}", json = payload)
 gemini_response = response.json()['candidates'][0]['content']['parts'][0]['text']

 music = json.loads(gemini_response.replace('```', '').replace('json', ''))
 music_waveform = []

 for note in music:
  A = note["initial-amplitude"]
  k = note['decay_rate']
  t = note['secs']
  f = note['frequency']
 
  t = np.linspace(0, t, int(t * 44100))

  amplitude_envolope = A * np.exp(-k * t)
  sine_wave = np.sin(2 * np.pi * f * t)

  sound = amplitude_envolope * sine_wave 
 
  music_waveform.append(sound)

 music_waveform = np.concatenate(music_waveform)

 sf.write(f'{file_name}.mp3', music_waveform, 44100)
 
 with open(f'{file_name}.mp3', 'rb') as f:
  bytes_ = f.read()

 st.download_button(label = "Download Composed Music", file_name = f"{file_name}.mp3", data = bytes_, mime = 'audio/mpeg')