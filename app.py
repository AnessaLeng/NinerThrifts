import os
from flask import Flask, redirect, render_template, request, send_from_directory, url_for, abort, session
from random import randint, random
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from repositories import post_repo, profile_repo


load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')

bcrypt = Bcrypt(app)
profile_info = {}
users = {}

##Jaidens profile page
@app.get('/profile')
def show_profile():
    # user_pic = "static/user_icon.png"
    # username = "username here"
    # bio = "bio here"
    # followers = "###"
    # following = "###"
    # posts= ['static/placeholder.png', 'static/placeholder.png', 'static/placeholder.png', 'static/placeholder.png',
    #         'static/placeholder.png','static/placeholder.png','static/placeholder.png','static/placeholder.png']
    # profile_info[username] = []
    # profile_info[username].append(user_pic)
    # profile_info[username].append(bio)
    # profile_info[username].append(followers)
    # profile_info[username].append(following)

    #use this instead for when database is implemented
    all_profiles = profile_repo.get_profile_info()
    return render_template('profile.html', profiles = all_profiles)

    #return render_template("profile.html", profile_info = profile_info, posts = posts)

# Anessa's signup/login feature
@app.route('/')
def index():
    if request.method == 'GET' and request.form.get('signup'):
        return render_template('index.html', is_user=2)
    elif request.method == 'GET' and request.form.get('login'):
        return render_template('index.html', is_user=1, error=False)
    return render_template('index.html', is_user=0)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        email = request.form.get('email')
        dob = request.form.get('dob')
        profile_image = request.form.get('profile_image')
        with open(profile_image, 'rb') as file:
            image_data = file.read()
        uid = randint(1, 9999)

        new_user = {
            "uid": uid,
            "first_name": first_name,
            "last_name": last_name,
            "password": password, 
            "email": email,
            "dob": dob,
            "profile_image": image_data,
        }

        users[uid] = new_user

        return redirect(url_for('profile'))
    return render_template('index.html', is_user=2)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        for user in users:
            if user['email'] == email and user['password'] == password:
                return redirect(url_for('profile'))
        error_message = "Invalid email or password"
        return render_template('index.html', is_user=1, error=True, error_message=error_message)
    return render_template('index.html', is_user=1, error=False)
  
# Cindy's create a post feature
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        hashtags = request.form.get('hashtags')
        description = request.form.get('description')

        print("Title:", title)
        print("Price:", price)
        print("Hashtags:", hashtags)
        print("Description:", description)
        return "You have succesfully created a listing!"

    return render_template('create_post.html')

@app.route('/individual_post')
def show_post():
    post_image = 'static/blankpost.jpg'
    post_title = "Placeholder Title"
    post_price = "$Placeholder Price"
    post_description = "Placeholder Description"
    post_seller = " "
    return render_template('individual_post.html', post_image=post_image, post_title=post_title, post_price=post_price, post_description=post_description, post_seller=post_seller)

postGrid = {}
# Nhu's explore feature
@app.get('/explore')
def explore():
    all_posts = post_repo.get_all_posts()
    return render_template("explore.html", posts = all_posts)

# Nhu's search feature
@app.post('/search')
def search():
    value = request.form.get('query')
    search_result = post_repo.get_searched_posts(value)
    return render_template("search.html", search_result = search_result)


@app.route('/favorites', methods=["GET"])
def favorites():
    # will change this after pulling posts from database
    post = "static/blankpost.jpg"
    post_id = "post id"
    posts = ["static/blankpost.jpg", "static/blankpost.jpg", "static/blankpost.jpg", "static/blankpost.jpg", 
            "static/blankpost.jpg", "static/blankpost.jpg", "static/blankpost.jpg", "static/blankpost.jpg"]
    postGrid[post_id] = []
    postGrid[post_id].append(post)
    return render_template("favorites.html", postGrid = postGrid, posts = posts)

#Cayla's DM Feature

# Sample data
chats = [
    {'id': 1, 'user': 'User 1'},
    {'id': 2, 'user': 'User 2'},
    {'id': 3, 'user': 'User 3'},
]

chat_logs = [
    {'chat_id': 1, 'message': 'Hello, how are you?'},
    {'chat_id': 1, 'message': 'I\'m doing well, thanks!'},
    {'chat_id': 2, 'message': 'Hi there!'},
    {'chat_id': 2, 'message': 'What are you up to?'},
]

@app.route('/directmessages', methods=['GET', 'POST'])
def direct_messages():
    if request.method == 'POST':
        pass
    return render_template('directmessages.html', chats=chats, chat_logs=chat_logs)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)