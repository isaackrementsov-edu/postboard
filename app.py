from flask import Flask, render_template, request
from tinydb import TinyDB, Query
from tinydb.operations import increment
import uuid

from fileUpload import fileUpload

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/', methods=['GET'])
def getPosts():
    filter = request.value.get('filter')
    posts = []

    if filter:
        Post = Query()
        posts = db.search(filter in Post.content)
    else:
        posts = db.all()

    return render_template('home.html', posts=posts)

@app.route('/', methods=['POST'])
def createPost():
    title = request.value.get('title')
    content = request.value.get('content')
    name = request.value.get('name')
    image = request.files['image']

    if title and content and name and image:
        post = dict(
            id = uuid.uuid1()
            title = title,
            content = content,
            name = name,
            image_name = file.filename,
            likes = 0
        )

        db.insert(post)

        fileUpload(image, app)

    return redirect('/', code=302)

@app.route('/like', methods=['POST'])
    post_id = request.value.get('post_id')

    if post_id:
        Post = Query()
        db.update(increment('likes'), Post.id == post_id)

    return redirect('/', code=302)

if __name__ == 'main':
    app.run()
    db = TinyDB('database.json')
