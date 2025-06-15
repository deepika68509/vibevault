from flask import Flask, render_template, request, jsonify, Response, redirect
import cv2
from deepface import DeepFace
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import numpy as np
import random
import ssl

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Force HTTPS in production
@app.before_request
def before_request():
    if not request.is_secure and os.environ.get('FLASK_ENV') == 'production':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

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
detected_emotion = None  # Store the emotion detected when button is clicked

def get_camera():
    global camera
    if camera is None:
        try:
            camera = cv2.VideoCapture(0)
            if not camera.isOpened():
                # Try alternative camera index
                camera = cv2.VideoCapture(1)
            if not camera.isOpened():
                print("❌ Warning: Could not open camera")
                return None
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 350)
        except Exception as e:
            print("❌ Camera initialization error:", e)
            return None
    return camera

def generate_frames():
    global current_emotion, detected_emotion
    frame_count = 0
    max_frames = 10  # Process every 10 frames

    while True:
        camera = get_camera()
        if camera is None:
            # Return a blank frame if camera is not available
            blank_frame = np.zeros((350, 500, 3), dtype=np.uint8)
            cv2.putText(blank_frame, "Camera not available", (50, 175), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            ret, buffer = cv2.imencode('.jpg', blank_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            continue

        success, frame = camera.read()
        if not success:
            # Return a blank frame if frame read fails
            blank_frame = np.zeros((350, 500, 3), dtype=np.uint8)
            cv2.putText(blank_frame, "Camera error", (50, 175), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            ret, buffer = cv2.imencode('.jpg', blank_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            continue

        # Flip the frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Process every 10 frames to reduce CPU usage
        if frame_count % max_frames == 0:
            try:
                # Convert frame to RGB for DeepFace
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = DeepFace.analyze(rgb_frame, actions=["emotion"], enforce_detection=False, silent=True)
                current_emotion = result[0]['dominant_emotion']
            except Exception as e:
                print("❌ Emotion detection failed:", e)
                current_emotion = "neutral"

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
        
        frame_count += 1

def get_spotify_tracks(emotion, language='english'):
    try:
        # Language-specific queries with more specific terms
        language_queries = {
            'english': f"{emotion} mood english songs",  # More specific for English
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

        # Get tracks for the selected language
        query = language_queries.get(language.lower(), language_queries['english'])
        
        # Get more tracks than needed to allow for better shuffling
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

        # Shuffle the tracks and return only 12
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
    app.run(debug=True, ssl_context='adhoc')