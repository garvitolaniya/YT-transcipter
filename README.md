# YouTube Transcriber

A web application to extract and display YouTube video transcripts in a user-friendly way, with automatic language handling for Hindi and English.

## Features
- Extracts transcripts from YouTube videos using a URL
- Splits transcripts into 35-second time-based chunks
- Displays both full transcript and chunked views
- Automatically shows Hindi transcript if the video is in Hindi, otherwise translates and shows in English
- Search and highlight within the transcript
- Font size adjustment for readability
- Modern, responsive web interface

## Requirements
- Python 3.8+
- pip

### Python Packages
- youtube-transcript-api
- googletrans
- yt-dlp
- flask
- python-dotenv

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## Installation & Setup
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

## Usage
1. Enter a YouTube video URL in the input box.
2. Click "Get Transcript".
3. View the transcript in both full and time-based chunked formats.
4. Use the search box to find and highlight text in the transcript.
5. Adjust font size for better readability.

## Language Handling Logic
- If the video transcript is originally in **Hindi**, the transcript is shown in Hindi by default.
- If the video transcript is in **any other language**, it is automatically translated and shown in English.
- There is no manual language selection in the UI; this logic is automatic.

## Troubleshooting
- **No transcript found:** Some videos may not have transcripts available, or may be region-locked or private.
- **Google Translate errors:** If translation fails, the original text will be shown.
- **Dependencies not installed:** Make sure to run `pip install -r requirements.txt` before starting the app.
- **Port already in use:** If port 5000 is busy, stop other apps or change the port in `youtube_transcriber.py`.

## Project Structure
```
├── youtube_transcriber.py         # Main Flask app and backend logic
├── requirements.txt              # Python dependencies
├── templates/
│   ├── index.html                # Main web interface
│   └── transcript_partial.html   # AJAX transcript partial
└── README.md                     # This file
```

## License
MIT License

---

**Enjoy fast, language-smart YouTube transcribing!** 