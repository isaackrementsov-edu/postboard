# Isaac Krementsov
# 12/20/2019
# Software Development Fundamentals
# PostBoard - allows users to post images and quick notes online

# Import flask framework to run webserver
from flask import Flask, render_template, request

# Import tinydb to store post data
from tinydb import TinyDB, Query
from tinydb.operations import increment

# Import uuid to generate unique ids
import uuid

# This is an internal module to upload files
from fileUpload import fileUpload

# Initialize flask application and set the upload folder
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Handle all GET requests to / URL by obtaining posts for user
@app.route('/', methods=['GET'])
def getPosts():
    # Get the search term the user used
    filter = request.value.get('filter')
    # Create the empty array of posts to be returned
    posts = []

    # If the user had a search term, filter the posts by the term
    if filter:
        Post = Query()

        # Only select posts that contain the search term in their bodies or titles
        posts = db.search(filter in Post.content | filter in Post.title)
    else:
        # If no search term, get all of the database
        posts = db.all()

    # Render the home template no matter what
    return render_template('home.html', posts=posts)

# Handle POST request to the / URL by creating a post
@app.route('/', methods=['POST'])
def createPost():
    # Get the user'sc data for a post: its title, content, name, and image
    title = request.value.get('title')
    content = request.value.get('content')
    name = request.value.get('name')
    image = request.files['image']

    # If all of these fields were filled out, continue
    if title and content and name and image:
        # Create a dictionary to store the post's attributes
        post = dict(
            id = uuid.uuid1(), # Create a unique id to lookup posts later
            title = title,
            content = content,
            name = name,
            image_name = file.filename, # Store the name of the file uploaded so that it can be found again
            likes = 0
        )

        db.insert(post)

        fileUpload(image, app)

    # Redirect to the GET homepage method when done
    return redirect('/', code=302)

# Handle POST requests to /like by inrementing a post's likes
@app.route('/like', methods=['POST'])
    # Get the post unique id to find it
    post_id = request.value.get('post_id')

    # If this was submitted, update the appropriate post
    if post_id:
        Post = Query()
        # Incrmeent the post's likes  by 1
        db.update(increment('likes'), Post.id == post_id)


    # Redirect back to the homepage GET method
    return redirect('/', code=302)

# Run the app webserver and initialize the JSON database
if __name__ == 'main':
    app.run()
    db = TinyDB('database.json')
