# 🌾 உழவன் குரல் — Uzhavan Kural
### Tamil Farmer AI Assistant

A full-stack AI-powered voice assistant for Tamil farmers.
Speak a question in Tamil → AI answers in Tamil → Hear the answer!

---

## 🔄 How It Works (Pipeline)

```
🎙 Farmer speaks Tamil
        ↓
  Web Speech API (STT)
        ↓
  LLaMA: Translate Tamil → English  (internal)
        ↓
  LLaMA: Answer farming question in English
        ↓
  LLaMA: Translate English answer → Tamil  (internal)
        ↓
  gTTS: Tamil text → MP3 audio
        ↓
🔊 Farmer hears Tamil answer
```

---

## ⚙️ Setup (Run these commands)

### 1. Install Ollama + LLaMA model
```bash
# Install Ollama from https://ollama.com
ollama pull llama3
ollama serve
```

### 2. Install Python gTTS
```bash
pip install gTTS
```

### 3. Install Node dependencies
```bash
npm install
```

### 4. Start the app
```bash
npm start
```

### 5. Open in Chrome
```
http://localhost:3001
```

> ⚠️ Must use **Google Chrome** for Tamil voice recognition

---

## 📁 Project Structure
```
uzhavan-kural/
├── server.js          ← Express backend + AI pipeline
├── package.json
├── requirements.txt   ← Python: gTTS
├── public/
│   └── index.html     ← Full frontend
├── audio_output/      ← Generated MP3s (auto-created)
└── history.json       ← Saved Q&A history (auto-created)
```

## API Endpoints
| Method | Route              | Description                    |
|--------|--------------------|--------------------------------|
| GET    | /                  | Web app                        |
| GET    | /health            | Server + Ollama status         |
| POST   | /api/ask           | Tamil Q → AI → Tamil Answer + Audio |
| GET    | /api/history       | Get history                    |
| POST   | /api/history/save  | Save history                   |
