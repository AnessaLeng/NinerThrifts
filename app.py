import os
from flask import session
from flask import Flask, redirect, render_template, request, send_from_directory, url_for, abort, session, flash
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from repositories import post_repo, profile_repo, user_repo, message_repo
from repositories.create_repo import create_post
import base64
import requests
from io import BytesIO


load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')

socketio = SocketIO(app)

bcrypt = Bcrypt(app)
profile_info = {}
users = {}


    
##Jaidens profile page
# @app.get('/profile')
# def show_profile():
#     if 'email' not in session:
#         return redirect(url_for('login'))
#     email = session['email']
#     posts = []
#     profile = profile_repo.get_profile_by_email(email)
#     # all_posts = post_repo.get_all_posts()
#     # for post in all_posts:
#     #     if(post['email'] == email):
#     #         posts.append(post)
#     user = user_repo.get_logged_in_user()
#     username = user['username']
#     posts = post_repo.get_posts_by_username(username)
#     return render_template('profile.html', profile = profile, posts = posts)

@app.get('/profile/<username>')
def show_profile(username):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    # Fetch profile information for the user whose profile is being viewed
    profile = profile_repo.get_profile_by_username(username)

    # Fetch posts associated with the user whose profile is being viewed
    posts = post_repo.get_posts_by_username(username)

    return render_template('profile.html', profile=profile, posts=posts)

@app.get('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')

@app.get('/updated_profile')
def updated_profile():
    user = user_repo.get_logged_in_user()
    username = user['username']
    return redirect(url_for('show_profile', username=username))


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
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        dob = request.form.get('dob')
        bio = request.form.get('biography')

        if user_repo.does_email_exist(email):
            return render_template('error.html', error_message='409: Email already exists.'), 409

        if 'profile_picture' not in request.files:
            return render_template('error.html', error_message='400: No profile image provided.'), 400
        
        profile_picture = request.files['profile_picture']
        api_key = os.getenv('API_KEY')
        upload_url = 'https://api.imgbb.com/1/upload'
        if profile_picture.filename == '':
            return render_template('error.html', error_message='400: No profile image selected.'), 400
        payload = {
            'key': api_key,
            'image': base64.b64encode(profile_picture.read())
        }
        response = requests.post(upload_url, data=payload)

        if response.status_code == 200:
            json_response = response.json()
        else:
            return render_template('error.html', error_message='500: Internal Server Error: Failed to upload profile image to ImgBB.'), 500

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_repo.create_user(username, email, hashed_password, bio, first_name, last_name, dob, json_response['data']['url'])
        session['email'] = email
        session['username'] = username
        user = user_repo.get_user_by_email(email)
        return redirect(url_for('show_profile', username=user['username']))
    return render_template('index.html', is_user=2)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            error_message = "Invalid email or password"
            return render_template('index.html', is_user=1, error=True, error_message=error_message)
        user = user_repo.get_user_by_email(email)
        if user is not None:
            session['email'] = email
            session['username'] = user['username']
            return redirect(url_for('show_profile', username=user['username']))
    return render_template('index.html', is_user=1, error=False)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Cindy's create a post feature
@app.route('/create_post', methods=['GET', 'POST'])
def create_listing():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        condition = request.form.get('condition')
        body = request.form.get('description')
        post_image = request.files['myFile']

        user = user_repo.get_logged_in_user()
        username = user['username']
        print(post_image)

        api_key = os.getenv('API_KEY')
        upload_url = 'https://api.imgbb.com/1/upload'
        data = {
                'key': api_key,
                'image': base64.b64encode(post_image.read())
            }
        response = requests.post(upload_url, data=data)
        print(response)

        if response.status_code == 200:
            json_response = response.json()
            print(json_response)
            create_post(username, title, body, price, condition, json_response['data']['url'])
            return redirect(url_for('show_profile', username=username))
    return render_template('create_post.html')

# Edit post route
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = post_repo.get_post_by_id(post_id)
    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']
        new_price = request.form['price']
        new_condition = request.form['condition']
        
        # Handle file upload for image if provided
        if 'myFile' in request.files:
            post_image = request.files['myFile']
            api_key = os.getenv('API_KEY')
            upload_url = 'https://api.imgbb.com/1/upload'
            data = {
                    'key': api_key,
                    'image': base64.b64encode(post_image.read())
                }
            response = requests.post(upload_url, data=data)
            if response.status_code == 200:
                json_response = response.json()
                new_image_url = json_response['data']['url']
                post_repo.update_post(post_id, new_title, new_body, new_price, new_condition, new_image_url)
            else:
                flash('Failed to upload new image for post', 'error')
        else:
            # If no new image is provided, update post without changing the image URL
            post_repo.update_post(post_id, new_title, new_body, new_price, new_condition)
        
        flash('Post updated successfully', 'success')
        return redirect(url_for('show_individual_post', post_id=post_id))
    return render_template('edit_post.html', post=post)


