# Import the OS module to interact with the file system in any OS
import os

# File upload function for external use; made into its own module in case it changes later
def fileUpload(file, app):
        # Save the file to the app's upload folder with its filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
