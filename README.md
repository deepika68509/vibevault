# Emotion-Based Music Recommender 🎵

A web application that detects your emotions through your camera and recommends music based on your mood and preferred language.

## Features

- Real-time emotion detection using your camera
- Text-based emotion detection as an alternative
- Music recommendations based on detected emotions
- Support for multiple languages (English, Hindi, Kannada, Tamil, Telugu, Malayalam, Bengali, Marathi, Punjabi, Gujarati)
- Beautiful modern UI with animations
- Spotify integration for music recommendations
- Responsive design

## Tech Stack

- Python 3.9.7
- Flask
- OpenCV for emotion detection
- Spotify API for music recommendations
- HTML/CSS/JavaScript for frontend
- DeepFace for emotion analysis
- Hugging Face Transformers for text-based emotion detection

## Prerequisites

- Python 3.9.18 (required)
- Spotify Developer Account
- Webcam access (for local development)

## Local Installation

1. Clone the repository:
```bash
git clone https://github.com/deepika68509/vibevault.git
cd vibevault
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
Create a `.env` file in the root directory with:
```
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
```

## Local Usage

1. Run the application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Allow camera access when prompted (or use text input)

4. Select your preferred language and click "Get Music Recommendations"

## Deployment

The application is deployed on Render.com. To deploy your own version:

1. Create a Render account at https://render.com
2. Create a new Web Service
3. Connect your GitHub repository
4. Add the following environment variables in Render:
   - `SPOTIPY_CLIENT_ID`
   - `SPOTIPY_CLIENT_SECRET`
5. Deploy!

Note: The camera functionality is only available in local development. In production, use the text-based emotion detection.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Spotify API for music data
- DeepFace for emotion detection
- OpenCV for camera handling
- Hugging Face for text-based emotion detection 
