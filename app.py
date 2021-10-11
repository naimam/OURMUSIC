import os
import random
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, request, redirect, Response, flash
from spot import get_artist_info, get_lyrics
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
    UserMixin,
)
from flask_sqlalchemy import SQLAlchemy


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

db = SQLAlchemy()
db.init_app(app)
login = LoginManager()
login.init_app(app)
login.login_view = "login"


class Person(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    artists = db.relationship("Artist", backref="users", lazy=True)

    def __repr__(self):
        return "<Username: {}>".format(self.username)

    def get_id(self):
        return self.user_id


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(22))
    person_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    def __repr__(self):
        return "<Artist Id: {}>".format(self.artist_id)


@login.user_loader
def load_user(user_id):
    return Person.query.get(user_id)


@app.errorhandler(401)
def page_not_found(e):
    return Response("<p>Login failed</p>")


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/")
@login_required
def index():
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
    artist = ARTIST_IDS[random_artist]

    (name, img, track, topTracks) = get_artist_info(artist)
    (trackName, trackAudio, trackImg) = track

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
        return redirect("/")

    if request.method == "POST":
        username = request.form["username"]
        user = Person.query.filter_by(username=username).first()
        if user is not None:
            login_user(user)
            return redirect("/")
        if user is None:
            flash("Invalid username!")
    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.form["username"]

        if Person.query.filter_by(username=username).first():
            flash("Username is taken!")
            return redirect("/register")

        user = Person(username=username)
        db.session.add(user)
        db.session.commit()
        flash("Account creation successful! Login with your username below!")
        return redirect("/login")
    return render_template("register.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


app.run(
    # host="0.0.0.0",
    # port=int(os.getenv("PORT", 8080)),
    debug=True
)
