import streamlit as st
from agent import agent
import json
import re
import urllib.parse

from dotenv import load_dotenv
load_dotenv()
import os
groq_api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Music Playlist Agent", layout="centered")

# 🎨 Styling
st.markdown("""
<style>

/* 🌤️ Premium Soft Light Gradient Background */
.stApp {
    background: linear-gradient(135deg, #f7fbff, #eaf4ff, #f0f8ff, #ffffff);
    background-size: 300% 300%;
    animation: bgFlow 18s ease infinite;
}

/* 🌊 Background animation */
@keyframes bgFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 🎧 Animated music wave overlay */
.stApp::before {
    content: "";
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 220px;
    background: url("https://svgshare.com/i/13tP.svg");
    background-size: cover;
    opacity: 0.10;
    animation: waveMove 12s linear infinite;
    pointer-events: none;
    z-index: 0;
}

/* 🌊 Wave animation movement */
@keyframes waveMove {
    0% { transform: translateX(0); }
    100% { transform: translateX(-200px); }
}

/* 🎧 Main container */
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 2.5rem;
}

/* 🎵 Title */
h1 {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #1f2a44;
    margin-bottom: 10px;
}

/* 🎼 Playlist title */
.playlist-title {
    font-size: 32px;
    font-weight: bold;
    text-align: center;
    color: #1f2a44;
    margin-top: 20px;
}

/* 🎶 Glass song card */
.song-card {
    background: rgba(255, 255, 255, 0.60);
    backdrop-filter: blur(16px);
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 14px;
    border: 1px solid rgba(0, 0, 0, 0.06);
    box-shadow: 0 8px 22px rgba(0,0,0,0.08);
    transition: all 0.25s ease;
    position: relative;
    z-index: 2;
}

.song-card:hover {
    transform: translateY(-5px) scale(1.01);
    box-shadow: 0 14px 30px rgba(0,0,0,0.12);
}

/* 🎼 Song title */
.song-title {
    font-size: 18px;
    font-weight: 700;
    color: #1f2a44;
}

/* 🎼 Reason text */
.song-reason {
    font-size: 14px;
    color: #4b5563;
    margin-top: 6px;
    margin-bottom: 10px;
}

/* 🎧 Spotify button */
.spotify-btn {
    display: inline-block;
    padding: 8px 14px;
    background: linear-gradient(135deg, #1DB954, #1ed760);
    color: white;
    border-radius: 10px;
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    transition: 0.2s ease;
}

.spotify-btn:hover {
    transform: scale(1.07);
}

/* 📱 Input styling */
input {
    border-radius: 10px !important;
    padding: 10px !important;
    border: 1px solid #d0d7e2 !important;
}

/* 🌫️ Soft glow overlay */
.stApp::after {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 20% 20%, rgba(120,180,255,0.10), transparent 40%),
                radial-gradient(circle at 80% 30%, rgba(180,220,255,0.12), transparent 45%),
                radial-gradient(circle at 50% 80%, rgba(200,230,255,0.08), transparent 50%);
    pointer-events: none;
    z-index: 0;
}

</style>
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🎧 Music Playlist Curator Agent</h1>", unsafe_allow_html=True)

# Input
user_input = st.text_input("Enter your mood (happy, chill, focus...)")
language = st.multiselect(
    "🌍 Select languages for songs",
    ["Kannada", "Hindi", "English", "Tamil", "Telugu", "Malayalam"],
    default=["Kannada", "Hindi", "English"]
)

playlist_data = None  # store globally for download

if st.button("Generate Playlist"):

    if not user_input:
        st.warning("Please enter a mood 😄")

    else:
        with st.spinner("Creating your vibe... 🎶"):
            try:
                prompt = f"""
User mood: {user_input}

Selected languages: {', '.join(language)}

Generate a music playlist.

IMPORTANT RULES:
- Use only selected languages
- Match mood properly

Return ONLY JSON format:
{{
  "playlist_name": "",
  "songs": [
    {{"title": "", "reason": ""}}
  ]
}}
"""
                response = agent.invoke(
                    {"messages": [{"role": "user", "content": prompt}]},
                    {"configurable": {"thread_id": "1"}}
                )

                result = response["messages"][-1].content.strip()

                match = re.search(r'\{.*\}', result, re.DOTALL)

                if match:
                    playlist_data = json.loads(match.group())
                else:
                    st.error("Invalid JSON from model ❌")
                    st.write(result)
                    st.stop()

                # 🎧 Playlist Title
                st.markdown(
                    f"<div class='playlist-title'>{playlist_data['playlist_name']}</div>",
                    unsafe_allow_html=True
                )

                st.markdown("---")

                # 🎵 Songs
                for song in playlist_data["songs"]:

                    song_title = song["title"]
                    reason = song["reason"]

                    # Spotify search link
                    query = urllib.parse.quote(song_title)
                    spotify_url = f"https://open.spotify.com/search/{query}"

                    st.markdown(f"""
                    <div class="song-card">
                        <div class="song-title">🎵 {song_title}</div>
                        <div class="song-reason">👉 {reason}</div>
                        <a class="spotify-btn" href="{spotify_url}" target="_blank">🎧 Open in Spotify</a>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")

                # 💾 Download playlist
                st.download_button(
                    label="💾 Download Playlist JSON",
                    data=json.dumps(playlist_data, indent=4),
                    file_name="playlist.json",
                    mime="application/json"
                )

            except Exception as e:
                st.error(f"ERROR: {e}")