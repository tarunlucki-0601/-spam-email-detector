import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

# Ensure NLTK stopwords are downloaded
nltk.download('stopwords', quiet=True)

def preprocess_text(text):
    """
    Lowercase text, remove punctuation and stopwords.
    """
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = "".join([char for char in text if char not in string.punctuation])
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

def train_and_save_model():
    data_path = 'data/SMSSpamCollection'
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}. Please run download_data.py first.")
        return

    print("Loading data...")
    # The dataset is tab-separated, with columns for label and message
    df = pd.read_csv(data_path, sep='\t', header=None, names=['label', 'message'])

    print("Preprocessing text...")
    df['clean_message'] = df['message'].apply(preprocess_text)
    
    # Map labels to binary values (spam: 1, ham: 0)
    df['label_num'] = df['label'].map({'ham': 0, 'spam': 1})

    X = df['clean_message']
    y = df['label_num']

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Extracting features using TF-IDF...")
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    print("Training Naive Bayes Model...")
    model = MultinomialNB()
    model.fit(X_train_tfidf, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test_tfidf)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.4f}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Ham', 'Spam']))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("Saving model and vectorizer...")
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/spam_model.pkl')
    joblib.dump(vectorizer, 'models/vectorizer.pkl')
    print("Model saved to 'models/' directory.")

if __name__ == '__main__':
    train_and_save_model()
