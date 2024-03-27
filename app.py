from flask import Flask, render_template, request

app = Flask(__name__)
postGrid = {}

app.route('/')
def index():
    return render_template("index.html")

@app.route('/')
def explore():
    # will change this after pulling posts from database
    post = "static/blankpost.jpg"
    post_id = "post id"
    posts = ["static/blankpost.jpg", "static/blankpost.jpg", "static/blankpost.jpg", "static/blankpost.jpg", 
             "static/blankpost.jpg", "static/blankpost.jpg", "static/blankpost.jpg", "static/blankpost.jpg"]
    postGrid[post_id] = []
    postGrid[post_id].append(post)
    return render_template("explore.html", postGrid = postGrid, posts = posts)

@app.route('/search', methods=["POST"])
def search():
    search_result = request.form['query']
    #to do: get results from database
    return render_template("search.html", search_result = search_result)