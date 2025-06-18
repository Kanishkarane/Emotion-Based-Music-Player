import streamlit as st
import cv2
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import time
import numpy as np
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="Emotion Music Player",
    page_icon="🎵",
    layout="wide"
)

# Initialize session state
if 'emotion' not in st.session_state:
    st.session_state.emotion = None
if 'emotion_confidence' not in st.session_state:
    st.session_state.emotion_confidence = None
if 'captured_image' not in st.session_state:
    st.session_state.captured_image = None
if 'spotify_authenticated' not in st.session_state:
    st.session_state.spotify_authenticated = False

# Spotify configuration
SPOTIFY_CONFIG = {
    "client_id": "0eecaf83a4cb44828b73ea8507dd7669",
    "client_secret": "495c2464a176499083713eb8dec1b794",
    "redirect_uri": "http://127.0.0.1:8888/callback",
    "scope": "user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
}

# Playlist URLs mapping
PLAYLIST_URLS = {
    "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/playlist/37i9dQZF1DWZRCwEx4sYHR",
    "surprise": "https://open.spotify.com/playlist/37i9dQZF1DWVlYsZJXqdym",
    "neutral": "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO",
    "fear": "https://open.spotify.com/playlist/37i9dQZF1DWTtTyYU0Z2sM",
    "disgust": "https://open.spotify.com/playlist/37i9dQZF1DX4fpCWaHOned"
}

# Emotion emojis and descriptions
EMOTION_INFO = {
    "happy": {"emoji": "😊", "description": "Feeling joyful and upbeat!", "color": "🟡"},
    "sad": {"emoji": "😢", "description": "Feeling down or melancholic", "color": "🔵"},
    "angry": {"emoji": "😠", "description": "Feeling frustrated or mad", "color": "🔴"},
    "surprise": {"emoji": "😲", "description": "Feeling amazed or shocked", "color": "🟣"},
    "neutral": {"emoji": "😐", "description": "Feeling calm and balanced", "color": "⚪"},
    "fear": {"emoji": "😨", "description": "Feeling anxious or scared", "color": "🟤"},
    "disgust": {"emoji": "🤢", "description": "Feeling repulsed or annoyed", "color": "🟢"}
}

def initialize_spotify():
    """Initialize Spotify client"""
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(**SPOTIFY_CONFIG))
        current = sp.current_playback()
        return sp, True
    except Exception as e:
        return None, False

def capture_from_camera():
    """Capture image from camera"""
    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            return None, "Camera not accessible"
        
        ret, frame = cam.read()
        cam.release()
        cv2.destroyAllWindows()
        
        if ret:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame_rgb, None
        else:
            return None, "Failed to capture image"
    except Exception as e:
        return None, str(e)

def analyze_emotion(image):
    """Analyze emotion from image"""
    try:
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Save temporary image for DeepFace analysis
        temp_image = Image.fromarray(image)
        temp_image.save("temp_capture.jpg")
        
        # Analyze emotion
        result = DeepFace.analyze(img_path="temp_capture.jpg", actions=['emotion'])
        emotion = result[0]['dominant_emotion']
        confidence = result[0]['emotion'][emotion]
        
        # Clean up temp file
        if os.path.exists("temp_capture.jpg"):
            os.remove("temp_capture.jpg")
        
        return emotion, confidence, None
    except Exception as e:
        return None, None, str(e)