# Delete post route


@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    # Check if the request method is POST
    if request.method == 'POST':
        # Fetch the post being deleted
        post = post_repo.get_post_by_id(post_id)

        # Check if the post exists
        if post:
            # Delete the post from the database
            post_repo.delete_post(post_id)
            flash('Post deleted successfully', 'success')
            return redirect(url_for('show_profile', username=session['username']))
        else:
            # If the post does not exist, display an error message
            flash('Post not found', 'error')
            return redirect(url_for('explore'))  # Redirect to the explore page
    else:
        # If the request method is not POST, redirect to an error page
        flash('Invalid request method', 'error')
        return redirect(url_for('explore'))  # Redirect to the explore page


@app.route('/individual_post')
def show_individual_post():
    post_id = request.args.get('post_id')
    post = post_repo.get_post_by_id(post_id)
    return render_template('individual_post.html', post=post)

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


# @app.route('/favorites', methods=["GET"])
# def favorites():
#     # will change this after pulling posts from database
#     postGrid = {}
#     post = "static/blankpost.jpg"
#     post_id = "post id"
#     posts = ["static/blankpost.jpg", "static/blankpost.jpg", "static/blankpost.jpg", "static/blankpost.jpg", 
#             "static/blankpost.jpg", "static/blankpost.jpg", "static/blankpost.jpg", "static/blankpost.jpg"]
#     postGrid[post_id] = []
#     postGrid[post_id].append(post)
#     return render_template("favorites.html", postGrid = postGrid, posts = posts)


# Cindy's favorites feature
# @app.route('/favorites')
# def favorites():
#     all_favorites = get_all_favorites()
#     return render_template("favorites.html", favorites=all_favorites)

# @app.route('/add_favorite', methods=['POST'])
# def add_favorite():
#     if request.method == 'POST':
#         user_id = request.form.get('user_id')
#         post_id = request.form.get('post_id')
#         add_favorite(user_id, post_id)
#         return redirect(url_for('favorites'))

# @app.route('/remove_favorite', methods=['POST'])
# def remove_favorite():
#     if request.method == 'POST':
#         user_id = request.form.get('user_id')
#         post_id = request.form.get('post_id')
#         remove_favorite(user_id, post_id)
#         return redirect(url_for('favorites'))

#Cayla's DM Feature


@app.route('/directmessages', methods=['GET'])
def direct_messages():
    query = request.args.get('q')
    if query:
        users = user_repo.search_users(query)
    else:
        users = user_repo.get_all_users()
    return render_template('directmessages.html', users=users)

@app.route('/chatlog/<recipient_username>', methods=['GET'])
def chatlog(recipient_username):
    # Check if user is logged in
    if 'username' not in session:
        # Redirect to login page
        return redirect(url_for('login'))
    
    # Get the logged-in user's ID
    sender_username = session.get('user_id')

    # Fetch messages for the specified thread ID
    thread_id = message_repo.get_thread_id(sender_username, recipient_username)
    messages = message_repo.get_messages_for_thread(thread_id)

    # Fetch user information for both the sender and recipient
    sender = user_repo.get_user_by_username(sender_username)
    recipient = user_repo.get_user_by_username(recipient_username)

    # Render template to display messages
    return render_template('chatlog.html', messages=messages, sender=sender, recipient=recipient)

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    user_repo.update_user_status(username, 'online')

@socketio.on("new_message")
def handle_new_message(data):
    sender_username = session.get('user_id')  # Get sender's user ID from session
    recipient_username = data.get('recipient_username')
    message_content = data.get('message_content')
    # Determine the thread ID based on the sender and recipient
    thread_id = message_repo.get_thread_id(sender_username, recipient_username)
    # If the thread doesn't exist, create a new one
    if not thread_id:
        thread_id = message_repo.create_thread(sender_username, recipient_username)
    # Insert the new message into the database with the thread ID
    message_repo.create_message(thread_id, sender_username, recipient_username, message_content)
    # Broadcast the new message to all clients
    emit("receive_message", {"thread_id": thread_id, "sender_username": sender_username, "message_content": message_content}, broadcast=True)
    # Emit a receive_message event to the sender's socket to display the new message automatically
    emit("receive_message", {"thread_id": thread_id, "sender_username": sender_username, "message_content": message_content}, room=sender_username)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    socketio.run(app)