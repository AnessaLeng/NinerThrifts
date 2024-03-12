from flask import Flask, render_template

app = Flask(__name__)

post = {
    "TI-84 Calculator": {
        "title": "TI-84 Calculator",
        "image": "/static/images/user_posted_images",
        "hashtags": "#calculator",
        "price": 30,
        "description": "Blue calculator, works properly, requires 4 AA batteries; batteries NOT included",
        "username": "_anessa"
    }
}

rating = {
    0: "/static/images/0_star.png",
    1: "/static/images/1_star.png",
    2: "/static/images/2_star.png",
    3: "/static/images/3_star.png",
    4: "/static/images/4_star.png",
    5: "/static/images/5_star.png"
}

reviews = {
    "reviewee": {
        "star_rating": rating.get(3),
        "reviewer": "anonymous",
        "reviewee": "_anessa",
        "comment": "The calculator didn't have batteries :("
    }
}

users = {
    "_anessa": {
        "username": "_anessa",
        "first_name": "Anessa",
        "last_name": "Leng",
        "password": 123, 
        "email": "aleng@uncc.edu",
        "dob": 5/6,
        "image": "/static/images/profile_images",
        "bio": "  m(._.)m  hello.",
        "following": 0,
        "followers": 0,
        "sold": 0,
        "rating": rating.get(3),
        "reviews": reviews.get("reviewee"),
        "listings": post.get("TI-84 Calculator"),
        "logged_in": False
    }
}

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/post/create', methods=['POST', 'GET'])
def create():
    return render_template('/post/create.html')

@app.route('/post/edit', methods=['POST', 'GET'])
def edit():
    return render_template('/post/edit.html')

@app.route('/post/show', methods=['POST', 'GET'])
def show():
    return render_template('/post/show.html')

@app.route('/loved', methods=['POST', 'GET'])
def loved():
    return render_template('loved.html')

@app.route('/messages', methods=['POST', 'GET'])
def messages():
    return render_template('messages.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    return render_template('profile.html')

@app.route('/profile/signup', methods=['POST', 'GET'])
def signup():
    return render_template('/user/signup.html')

@app.route('/profile/login', methods=['POST', 'GET'])
def login():
    return render_template('/user/login.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    return render_template('search.html')