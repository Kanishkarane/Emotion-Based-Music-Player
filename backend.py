import cv2
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import time

# -------------------- STEP 1: Capture Image --------------------
cam = cv2.VideoCapture(0)
ret, frame = cam.read()
if ret:
    cv2.imwrite("Captured.jpg", frame)
cam.release()
cv2.destroyAllWindows()

# -------------------- STEP 2: Analyze Emotion --------------------
try:
    result = DeepFace.analyze(img_path="Captured.jpg", actions=['emotion'])
    emotion = result[0]['dominant_emotion']
    print("🧠 Detected Emotion:", emotion)
except Exception as e:
    print("❌ Error analyzing face:", e)
    emotion = None

# -------------------- STEP 3: Authenticate with Spotify --------------------
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="",
    client_secret="",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
))

try:
    current = sp.current_playback()
    print("✅ Spotify Authentication Successful")
except Exception as e:
    print("❌ Spotify Authentication Failed:", e)

# -------------------- STEP 4: Map Emotion to Playlist --------------------
playlist_urls = {
    "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/playlist/37i9dQZF1DWZRCwEx4sYHR",
    "surprise": "https://open.spotify.com/playlist/37i9dQZF1DWVlYsZJXqdym",
    "neutral": "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO",
    "fear": "https://open.spotify.com/playlist/37i9dQZF1DWTtTyYU0Z2sM",
    "disgust": "https://open.spotify.com/playlist/37i9dQZF1DX4fpCWaHOned"
}

# -------------------- STEP 5: Open Spotify Playlist in Browser --------------------
if emotion in playlist_urls:
    print(f"🎵 Opening {emotion}-based playlist in browser...")
    webbrowser.open(playlist_urls[emotion])
    time.sleep(1)  # slight delay to ensure browser opens
    print("👉 Please hit 'Play' on the Spotify Web Player.")
else:
    print("😕 No playlist mapped to this emotion.")
