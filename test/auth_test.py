from spotipy.oauth2 import SpotifyOAuth
import spotipy

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="8c93be50806b40dea8e6995b9b19cf6f",
    client_secret="b6249807ba5d41f38e5822b9d1ed8bcf",
    redirect_uri="http://127.0.0.1:8000/callback",
    scope="user-read-playback-state,user-modify-playback-state"
))

print("✅ Spotify Authenticated! Now close this and run main.py")

try:
    sp.volume(50)
    print("Volume set to 50%")
except Exception as e:
    print("❌ Error:", e)