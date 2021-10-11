import os
import random
from dotenv import find_dotenv, load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from spot import get_artist_info, get_lyrics

load_dotenv(find_dotenv())
url = os.getenv("DATABASE_URL")
if url and url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

SECRET_KEY = os.getenv("SECRET_KEY")


app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY

db = SQLAlchemy(app)


class Person(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    artist = db.Column(db.String(22))


db.create_all()


@app.route("/", methods=["GET", "POST"])
def main():
    ARTIST_IDS = [
        "78rUTD7y6Cy67W1RVzYs7t",
        "2xvtxDNInKDV4AvGmjw6d1",
        "1CbA4z6JauNQnHzOErDQL6",
        "3x2XRFCUMHeXZ9uRit3pKu",
        "2SJhf6rTOU53g8yBdAjPby",
        "73sIBHcqh3Z3NyqHKZ7FOL",
        "2sSGPbdZJkaSE2AbcGOACx",
    ]
    artist_len = len(ARTIST_IDS) - 1
    random_artist = random.randint(0, artist_len)
    artist_info = get_artist_info(ARTIST_IDS[random_artist])
    # ARTIST INFO
    name = artist_info[0]
    img = artist_info[1]

    # TRACK INFO
    track = artist_info[2]
    trackName = track[0]
    trackAudio = track[1]
    trackImg = track[2]

    topTracks = artist_info[3]

    lyricLink = get_lyrics(name, trackName)

    return render_template(
        "index.html",
        name=name,
        img=img,
        len=len(topTracks),
        topTracks=topTracks,
        track=track,
        trackName=trackName,
        trackImg=trackImg,
        trackAudio=trackAudio,
        lyricLink=lyricLink,
    )


app.run(
    # host="0.0.0.0",
    # port=int(os.getenv("PORT", 8080)),
    debug=True
)
