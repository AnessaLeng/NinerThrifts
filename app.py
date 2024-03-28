from flask import Flask, render_template, request
app = Flask(__name__)


profile_info = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def show_profile():
    user_pic = "static/user_icon.png"
    username = "username here"
    bio = "bio here"
    followers = "###"
    following = "###"
    posts= ['static/placeholder.png', 'static/placeholder.png', 'static/placeholder.png', 'static/placeholder.png',
            'static/placeholder.png','static/placeholder.png','static/placeholder.png','static/placeholder.png']
    profile_info[username] = []
    profile_info[username].append(user_pic)
    profile_info[username].append(bio)
    profile_info[username].append(followers)
    profile_info[username].append(following)
    return render_template("profile.html", profile_info = profile_info, posts = posts)