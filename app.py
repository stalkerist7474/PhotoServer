from flask import Flask, render_template, url_for, request, redirect,abort
from werkzeug.utils import secure_filename
import os
import datetime
import logging


UPLOAD_FOLDER = 'static/user-data/images/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#def create_app(testing: bool = True):
app = Flask(__name__)
logger = app.logger
app.logger.setLevel(logging.DEBUG)



@app.route('/')
def index():
    return render_template("index.html")



@app.route('/send-new', methods=['POST', 'GET'])
def createNewMember():
    if request.method == "POST":   

        # save image

        f = request.files['image']

        # get format
        file_extension = os.path.splitext(f.filename)[1]  # e.g., ".jpg" or ".png"

        # get data
        now = datetime.datetime.now()
        date_string = now.strftime("%Y%m%d%H%M%S")

        new_filename = f"{date_string}{file_extension}"

        filename = secure_filename(new_filename)
        pathPhotoOnServ = os.path.join(UPLOAD_FOLDER, filename) 
        f.save(os.path.join(app.root_path, pathPhotoOnServ)) 
        # end save image

        user_url = url_for('show_user_profile', user_id=date_string, _external=True) 

        app.logger.info('date_string: %s', date_string)

        return user_url, {'Content-Type': 'text/plain; charset=utf-8'}

    else:
        return render_template("test-add.html")



@app.route('/user/<int:user_id>')
def show_user_profile(user_id):

    imageFilePath = find_file_by_name_without_extension(UPLOAD_FOLDER,user_id)
    app.logger.info('imageFilePath: %s', imageFilePath)

    if imageFilePath == None:
            abort(404)

    else:
        return render_template('user.html', member=imageFilePath)



def find_file_by_name_without_extension(directory, filename_without_extension):

    if not os.path.exists(UPLOAD_FOLDER):
        app.logger.error('directory no found: %s', directory)
        return None
            
    for name in os.listdir(directory):
        if str(filename_without_extension) in name:
            app.logger.info('found: %s', name)
            return find_file_by_name(directory,name)

    return None



def find_file_by_name(directory, filename):
    for root, _, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)

    return None 



@app.errorhandler(404)
def error404(error):
    return render_template("404.html"), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
