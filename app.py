from flask import Flask, render_template, request
from random import random
#from repositories import post_repo

app = Flask(__name__)
profile_info = {}
users = {}

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

# Sample data
chats = [
    {'id': 1, 'user': 'User 1'},
    {'id': 2, 'user': 'User 2'},
    {'id': 3, 'user': 'User 3'},
]

chat_logs = [
    {'message': 'Hello, how are you?'},
    {'message': 'I\'m doing well, thanks!'},
    # Add more chat logs here
]

@app.route('/directmessages')
def direct_messages():
    return render_template('directmessages.html', chats=chats)

@app.route('/inbox/<int:chat_id>')
def inbox(chat_id):
    chat = next((chat for chat in chats if chat.id == chat_id), None)
    return render_template('inbox.html', chat=chat, chat_logs=chat_logs)

@app.route('/send_message', methods=['POST'])
def send_message():
    # Handle sending a message here
    pass

if __name__ == '__main__':
    socketio.run(app, debug=True)