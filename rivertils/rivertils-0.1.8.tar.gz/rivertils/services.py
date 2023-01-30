import os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
from dotenv import load_dotenv

load_dotenv(override=True)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# GSPREADER_GOOGLE_CREDS = os.environ["GSPREADER_GOOGLE_CREDS"] if "GSPREADER_GOOGLE_CREDS" in os.environ else None
# GSPREADER_GOOGLE_CREDS_PATH = os.environ["GSPREADER_GOOGLE_CREDS_PATH"] if "GSPREADER_GOOGLE_CREDS_PATH" in os.environ else None
# GSPREADER_GOOGLE_CLIENT_EMAIL = os.environ["GSPREADER_GOOGLE_CLIENT_EMAIL"]


def get_spotify_client():
    # print('signing into spotify...')
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)