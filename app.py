import os
import random
from flask import Flask, render_template
from spot import get_artist_info, get_lyrics

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def main():
    ARTIST_IDS = ["78rUTD7y6Cy67W1RVzYs7t", "2xvtxDNInKDV4AvGmjw6d1", 
    "1CbA4z6JauNQnHzOErDQL6", "3x2XRFCUMHeXZ9uRit3pKu", 
    "2SJhf6rTOU53g8yBdAjPby", "73sIBHcqh3Z3NyqHKZ7FOL",
    "2sSGPbdZJkaSE2AbcGOACx"]
    artist_len = len(ARTIST_IDS) - 1
    random_artist = random.randint(0, artist_len)	
    artist_info = get_artist_info(ARTIST_IDS[random_artist])
    # ARTIST INFO
    name=artist_info[0]
    img = artist_info[1]

    #TRACK INFO
    track = artist_info[2]
    trackName = track[0]
    trackAudio = track[1]
    trackImg = track[2]

    topTracks = artist_info[3]

    lyricLink = get_lyrics(name, trackName)
    

    return render_template(
        "index.html",
        name = name,
        img = img,
        len = len(topTracks), topTracks = topTracks,
        track = track,
        trackName = trackName,
        trackImg = trackImg,
        trackAudio = trackAudio,
        lyricLink = lyricLink,
    )

app.run(
    host='0.0.0.0',
    port=int(os.getenv('PORT', 8080)),
    debug=True
)
