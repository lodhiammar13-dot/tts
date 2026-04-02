import streamlit as st
import asyncio
import edge_tts

st.set_page_config(page_title="TTS App", layout="centered")

st.title("🔊 Text to Speech Web App (Edge TTS)")

# Some popular Edge TTS voices
voices = {
    "Male (US)": "en-US-GuyNeural",
    "Female (US)": "en-US-JennyNeural",
    "Male (UK)": "en-GB-RyanNeural",
    "Female (UK)": "en-GB-SoniaNeural",
    "Indian Female": "en-IN-NeerjaNeural",
    "Indian Male": "en-IN-PrabhatNeural"
}

# Voice selection
selected_voice_name = st.selectbox("Select Voice", list(voices.keys()))
selected_voice = voices[selected_voice_name]

# Text input
text_input = st.text_area("Enter text to convert to speech")

# Async function to generate audio bytes
async def generate_audio(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    audio_bytes = b""

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]

    return audio_bytes

# Button
if st.button("Convert to Speech"):
    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        audio_data = asyncio.run(generate_audio(text_input, selected_voice))

        st.success("Audio generated!")

        # Play audio directly (no file saving)
        st.audio(audio_data, format="audio/mp3")