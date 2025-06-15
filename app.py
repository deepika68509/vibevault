from flask import Flask, render_template, request, jsonify, Response
import cv2
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import numpy as np
import random

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Spotify credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
    print("❌ Error: Spotify credentials not found in .env file")
    print("Please create a .env file with SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET")
    sys.exit(1)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

# Global variables for camera
camera = None
current_emotion = "neutral"
detected_emotion = None

def get_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 350)
    return camera

def generate_frames():
    global current_emotion, detected_emotion
    while True:
        success, frame = get_camera().read()
        if not success:
            break
        else:
            # Flip the frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Add emotion text to frame
            emotion_text = f"Current: {current_emotion}"
            if detected_emotion:
                emotion_text += f" | Detected: {detected_emotion}"
            
            cv2.putText(frame, emotion_text, (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def get_spotify_tracks(emotion, language='english'):
    try:
        # Language-specific queries with more specific terms
        language_queries = {
            'english': f"{emotion} mood english songs",
            'hindi': f"{emotion} mood hindi bollywood",
            'kannada': f"{emotion} mood kannada",
            'tamil': f"{emotion} mood tamil",
            'telugu': f"{emotion} mood telugu",
            'malayalam': f"{emotion} mood malayalam",
            'bengali': f"{emotion} mood bengali",
            'marathi': f"{emotion} mood marathi",
            'punjabi': f"{emotion} mood punjabi",
            'gujarati': f"{emotion} mood gujarati"
        }

        query = language_queries.get(language.lower(), language_queries['english'])
        results = sp.search(q=query, type='track', limit=50)
        tracks = []

        for item in results['tracks']['items']:
            track = {
                "name": item['name'],
                "artist": item['artists'][0]['name'],
                "preview_url": item['preview_url'],
                "external_url": item['external_urls']['spotify'],
                "image": item['album']['images'][0]['url'] if item['album']['images'] else None,
                "language": language
            }
            tracks.append(track)

        random.shuffle(tracks)
        return tracks[:15]
    except Exception as e:
        print("❌ Spotify API error:", e)
        return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detect', methods=['POST'])
def detect():
    global current_emotion, detected_emotion
    data = request.get_json()
    language = data.get('language', 'english')
    text_input = data.get('text', '')
    
    if text_input:
        # Use manual emotion input
        detected_emotion = text_input.lower()
    else:
        # Use camera-based emotion detection
        detected_emotion = current_emotion
    
    tracks = get_spotify_tracks(detected_emotion, language)
    return jsonify({"emotion": detected_emotion, "tracks": tracks})

@app.route('/stop_camera')
def stop_camera():
    global camera
    if camera is not None:
        camera.release()
        camera = None
    return jsonify({"status": "success"})

if __name__ == '__main__':
    print("🚀 Starting Emotion Music Recommender...")
    print("📝 Make sure you have created a .env file with your Spotify credentials")
    print("🌐 Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True)