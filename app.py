from flask import Flask, redirect, render_template, request, url_for
from flask_socketio import SocketIO, emit
from random import randint
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Set Flask's secret key for DMs
socketio = SocketIO(app, secret_key=app.config['SECRET_KEY'])  # Set Flask-SocketIO's secret key for DMs

users = {} #DMs
messages = {} #Dms

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


# Cayla's DM Feature (the real one once i get the IDs to work)
# @app.route('/dm/<recipient_id>', methods=['GET', 'POST'])
# def direct_message(recipient_id):
#     if request.method == 'POST':
#         message = request.form.get('message')
#         sender = request.form.get('sender')  # Assuming you include sender in the form

#         if recipient_id in users:
#             if recipient_id not in messages:
#                 messages[recipient_id] = []
#             messages[recipient_id].append({'sender': sender, 'message': message})
#             emit('message', {'sender': sender, 'message': message}, room=recipient_id, broadcast=True)
#             return redirect(url_for('direct_message', recipient_id=recipient_id))
#         else:
#             return render_template('error.html', error_message='Recipient not found')

#     # Display DM page
#     if recipient_id in users:
#         if recipient_id in messages:
#             return render_template('directmessages.html', recipient_id=recipient_id, messages=messages[recipient_id])
#         else:
#             messages[recipient_id] = []  # Initialize empty messages for this recipient
#             return render_template('directmessages.html', recipient_id=recipient_id, messages=messages[recipient_id])
#     else:
#         return render_template('error.html', error_message='Recipient not found')
    
# @app.route('/dm', methods=['GET', 'POST'])
# def direct_message():
#     if request.method == 'POST':
#         message = request.form.get('message')
#         sender = request.form.get('sender')  
#         messages.append({'sender': sender, 'message': message})
#         return redirect(url_for('direct_message'))

#     # Display the DM page
#     return render_template('directmessages.html', messages=messages)
@app.route('/dm', methods=['GET'])
def direct_messages():
    # Display the DMs page without specifying a recipient
    return render_template('directmessages.html', messages=messages)


if __name__ == '__main__':
    socketio.run(app, debug=True)