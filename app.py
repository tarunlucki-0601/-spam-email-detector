import streamlit as st
import joblib
import os
import string
import nltk
from nltk.corpus import stopwords

# Ensure NLTK stopwords are downloaded silently
nltk.download('stopwords', quiet=True)

# Set page configuration
st.set_page_config(page_title="Spam Detector", page_icon="✉️", layout="centered")

# Copy of the preprocessing function from train_model.py
def preprocess_text(text):
    text = text.lower()
    text = "".join([char for char in text if char not in string.punctuation])
    stop_words = set(stopwords.words('english'))
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

@st.cache_resource
def load_model_components():
    model_path = 'models/spam_model.pkl'
    vectorizer_path = 'models/vectorizer.pkl'
    
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        return model, vectorizer
    else:
        return None, None

# Load the model
model, vectorizer = load_model_components()

# UI Layout
st.title("✉️ Spam Email Detector")
st.write("Paste an email or message below to check if it's spam or legitimate (ham).")

if model is None or vectorizer is None:
    st.error("Model files not found! Please run `python train_model.py` first to generate the models.")
    st.stop()

# Text input
user_input = st.text_area("Message Content", height=150, placeholder="Type or paste your message here...")

# Analyze button
if st.button("Analyze Message", type="primary"):
    if user_input.strip() == "":
        st.warning("Please enter a message to analyze.")
    else:
        with st.spinner("Analyzing..."):
            # Process and predict
            clean_text = preprocess_text(user_input)
            features = vectorizer.transform([clean_text])
            prediction = model.predict(features)[0]
            
            # Display results
            if prediction == 1:
                st.error("🚨 **SPAM DETECTED** 🚨")
                st.write("This message looks highly suspicious.")
            else:
                st.success("✅ **NOT SPAM (HAM)** ✅")
                st.write("This message appears to be safe.")
