import joblib
import os
import argparse
from train_model import preprocess_text

def predict_spam(message):
    model_path = 'models/spam_model.pkl'
    vectorizer_path = 'models/vectorizer.pkl'

    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        print("Error: Model or vectorizer not found. Please run train_model.py first.")
        return

    # Load model and vectorizer
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    # Preprocess the message
    clean_message = preprocess_text(message)

    # Vectorize
    features = vectorizer.transform([clean_message])

    # Predict
    prediction = model.predict(features)[0]

    result = "Spam" if prediction == 1 else "Not Spam (Ham)"
    print(f"\nMessage: '{message}'")
    print(f"Prediction: **{result}**\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Predict if a message is spam.")
    parser.add_argument("message", type=str, help="The message/email text to classify.")
    args = parser.parse_args()

    predict_spam(args.message)
