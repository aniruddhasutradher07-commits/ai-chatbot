# AI-Powered Chatbot

An intelligent chatbot built for customer support and FAQ handling, using NLP for understanding user queries beyond simple keyword matching.

## Features

- **NLP-based understanding** — Uses NLTK for tokenization and stopword removal, so it understands full sentences, not just exact keywords
- **9 FAQ categories** — Covers orders, refunds, cancellations, shipping, payments, account issues, complaints, and contact info
- **Web chat interface** — Clean, responsive chat UI with typing indicator
- **Conversation logging** — All chats are stored in a SQLite database for review
- **REST API** — `/chat` endpoint for sending messages, `/logs` endpoint for viewing history

## Tech Stack

- **Backend:** Python, Flask
- **NLP:** NLTK (tokenization, stopword removal)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript

## Setup Instructions

1. Clone the repository:
```bash
   git clone https://github.com/aniruddhasutradher07-commits/ai-chatbot
   cd ai-chatbot
```

2. Create and activate a virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Download NLTK data (run in a Python shell):
```python
   import nltk
   nltk.download('punkt_tab')
   nltk.download('stopwords')
```

5. Run the app:
```bash
   python app.py
```

6. Open your browser at `http://127.0.0.1:5000`

## Future Improvements

- Integrate Transformer-based models (e.g., Hugging Face) for deeper contextual understanding
- Add user authentication for personalized chat history
- Deploy to a cloud platform for public access

## Author

Aniruddha Sutradhar
