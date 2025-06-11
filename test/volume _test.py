import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-modify-playback-state user-read-playback-state"))

try:
    sp.volume(50)
    print("Volume set to 50%")
except Exception as e:
    print("❌ Error:", e)
