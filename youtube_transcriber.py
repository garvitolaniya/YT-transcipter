from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
import yt_dlp
import re
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, render_template_string
import os
import random
import requests
from urllib.parse import parse_qs, urlparse

app = Flask(__name__)

class YouTubeTranscriber:
    def __init__(self):
        self.translator = Translator()
        # List of common user agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        
        # Configure yt-dlp options
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'format': 'best',
            'user_agent': random.choice(self.user_agents),
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'no_color': True,
            'geo_bypass': True,
            'geo_verification_proxy': None,
            'socket_timeout': 30,
            'retries': 10,
        }

    def get_video_info_direct(self, video_id):
        """Get video information directly from YouTube."""
        try:
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
            
            # First try to get video info from oEmbed API
            oembed_url = f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json'
            response = requests.get(oembed_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return {
                    'title': data.get('title', 'Unknown Title'),
                    'duration': 0,  # oEmbed doesn't provide duration
                    'id': video_id
                }
            
            return None
        except Exception as e:
            print(f"Error in direct video info fetch: {str(e)}")
            return None
        
    def get_video_info(self, url):
        """Get video information using multiple methods."""
        try:
            # Extract video ID
            video_id = self.extract_video_id(url)
            if not video_id:
                return None

            # Try direct method first
            info = self.get_video_info_direct(video_id)
            if info:
                return info

            # Fallback to yt-dlp
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    return {
                        'title': info.get('title', 'Unknown Title'),
                        'duration': info.get('duration', 0),
                        'id': info.get('id', '')
                    }
        except Exception as e:
            print(f"Error getting video info: {str(e)}")
            return None

    def format_timestamp(self, seconds):
        """Convert seconds to HH:MM:SS format."""
        return str(timedelta(seconds=int(seconds)))

    def format_chunk_text(self, chunk):
        """Format a single chunk with timestamp and text."""
        start_time = self.format_timestamp(chunk['start_time'])
        end_time = self.format_timestamp(chunk['end_time'])
        return f"[{start_time} - {end_time}]\n{chunk['text']}\n"

    def save_readable_transcript(self, result, base_filename):
        """Save transcript in a human-readable format."""
        text_filename = f"{base_filename}.txt"
        
        with open(text_filename, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"Video Title: {result['video_title']}\n")
            f.write(f"Video URL: {result['video_url']}\n")
            f.write(f"Duration: {self.format_timestamp(result['duration'])}\n")
            f.write(f"Number of chunks: {len(result['chunks'])}\n")
            f.write("=" * 80 + "\n\n")
            
            # Write chunks
            for chunk in result['chunks']:
                f.write(self.format_chunk_text(chunk))
                f.write("-" * 80 + "\n\n")
        
        return text_filename

    def extract_video_id(self, url):
        """Extract video ID from YouTube URL."""
        try:
            if 'youtu.be' in url:
                return url.split('/')[-1].split('?')[0]
            elif 'youtube.com' in url:
                parsed_url = urlparse(url)
                if parsed_url.path == '/watch':
                    return parse_qs(parsed_url.query)['v'][0]
                elif parsed_url.path.startswith('/embed/'):
                    return parsed_url.path.split('/')[2]
                elif parsed_url.path.startswith('/v/'):
                    return parsed_url.path.split('/')[2]
            return None
        except Exception as e:
            print(f"Error extracting video ID: {str(e)}")
            return None

    def get_transcript(self, video_id):
        """Get transcript for the video."""
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            # List of all possible language codes
            all_language_codes = [
                'en', 'fr', 'de', 'es', 'it', 'pt', 'ru', 'ja', 'ko', 'zh',
                'ab', 'aa', 'af', 'ak', 'sq', 'am', 'ar', 'hy', 'as', 'ay', 'az', 'bn', 'ba', 'eu', 'be', 'bho', 'bs', 'br', 'bg', 'my', 'ca', 'ceb', 'zh-Hans', 'zh-Hant', 'co', 'hr', 'cs', 'da', 'dv', 'nl', 'dz', 'eo', 'et', 'ee', 'fo', 'fj', 'fil', 'fi', 'gaa', 'gl', 'lg', 'ka', 'gn', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'iu', 'ga', 'jv', 'kl', 'kn', 'kk', 'kha', 'km', 'rw', 'kri', 'ku', 'ky', 'lo', 'la', 'lv', 'ln', 'lt', 'lua', 'luo', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'gv', 'mi', 'mr', 'mn', 'mfe', 'ne', 'new', 'nso', 'no', 'ny', 'oc', 'or', 'om', 'os', 'pam', 'ps', 'fa', 'pl', 'pt-PT', 'pa', 'qu', 'ro', 'rn', 'sm', 'sg', 'sa', 'gd', 'sr', 'crs', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'st', 'su', 'sw', 'ss', 'sv', 'tg', 'ta', 'tt', 'te', 'th', 'bo', 'ti', 'to', 'ts', 'tn', 'tum', 'tr', 'tk', 'uk', 'ur', 'ug', 'uz', 've', 'vi', 'war', 'cy', 'fy', 'wo', 'xh', 'yi', 'yo', 'zu'
            ]
            # Log available languages for debugging
            print(f"Available transcripts for video {video_id}:")
            for t in transcript_list:
                print(f" - {t.language_code} ({t.language}) [generated={t.is_generated}]")
            try:
                # Try to get English transcript first
                transcript = transcript_list.find_transcript(['en'])
            except Exception:
                try:
                    # Try all possible language codes (manual)
                    transcript = transcript_list.find_transcript(all_language_codes)
                except Exception:
                    try:
                        # Try all possible language codes (auto-generated)
                        transcript = transcript_list.find_generated_transcript(all_language_codes)
                    except Exception:
                        print(f"No transcript found for video {video_id} in any language.")
                        return None
            return transcript.fetch()
        except Exception as e:
            print(f"Error getting transcript for video {video_id}: {str(e)}")
            return None

    def translate_text(self, text, target_lang='en'):
        """Translate text to target language."""
        try:
            result = self.translator.translate(text, dest=target_lang)
            return result.text
        except Exception as e:
            print(f"Error translating text: {str(e)}")
            return text

    def chunk_transcript(self, transcript, chunk_duration=35):
        """Chunk transcript into specified duration segments."""
        chunks = []
        current_chunk = []
        current_duration = 0

        for entry in transcript:
            if current_duration + entry['duration'] <= chunk_duration:
                current_chunk.append(entry)
                current_duration += entry['duration']
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = [entry]
                current_duration = entry['duration']

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def process_video(self, url, display_lang=None):
        """Process YouTube video and return transcript in chunks, with language selection support."""
        try:
            # Get video info
            video_info = self.get_video_info(url)
            if not video_info:
                return None
            
            # Get transcript
            transcript = self.get_transcript(video_info['id'])
            if not transcript:
                return None

            # Detect original language (use first entry's language if available, else default to 'en')
            original_lang = transcript[0].get('language', transcript[0].get('language_code', 'en'))
            if not original_lang:
                original_lang = 'en'

            # Chunk the transcript
            chunks = self.chunk_transcript(transcript)

            # Determine display language
            if display_lang is None:
                # If original is Hindi, default to Hindi, else English
                display_lang = 'hi' if original_lang.startswith('hi') else 'en'

            processed_chunks = []
            for i, chunk in enumerate(chunks):
                chunk_text = ' '.join([entry['text'] for entry in chunk])
                if display_lang == original_lang or (original_lang.startswith('hi') and display_lang == 'hi'):
                    display_text = chunk_text
                else:
                    display_text = self.translate_text(chunk_text, target_lang=display_lang)
                start_time = chunk[0]['start']
                end_time = chunk[-1]['start'] + chunk[-1]['duration']
                processed_chunks.append({
                    'chunk_number': i + 1,
                    'start_time': self.format_timestamp(start_time),
                    'end_time': self.format_timestamp(end_time),
                    'text': display_text
                })

            # Also prepare the full transcript in the selected language
            full_text = ' '.join([entry['text'] for entry in transcript])
            if display_lang == original_lang or (original_lang.startswith('hi') and display_lang == 'hi'):
                full_transcript = full_text
            else:
                full_transcript = self.translate_text(full_text, target_lang=display_lang)

            return {
                'video_title': video_info['title'],
                'video_url': url,
                'duration': self.format_timestamp(video_info['duration']),
                'chunks': processed_chunks,
                'full_transcript': full_transcript,
                'original_lang': original_lang,
                'display_lang': display_lang
            }
        except Exception as e:
            print(f"Error processing video: {str(e)}")
            return None

# Create Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    result = None
    
    if request.method == 'POST':
        url = request.form.get('url')
        display_lang = request.form.get('display_lang', None)
        if url:
            transcriber = YouTubeTranscriber()
            result = transcriber.process_video(url, display_lang=display_lang)
            if not result:
                error = "Failed to process video. Please check the URL and try again."
    
    return render_template('index.html', result=result, error=error)

@app.route('/transcript', methods=['POST'])
def transcript():
    url = request.form.get('url')
    display_lang = request.form.get('display_lang', None)
    if not url:
        return jsonify({'error': 'No URL provided.'}), 400
    transcriber = YouTubeTranscriber()
    result = transcriber.process_video(url, display_lang=display_lang)
    if not result:
        return jsonify({'error': 'Failed to process video.'}), 400
    # Render only the transcript section as HTML
    transcript_html = render_template('transcript_partial.html', result=result)
    return jsonify({'transcript_html': transcript_html})

def main():
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run Flask app
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    main() 