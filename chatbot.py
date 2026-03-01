import nltk
import json
import random
import string
from nltk.tokenize import word_tokenize

nltk.download('punkt', quiet=True)

# Load JSON data
with open("qa_data.json", "r") as f:
    qa_data = json.load(f)

# Store user preferred language (memory)
user_language = None

# ---------------------------
# Text preprocessing
# ---------------------------
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    return tokens


# ---------------------------
# Simple language detection
# ---------------------------
def detect_language(text):
    hinglish_keywords = [
        "kya", "tum", "naam", "kaise", "hai",
        "kitne", "saal", "mera", "aap"
    ]
    text = text.lower()
    for word in hinglish_keywords:
        if word in text:
            return "hinglish"
    return "english"


# ---------------------------
# Get chatbot response
# ---------------------------
def get_response(user_input):
    global user_language

    # Detect language if not set
    if user_language is None:
        user_language = detect_language(user_input)

    user_tokens = set(preprocess(user_input))

    best_score = 0
    best_item = None

    for item in qa_data:
        for pattern in item["patterns"]:
            pattern_tokens = set(preprocess(pattern))
            common_words = user_tokens & pattern_tokens
            score = len(common_words)

            if score > best_score:
                best_score = score
                best_item = item

    if best_score >=1 and best_item is not None:

        if user_language == "hinglish":
            responses = best_item.get("responses_hinglish", best_item.get("responses_english", []))
        else:
            responses = best_item.get("responses_english", best_item.get("responses_hinglish", []))

        if responses:
            return random.choice(responses)
        else:
            return "Response not available."

    else:
        if user_language == "hinglish":
            return random.choice([
                "Samajh nahi aaya 😅",
                "Thoda clearly pucho 😄",
                "Mujhe samajhne me dikkat ho rahi hai."
            ])
        else:
            return random.choice([
                "Sorry, I didn't understand that.",
                "Could you rephrase that?"
            ])


# ---------------------------
# Main chatbot loop
# ---------------------------
def run_chatbot():
    global user_language

    print("=" * 50)
    print("     Hi, Night Owl 🦉")
    print("     Type 'quit' to exit")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["quit", "exit", "bye", "phone rakh"]:
            if user_language == "hinglish":
                print("Bot: Bye! Phir milte hain 👋")
            else:
                print("Bot: Goodbye! Have a great day 👋")
            break

        if not user_input:
            print("Bot: Please type something!")
            continue

        response = get_response(user_input)
        print("Bot:", response)


# Run chatbot
if __name__ == "__main__":
    run_chatbot()