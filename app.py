import os
import base64
from flask import Flask, redirect, render_template, request, send_from_directory, url_for, abort, session
from random import randint, random
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from repositories import post_repo, profile_repo, user_repo, message_repo
from repositories.favorites_repo import get_all_favorites, add_favorite, remove_favorite
from repositories.create_repo import create_post



load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')

socketio = SocketIO(app)

bcrypt = Bcrypt(app)
profile_info = {}
users = {}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = ''
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.template_filter('b64encode')
def b64encode_filter(data):
    print("Encoding image: " + base64.b64encode(data).decode('utf-8'))
    encoded_image = base64.b64encode(data).decode('utf-8')
    return encoded_image
    
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
    #all_profiles = profile_repo.get_profile_info()
    #return render_template('profile.html' , profiles = all_profiles)

    #return render_template("profile.html", profile_info = profile_info, posts = posts)

    email = request.args.get('email')
    user_profile = user_repo.get_user_by_email(email)
    if user_profile:
        profile_picture_data = user_profile['profile_picture']
        image_path = profile_picture_data.decode('utf-8')
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        # Encode the image data to Base64
        encoded_image_data = base64.b64encode(image_data).decode('utf-8')
        return render_template('profile.html' , profile=user_profile, encoded_profile_picture=encoded_image_data)
    else: 
        abort(404)

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
            abort(409, 'Email already exists')

        if 'profile_image' not in request.files:
            abort(400, 'No profile image provided')
        
        profile_image = request.files['profile_image']
        
        if profile_image.filename == '':
            abort(400, 'No profile image selected')
        
        if profile_image:
            filename = secure_filename(profile_image.filename)
            print("saving image: " + filename)
            print("loading image to uploads folder")
            profile_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profile_image.save(profile_image_path)
            print("path: " + profile_image_path)
        else:
            abort(400, 'Invalid file type or extension')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_repo.create_user(username, email, hashed_password, bio, first_name, last_name, dob, profile_image_path)
        return redirect(url_for('show_profile', email=email))
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
            return redirect(url_for('show_profile', email=email))
    return render_template('index.html', is_user=1, error=False)

# Cindy's create a post feature
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        condition = request.form.get('condition')
        body = request.form.get('description')

        user_id = session.get('user_id')
        username = session.get('username')

        create_post(user_id, username, title, body, price, condition)
        return "You have successfully created a post!"
        # possible mixup w description and body

    return render_template('create_post.html')

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

# @app.route('/directmessages', methods=['GET', 'POST'])
# def direct_messages():
#     if request.method == 'POST':
#         pass
#     return render_template('directmessages.html', chats=chats, chat_logs=chat_logs)

@app.route('/directmessages', methods=['GET', 'POST'])
def direct_messages():
    user = user_repo.get_current_user()
    chat_logs = {}
    if request.method == 'POST':
        recipient_id = request.form['recipient']
        message = request.form['message']
        # Add a new message to the chat_logs data structure
        if recipient_id not in chat_logs:
            chat_logs[recipient_id] = []
        chat_logs[recipient_id].append(message)
    chats = {}
    # Iterate over all the chat logs
    for recipient_id, messages in chat_logs.items():
        # For each recipient, find their user information and message history
        recipient = user_repo.get_user_by_id(recipient_id)
        chat_history = []
        for message in messages:
            chat_history.append({'sender': user, 'message': message})
        chats[recipient] = chat_history
    return render_template('directmessages.html', chats=chats, chat_logs=chat_logs)

@app.route('/messages/<int:recipient_id>')
def view_messages(recipient_id):
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get the logged-in user's ID
    sender_id = session.get('user_id')

    # Get or create the thread ID for the conversation between the sender and recipient
    thread_id = message_repo.get_or_create_thread(sender_id, recipient_id)

    # Fetch messages for the specified thread ID
    messages = message_repo.get_messages_for_thread(thread_id)

    # Fetch user information for both the sender and recipient
    sender = user_repo.get_user_by_id(sender_id)
    recipient = user_repo.get_user_by_id(recipient_id)

    # Render template to display messages
    return render_template('view_messages.html', messages=messages, sender=sender, recipient=recipient)

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    # You can store the user's connection information in the database
    # For example, you can update the user's status to 'online'
    user_repo.update_user_status(username, 'online')

@socketio.on("new_message")
def handle_new_message(data):
    sender_id = session.get('user_id')  # Get sender's user ID from session
    recipient_id = data.get('recipient_id')
    message_content = data.get('message_content')

    # Determine the thread ID based on the sender and recipient
    thread_id = message_repo.get_thread_id(sender_id, recipient_id)

    # If the thread doesn't exist, create a new one
    if not thread_id:
        thread_id = message_repo.create_thread(sender_id, recipient_id)

    # Insert the new message into the database with the thread ID
    message_repo.create_message(thread_id, sender_id, recipient_id, message_content)

    # Broadcast the new message to all clients
    emit("receive_message", {"thread_id": thread_id, "sender_id": sender_id, "message_content": message_content}, broadcast=True)

    # Emit a receive_message event to the sender's socket to display the new message automatically
    emit("receive_message", {"thread_id": thread_id, "sender_id": sender_id, "message_content": message_content}, room=sender_id)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    socketio.run(app)
