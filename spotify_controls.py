import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="8c93be50806b40dea8e6995b9b19cf6f",
    client_secret="b6249807ba5d41f38e5822b9d1ed8bcf",
    redirect_uri="http://127.0.0.1:8000/callback",
    scope="user-read-playback-state,user-modify-playback-state"
))

def play_pause():
    playback = sp.current_playback()
    if playback and playback["is_playing"]:
        sp.pause_playback()
    else:
        sp.start_playback()

def next_track():
    sp.next_track()

def previous_track():
    sp.previous_track()

def volume_up():
    playback = sp.current_playback()
    if playback:
        vol = playback["device"]["volume_percent"]
        sp.volume(min(100, vol + 10))

def volume_down():
    playback = sp.current_playback()
    if playback:
        vol = playback["device"]["volume_percent"]
        sp.volume(max(0, vol - 10))
