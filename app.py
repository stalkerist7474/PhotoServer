from flask import Flask, render_template, url_for, request, redirect,abort
from werkzeug.utils import secure_filename
import os
import datetime
import logging
from PIL import Image


UPLOAD_FOLDER = 'static/user-data/images/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
logger = app.logger
app.logger.setLevel(logging.DEBUG)



@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")



@app.route('/send-new/', methods=['POST', 'GET'])
def create_new_member():
    if request.method == "POST":   
        image = request.files.get('image')

        if image == None:
            abort(404)
    
        now = datetime.datetime.now()
        date_string = now.strftime("%Y%m%d%H%M%S")
        convert_and_save_jpeg(image, date_string )

        user_url = url_for('show_user_profile', user_id=date_string, _external=True)        
        app.logger.info(f'date_string: {date_string}')
        return user_url, {'Content-Type': 'text/plain; charset=utf-8'}
    else:
        return render_template("test-add.html")



@app.route('/user/<int:user_id>/')
def show_user_profile(user_id):

    name_file = f'{user_id}.jpeg'
    path = f'{UPLOAD_FOLDER}{name_file}'

    #No file
    if not os.path.exists(path):
        app.logger.error(f'directory no found: {path}')
        abort(404)
        return None

    #Yes file
    else:
        app.logger.info(f'imageFilePath: {path}' )
        return render_template('user.html', member=path)


def convert_and_save_jpeg(image_data, new_name):
    
    img = Image.open(image_data)
    if img.mode != "RGB":
        img = img.convert("RGB")

    filename = str(new_name) + ".jpeg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    img.save(filepath, "JPEG")

    return filename
      

@app.errorhandler(404)
def error404(error):
    return render_template("404.html"), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
