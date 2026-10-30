
import streamlit as st
import soundfile as sf
import numpy as np
import requests
import json
 
st.set_page_config(page_title='AI Pianist', page_icon='🎹', layout='centered')
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
 
html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }
 
/* Animated aurora background */
.stApp {
    background:
        radial-gradient(900px 500px at 10% -10%, rgba(124, 58, 237, 0.35), transparent 60%),
        radial-gradient(800px 500px at 100% 0%, rgba(14, 165, 233, 0.28), transparent 60%),
        radial-gradient(700px 600px at 50% 110%, rgba(236, 72, 153, 0.22), transparent 60%),
        #0a0a14;
    color: #e8e8f3;
}
 
/* Hide default Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { padding-top: 2.5rem; max-width: 760px; }
 
/* Hero */
.hero { text-align: center; margin-bottom: 2rem; }
.badge {
    display: inline-block; padding: 6px 14px; border-radius: 999px;
    font-size: 0.78rem; font-weight: 600; letter-spacing: .04em;
    color: #c4b5fd; background: rgba(124, 58, 237, 0.15);
    border: 1px solid rgba(167, 139, 250, 0.35);
}
.hero h1 {
    font-size: 3.2rem; font-weight: 800; line-height: 1.1; margin: 1rem 0 .6rem 0;
    background: linear-gradient(90deg, #a78bfa 0%, #38bdf8 50%, #f472b6 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { color: #9a9ab5; font-size: 1.05rem; font-weight: 400; margin: 0; }
 
/* Piano keys decoration */
.keys { display: flex; justify-content: center; gap: 4px; margin: 1.6rem 0 0.4rem 0; height: 54px; }
.key { width: 26px; border-radius: 0 0 7px 7px; background: linear-gradient(#f5f5ff, #c9c9e0);
       box-shadow: 0 6px 16px rgba(0,0,0,.4); animation: press 3.2s ease-in-out infinite; }
.key.black { width: 16px; height: 62%; margin: 0 -14px; z-index: 2; background: linear-gradient(#2a2a3d, #0b0b14);
             border-radius: 0 0 5px 5px; animation: none; }
.key:nth-child(3n) { animation-delay: .4s; } .key:nth-child(4n) { animation-delay: 1.1s; } .key:nth-child(5n) { animation-delay: 1.8s; }
@keyframes press { 0%,100% { transform: translateY(0); } 50% { transform: translateY(3px); filter: brightness(.88); } }
 
/* Glass card (the main form container) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.045) !important;
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
    border-radius: 22px !important;
    backdrop-filter: blur(18px);
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.45);
    padding: 0.6rem 0.8rem;
}
 
/* Inputs */
label, .stTextInput label p { color: #c9c9e3 !important; font-weight: 600 !important; font-size: .88rem !important; }
.stTextInput input {
    background: rgba(10, 10, 20, 0.7) !important; color: #f1f1fb !important;
    border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 12px !important;
    padding: 0.8rem 1rem !important; transition: all .2s ease;
}
.stTextInput input::placeholder { color: #6b6b88 !important; }
.stTextInput input:focus {
    border-color: #a78bfa !important; box-shadow: 0 0 0 3px rgba(167,139,250,.25) !important;
}
.stTextInput [data-baseweb="input"], .stTextInput [data-baseweb="base-input"] { background: transparent !important; border: none !important; }
 
/* Buttons */
.stButton > button, .stDownloadButton > button {
    width: 100%; border: none; border-radius: 14px; padding: 0.85rem 1.2rem;
    font-weight: 700; font-size: 1rem; color: white;
    background: linear-gradient(90deg, #7c3aed, #0ea5e9);
    box-shadow: 0 10px 28px rgba(124, 58, 237, 0.4);
    transition: transform .15s ease, box-shadow .15s ease, filter .15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px); filter: brightness(1.1);
    box-shadow: 0 14px 34px rgba(14, 165, 233, 0.45); color: white; border: none;
}
.stButton > button:active, .stDownloadButton > button:active { transform: translateY(0); }
.stDownloadButton > button { background: linear-gradient(90deg, #ec4899, #8b5cf6); box-shadow: 0 10px 28px rgba(236,72,153,.35); }
 
/* Result card + audio */
.result-title { font-weight: 700; font-size: 1.1rem; color: #f1f1fb; margin: 1.4rem 0 .6rem 0; }
audio { width: 100%; border-radius: 12px; filter: invert(.92) hue-rotate(200deg) saturate(1.2); }
 
/* Spinner / alerts */
.stSpinner > div { color: #c4b5fd !important; }
.footer-note { text-align: center; color: #5f5f7a; font-size: .8rem; margin-top: 2.2rem; }
</style>
""", unsafe_allow_html=True)
 
st.markdown("""
<div class="hero">
    <span class="badge">✨ POWERED BY GEMINI</span>
    <h1>AI Pianist</h1>
    <p>Describe a mood, a style, a moment — and get piano music composed in seconds.</p>
    <div class="keys">
        <div class="key"></div><div class="key"></div><div class="key black"></div>
        <div class="key"></div><div class="key black"></div><div class="key"></div>
        <div class="key"></div><div class="key black"></div><div class="key"></div>
        <div class="key black"></div><div class="key"></div><div class="key"></div>
    </div>
</div>
""", unsafe_allow_html=True)
 
syntax = "[{'frequency':frequency, 'decay_rate':decay_rate, 'initial-amplitude':amplitude, 'secs':time_in_secs}]. Give the json removing all the unnecessary explaination. The music must be returned in exact syntax without any replacement. The and decay rate of each should be medium and noticable. If the music requested is in rap, the decay should be high"
api_key = st.secrets['API_KEY']
 
with st.container(border=True):
    music_description = st.text_input('🎼  Music description', placeholder='e.g. a calm, rainy-evening lullaby in C major')
 
    col1, col2 = st.columns(2)
    with col1:
        duration = st.text_input('⏱️  Duration (in mins)', placeholder='e.g. 1')
    with col2:
        file_name = st.text_input('📁  File name', placeholder='e.g. rainy_evening')
 
    compose = st.button('🎹  Compose Music')
 
# ----------------------------- BACKEND (unchanged logic) -----------------------------
if compose:
    with st.spinner('The pianist is composing your piece…'):
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
 
    st.success('Your composition is ready!', icon='🎶')
    with st.container(border=True):
        st.markdown('<div class="result-title">▶️  Preview your track</div>', unsafe_allow_html=True)
        st.audio(bytes_, format='audio/mpeg')
        st.download_button(label = "⬇️  Download Composed Music", file_name = f"{file_name}.mp3", data = bytes_, mime = 'audio/mpeg')
 
st.markdown('<div class="footer-note">Made with Streamlit · Compositions are AI-generated</div>', unsafe_allow_html=True)
