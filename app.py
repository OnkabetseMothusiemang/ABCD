import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import openai  # Use Groq API if preferred
from textblob import TextBlob

# Set OpenAI API Key
openai.api_key = "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"  # Replace with your OpenAI/Groq API key

st.title("🧠 Hey Friend!!")

# Function to analyze sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Returns a value from -1 to 1

# Function to generate AI response
def get_ai_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Change model as needed
        messages=[{"role": "system", "content": "You are a supportive AI psychologist."},
                  {"role": "user", "content": user_input}]
    )
    return response['choices'][0]['message']['content']

# Function for text-to-speech
def speak_text(text):
    tts = gTTS(text)
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")  
    tts.save(temp_audio.name)
    st.audio(temp_audio.name, format="audio/mp3")
    temp_audio.close()

# Function to handle voice input
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Speak now...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand your speech."
        except sr.RequestError:
            return "Sorry, there was an error with the speech recognition service."

# Choose input type
input_method = st.radio("How do you want to talk?", ["Type", "Voice"])

user_text = ""  # Initialize variable to store user input

if input_method == "Type":
    user_text = st.text_area("Tell me what's on your mind...")
else:
    if st.button("🎤 Record Voice Note"):
        user_text = voice_input()
        st.write(f"🗣️ You said: {user_text}")

# Submit button to process input
if st.button("📝 Submit"):
    if user_text.strip():  # Ensure there's text input
        sentiment_score = analyze_sentiment(user_text)
        if sentiment_score < -0.2:
            mood_response = "💙 I sense you're feeling a bit down. Let's talk about it."
        elif sentiment_score > 0.2:
            mood_response = "😊 You sound positive! I'm happy to hear that."
        else:
            mood_response = "🤔 I sense neutral emotions. Tell me more."

        st.write(mood_response)

        # Get AI advice
        advice = get_ai_response(user_text)
        st.subheader("AI's Advice:")
        st.write(advice)

        # AI Responds with voice automatically
        full_response = mood_response + " " + advice  # Combine mood and advice
        speak_text(full_response)  # 🔊 AI will talk automatically!
    else:
        st.warning("⚠️ Please enter text or record a voice note before submitting.")
