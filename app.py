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

@app.route('/individual_post')
def show_post():
    post_image = posts[post_id -1]
    post_title = "Placeholder Title"
    post_price = "$Placeholder Price"
    post_description = "Placeholder Description"
    return render_template('individual_post.html', post_image=post_image, post_title=post_title, post_price=post_price, post_description=post_description)