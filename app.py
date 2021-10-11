import os
import random
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, request, redirect
from spot import get_artist_info, get_lyrics
from models import db, login, Person, Artist
from flask_login import login_required, current_user, login_user, logout_user


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

db.init_app(app)
login.init_app(app)
login.login_view = "login"


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/music")
@login_required
def music():
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
        "music.html",
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


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect("/music")

    if request.method == "POST":
        username = request.form["username"]
        user = Person.query.filter_by(username=username).first()
        if user is not None:
            login_user(user)
            return redirect("/music")

    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect("/music")

    if request.method == "POST":
        username = request.form["username"]

        if Person.query.filter_by(username=username).first():
            return "Username is taken!"

        user = Person(username=username)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/music")


app.run(
    # host="0.0.0.0",
    # port=int(os.getenv("PORT", 8080)),
    debug=True
)
