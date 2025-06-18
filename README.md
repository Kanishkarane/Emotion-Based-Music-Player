# Emotion-Based-Music-Player

# Emotion-Based Music Player

A Streamlit application that detects emotions from facial expressions and recommends Spotify playlists based on your mood.

## Features

- Capture photos using camera or file upload
- AI-powered emotion detection from facial expressions
- Automatic Spotify playlist recommendations
- Support for 7 emotions: happy, sad, angry, surprise, neutral, fear, disgust

## Installation

```bash
pip install streamlit opencv-python deepface spotipy pillow numpy
```

## Setup

1. Create a Spotify app at https://developer.spotify.com/dashboard
2. Get your Client ID and Client Secret
3. Add `http://127.0.0.1:8888/callback` as redirect URI
4. Update the credentials in the code

## Usage

1. Run the application:
   ```bash
   streamlit run emotion_music_app.py
   ```

2. Open http://localhost:8501 in your browser

3. Follow the app tabs:
   - Capture: Take or upload a photo
   - Analyze: Detect emotion from your photo
   - Music: Connect to Spotify and play recommended playlist

## Requirements

- Python 3.7+
- Webcam (optional)
- Spotify account
- Internet connection

## Notes

- Images are processed locally and not stored
- Requires Spotify API credentials to function
- Works best with clear, well-lit photos