def main():
    # Main header
    st.title("🎵 Emotion-Based Music Player")
    st.markdown("**Detect your emotion and get personalized music recommendations!**")
    
    # Create tabs for better organization
    tab1, tab2, tab3, tab4 = st.tabs(["📸 Capture", "🧠 Analyze", "🎵 Music", "ℹ️ Info"])
    
    # Tab 1: Image Capture
    with tab1:
        st.header("📸 Capture Your Photo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Camera Capture")
            if st.button("📷 Take Photo", type="primary", use_container_width=True):
                with st.spinner("Capturing photo..."):
                    image, error = capture_from_camera()
                    if image is not None:
                        st.session_state.captured_image = image
                        st.success("✅ Photo captured successfully!")
                        st.balloons()
                    else:
                        st.error(f"❌ Camera capture failed: {error}")
        
        with col2:
            st.subheader("Upload Image")
            uploaded_file = st.file_uploader(
                "Choose an image file",
                type=['jpg', 'jpeg', 'png'],
                help="Upload a clear photo of your face"
            )
            
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.session_state.captured_image = np.array(image)
                st.success("✅ Image uploaded successfully!")
        
        # Display captured image
        if st.session_state.captured_image is not None:
            st.subheader("📷 Your Photo")
            st.image(
                st.session_state.captured_image,
                caption="Captured/Uploaded Image",
                width=400
            )
        else:
            st.info("👆 Please capture a photo or upload an image to get started")
    
    # Tab 2: Emotion Analysis
    with tab2:
        st.header("🧠 Emotion Analysis")
        
        if st.session_state.captured_image is not None:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if st.button("🔍 Analyze Emotion", type="primary", use_container_width=True):
                    with st.spinner("🤖 Analyzing your emotion..."):
                        emotion, confidence, error = analyze_emotion(st.session_state.captured_image)
                        if emotion:
                            st.session_state.emotion = emotion
                            st.session_state.emotion_confidence = confidence
                            st.success(f"✅ Analysis complete!")
                            st.balloons()
                        else:
                            st.error(f"❌ Analysis failed: {error}")
            
            with col2:
                if st.session_state.emotion:
                    emotion = st.session_state.emotion
                    confidence = st.session_state.emotion_confidence
                    emotion_info = EMOTION_INFO.get(emotion, {"emoji": "❓", "description": "Unknown emotion", "color": "⚫"})
                    
                    # Display emotion results
                    st.subheader("🎯 Results")
                    
                    # Create metrics
                    col_metric1, col_metric2 = st.columns(2)
                    with col_metric1:
                        st.metric(
                            label="Detected Emotion",
                            value=f"{emotion_info['emoji']} {emotion.title()}"
                        )
                    with col_metric2:
                        st.metric(
                            label="Confidence",
                            value=f"{confidence:.1f}%"
                        )
                    
                    # Progress bar for confidence
                    st.progress(confidence / 100)
                    
                    # Description
                    st.info(f"**{emotion_info['description']}**")
                    
                else:
                    st.info("👆 Click 'Analyze Emotion' to detect your current mood")
        else:
            st.warning("📸 Please capture or upload an image first in the 'Capture' tab")
    
    # Tab 3: Music Player
    with tab3:
        st.header("🎵 Music Recommendations")
        
        if st.session_state.emotion:
            emotion = st.session_state.emotion
            emotion_info = EMOTION_INFO.get(emotion, {"emoji": "❓", "description": "Unknown emotion"})
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader(f"🎶 {emotion.title()} Playlist")
                st.write(f"**Emotion:** {emotion_info['emoji']} {emotion.title()}")
                st.write(f"**Description:** {emotion_info['description']}")
                
                if emotion in PLAYLIST_URLS:
                    st.write(f"**Playlist:** Curated {emotion} music")
                    
                    # Spotify authentication
                    if not st.session_state.spotify_authenticated:
                        if st.button("🔐 Connect to Spotify", type="secondary", use_container_width=True):
                            with st.spinner("Connecting to Spotify..."):
                                sp, success = initialize_spotify()
                                if success:
                                    st.session_state.spotify_authenticated = True
                                    st.success("✅ Spotify connected successfully!")
                                else:
                                    st.error("❌ Spotify connection failed")
                    else:
                        st.success("✅ Spotify is connected")
                    
                    # Play music button
                    if st.button("🎵 Play Music", type="primary", use_container_width=True):
                        webbrowser.open(PLAYLIST_URLS[emotion])
                        st.success(f"🎉 Opening {emotion}-based playlist!")
                        st.info("💡 Please hit 'Play' on the Spotify Web Player")
                        st.balloons()
                else:
                    st.error("❌ No playlist found for this emotion")
            
            with col2:
                # Show all available playlists
                st.subheader("🎵 All Available Playlists")
                for emo, info in EMOTION_INFO.items():
                    with st.expander(f"{info['emoji']} {emo.title()} Playlist"):
                        st.write(f"**Mood:** {info['description']}")
                        if st.button(f"Play {emo.title()}", key=f"play_{emo}"):
                            webbrowser.open(PLAYLIST_URLS[emo])
                            st.success(f"Opening {emo} playlist!")
        else:
            st.warning("🧠 Please analyze your emotion first to get personalized music recommendations")
    
    # Tab 4: Information
    with tab4:
        st.header("ℹ️ How It Works")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Steps")
            st.markdown("""
            1. **📸 Capture Image**: Take a photo or upload an image
            2. **🧠 Analyze Emotion**: AI analyzes your facial expression
            3. **🎵 Get Music**: Receive personalized playlist recommendations
            4. **🎶 Play**: Enjoy music that matches your mood!
            """)
            
            st.subheader("🎯 Supported Emotions")
            for emotion, info in EMOTION_INFO.items():
                st.write(f"• {info['emoji']} **{emotion.title()}**: {info['description']}")
        
        with col2:
            st.subheader("🔧 Requirements")
            st.markdown("""
            - **Camera access** for photo capture
            - **Spotify account** for music playback
            - **Internet connection** for AI analysis
            """)
            
            st.subheader("🔒 Privacy")
            st.markdown("""
            - Images are processed locally
            - No personal data is stored
            - Temporary files are automatically deleted
            """)
            
            st.subheader("📞 Support")
            st.info("Having issues? Make sure your camera is working and you have a stable internet connection.")
    
    # Sidebar status
    with st.sidebar:
        st.header("📊 Status")
        
        # Image status
        if st.session_state.captured_image is not None:
            st.success("✅ Image Ready")
        else:
            st.warning("📸 No Image")
        
        # Emotion status
        if st.session_state.emotion:
            emotion_info = EMOTION_INFO.get(st.session_state.emotion, {"emoji": "❓"})
            st.success(f"✅ Emotion: {emotion_info['emoji']} {st.session_state.emotion.title()}")
        else:
            st.warning("🧠 No Emotion Detected")
        
        # Spotify status
        if st.session_state.spotify_authenticated:
            st.success("✅ Spotify Connected")
        else:
            st.warning("🔐 Spotify Not Connected")
        
        st.divider()
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        if st.button("🔄 Reset All", use_container_width=True):
            st.session_state.emotion = None
            st.session_state.emotion_confidence = None
            st.session_state.captured_image = None
            st.session_state.spotify_authenticated = False
            st.success("🔄 All data reset!")
            st.rerun()

if __name__ == "__main__":
    main()
