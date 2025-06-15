# Emotion-Based Music Recommender 🎵

A web application that detects your emotions through your camera and recommends music based on your mood and preferred language.

## Features

- Real-time emotion detection using your camera
- Music recommendations based on detected emotions
- Support for multiple languages (English, Hindi, Kannada, Tamil, Telugu, Malayalam, Bengali, Marathi, Punjabi, Gujarati)
- Beautiful vintage-inspired UI with animations
- Spotify integration for music previews
- Responsive design

## Tech Stack

- Python (Flask)
- OpenCV for emotion detection
- Spotify API for music recommendations
- HTML/CSS/JavaScript for frontend
- DeepFace for emotion analysis

## Prerequisites

- Python 3.8 or higher
- Spotify Developer Account
- Webcam access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/emotion-music.git
cd emotion-music
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
Create a `.env` file in the root directory with:
```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Allow camera access when prompted

4. Select your preferred language and click "Get Music Recommendations"

## Deployment

The application is deployed on Render.com and can be accessed at: [Your Render URL]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Spotify API for music data
- DeepFace for emotion detection
- OpenCV for camera handling 