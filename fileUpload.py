import os;

def fileUpload(file, app):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
