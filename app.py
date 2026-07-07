from flask import Flask, request, jsonify, render_template
import time
import sqlite3
from datetime import datetime
import nltk
import ssl
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt_tab')
nltk.download('stopwords')

app = Flask(__name__)

stop_words = set(stopwords.words("english"))

# FAQ data - keywords list ke saath (ek se zyada keyword bhi ho sakte hain)
faq_data = [
    {"keywords": ["hello", "hi", "hey"], "reply": "Hi there! How can I help you today?"},
    {"keywords": ["bye", "goodbye", "thanks", "thank"], "reply": "You're welcome! Have a great day."},
    {"keywords": ["order", "status", "track", "tracking"], "reply": "Please share your order ID to check the status."},
    {"keywords": ["refund", "money", "back"], "reply": "Refunds are processed within 5-7 business days."},
    {"keywords": ["cancel", "cancellation"], "reply": "You can cancel your order within 24 hours of placing it from the 'My Orders' page."},
    {"keywords": ["shipping", "delivery", "deliver"], "reply": "Standard delivery takes 3-5 business days. Express delivery is available at checkout."},
    {"keywords": ["payment", "pay", "card", "upi"], "reply": "We accept credit/debit cards, UPI, and net banking."},
    {"keywords": ["account", "login", "password", "signup"], "reply": "You can reset your password from the login page using 'Forgot Password'."},
    {"keywords": ["complaint", "issue", "problem", "broken", "damaged"], "reply": "We're sorry for the trouble! Please share your order ID and describe the issue so we can help."},
    {"keywords": ["contact", "email", "support", "human", "agent"], "reply": "You can reach us at support@example.com or call 1800-123-4567."},
]

def clean_message(message):
    tokens = word_tokenize(message.lower())
    # Sirf meaningful words rakho (stopwords hata do)
    words = [w for w in tokens if w.isalpha() and w not in stop_words]
    return words

def get_response(user_message):
    user_words = set(clean_message(user_message))
    best_match = None
    best_score = 0

    for faq in faq_data:
        faq_keywords = set(faq["keywords"])
        matched = user_words & faq_keywords
        if not matched:
            continue
        # Match ka proportion nikaalo (kitne % keywords match hue us FAQ ke)
        score = len(matched) / len(faq_keywords)
        if score > best_score:
            best_score = score
            best_match = faq["reply"]

    if best_match:
        return best_match
    return "Sorry, I didn't understand that. Can you rephrase?"

def init_db():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_reply TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_log(user_message, bot_reply):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_logs (user_message, bot_reply, timestamp) VALUES (?, ?, ?)",
        (user_message, bot_reply, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = get_response(user_message) 
    time.sleep(1)
    save_log(user_message, reply)
    return jsonify({"reply": reply})

@app.route("/logs", methods=["GET"])
def get_logs():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    logs = [
        {"id": r[0], "user_message": r[1], "bot_reply": r[2], "timestamp": r[3]}
        for r in rows
    ]
    return jsonify(logs)

@app.route("/")
def home():
    return render_template("index.html")

init_db()

if __name__ == "__main__":
    app.run(debug=True)