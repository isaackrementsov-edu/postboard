# Isaac Krementsov
# 12/20/2019
# Software Development Fundamentals
# PostBoard - allows users to post images and quick notes online

# Import flask framework to run webserver
from flask import Flask, render_template, request, redirect

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

# Initialize JSON database
db = TinyDB('database.json')

# Handle all GET requests to / URL by obtaining posts for user
@app.route('/', methods=['GET'])
def getPosts():
    # Check for error data sent by other requests
    error = request.values.get('error');

    # Get the search term the user used
    filter = request.values.get('filter')
    # Create the empty array of posts to be returned
    posts = []

    try:
        # If the user had a search term, filter the posts by the term
        if filter:
            # Generate a query to search the database
            Post = Query()

            # Only select posts that contain the search term in their bodies or titles
            posts = db.search(Post.content.search(filter) | Post.title.search(filter))
        else:
            # If no search term, get all of the database
            posts = db.all()

        # Reverse the posts to sort chronologically
        posts.reverse()

        # Render the home template, auto-populate past query
        return render_template('home.html', posts=posts, query=filter, error=error)

    # In the case of any exception here, display a server error and do not attempt to show the post data
    except Exception:
        return render_template('home.html', posts=[], query=filter, error="Sorry, there was a server error")

# Handle POST request to the / URL by creating a post
@app.route('/', methods=['POST'])
def createPost():
    try:
        # Get the user's data for a post: its title, content, name, and image
        title = request.values.get('title')
        content = request.values.get('content')
        name = request.values.get('name')
        image = request.files['image']

        # If all of these fields were filled out, continue
        if title and content and name and image:
            # Create a dictionary to store the post's attributes
            post = dict(
                id = str(uuid.uuid1()), # Create a unique id to lookup posts later
                title = title,
                content = content,
                name = name,
                image_name = image.filename, # Store the name of the file uploaded so that it can be found again
                likes = 0
            )

            db.insert(post)

            fileUpload(image, app)

        # Redirect to the GET homepage method when done
        return redirect('/', code=302)

    # Break the program flow in case of any error saving the post
    except Exception:
        # Send the error data as a request query to be displayed on the homepage
        return redirect('/?error=Error%20saving%20post')

# Handle POST requests to /like by inrementing a post's likes
@app.route('/like', methods=['POST'])
def like():
    try:
        # Get the post unique id to find it
        post_id = request.values.get('post_id')

        # If this was submitted, update the appropriate post
        if post_id:
            Post = Query()
            # Incrmeent the post's likes  by 1
            db.update(increment('likes'), Post.id == post_id)


        # Redirect back to the homepage GET method
        return redirect('/', code=302)

    # In case there in an error updating likes, handle the exception
    except Exception:
        # Send the data forward to the homepage method
        return redirect('/?error=Error%20liking%20post', code=302)

# Run the app webserver
if __name__ == 'main':
    app.run()
