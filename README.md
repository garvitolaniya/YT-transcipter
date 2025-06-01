# 🎥 YouTube Transcriber

A web application to extract and display YouTube video transcripts in a user-friendly way, with automatic language handling for Hindi and English.

## 🚀 Features
🔗 Extract transcripts from any YouTube video via URL

⏱️ Split transcripts into 35-second chunks for better readability

🌐 Detects Hindi transcripts automatically or translates to English if needed

🔍 Search and highlight specific words/phrases in the transcript

🔠 Adjustable font size for enhanced readability

💻 Responsive, clean web UI (Flask-based)

## 📦 Requirements
- Python 3.8+
- pip

### 🐍 Python Dependencies
- youtube-transcript-api
- googletrans
- yt-dlp
- flask
- python-dotenv

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## ⚙️ Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   python youtube_transcriber.py
   ```
4. **Open your browser and go to:**
   [http://localhost:5000](http://localhost:5000)

## 🧑‍💻 How to Use
    1. Enter a YouTube video URL in the input box.
    2. Click "Get Transcript".
    3. View the transcript in both full and time-based chunked formats.
    4. Use the search box to find and highlight text in the transcript.
    5. Adjust font size for better readability.

## 🌍 Language Handling Logic
- If the video transcript is originally in **Hindi**, the transcript is shown in Hindi by default.
- If the video transcript is in **any other language**, it is automatically translated and shown in English.
- There is no manual language selection in the UI; this logic is automatic.

## 🛠️ Troubleshooting
| Issue                       | Solution                                                             |
| --------------------------- | -------------------------------------------------------------------- |
| ❌ No transcript found       | Video might be private, region-locked, or transcript is unavailable. |
| 🌐 Translation failed       | Fallback: untranslated text will be displayed.                       |
| 📦 Missing dependencies     | Run `pip install -r requirements.txt` again.                         |
| 🔌 Port 5000 already in use | Stop other services or change the port in `youtube_transcriber.py`.  |


## 📁 Project Structure
```
├── youtube_transcriber.py         # Main Flask app and backend logic
├── requirements.txt              # Python dependencies
├── templates/
│   ├── index.html                # Main web interface
│   └── transcript_partial.html   # AJAX transcript partial
└── README.md                     # This file
```

## 📄 License
MIT License

---

**🔍🎉 Watch less, understand more.
🪄 Let our transcriber do the magic — fast, intelligent, and language-aware!** 
