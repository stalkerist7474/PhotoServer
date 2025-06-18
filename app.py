from flask import Flask, render_template, url_for, request, redirect,abort
from werkzeug.utils import secure_filename
import os
import datetime

app = Flask(__name__)
logger = app.logger

photo_members_dict = {}
UPLOAD_FOLDER = 'static/user-data/images/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class PhotoMember():
    def __init__(self, id=0, pathPhotoOnServ="defaultPath", textAboutMember="InfoText"):
        self.id = id
        self.pathPhotoOnServ = pathPhotoOnServ
        self.textAboutMember = textAboutMember

    def __str__(self):
        return f"PhotoMember(id={self.id}, pathPhotoOnServ='{self.pathPhotoOnServ}', textAboutMember='{self.textAboutMember}')"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/send-new', methods=['POST', 'GET'])
def createNewMember():
    if request.method == "POST":
        # param
        
        member_id = int(request.form.get('id'))
        if not member_id:
            abort(404)

        textAboutMember = request.form['textAboutMember']

        # save image

        f = request.files['image']

        # get format
        file_extension = os.path.splitext(f.filename)[1]  # e.g., ".jpg" or ".png"

        # get data
        now = datetime.datetime.now()
        date_string = now.strftime("%Y%m%d_%H%M%S")

        new_filename = f"{date_string}{file_extension}"

        filename = secure_filename(new_filename)
        pathPhotoOnServ = os.path.join(UPLOAD_FOLDER, filename) 
        f.save(os.path.join(app.root_path, pathPhotoOnServ)) 
        # end save image

        newMember = PhotoMember(member_id, pathPhotoOnServ, textAboutMember) 
        photo_members_dict[newMember.id] = newMember

        user_url = url_for('show_user_profile', user_id=member_id, _external=True) 
        return user_url, {'Content-Type': 'text/plain; charset=utf-8'}

    else:
        return render_template("test-add.html")


@app.route('/user/<int:user_id>')
def show_user_profile(user_id):
    member = photo_members_dict.get(user_id)

    if not member:
            abort(404)

    else:
        return render_template('user.html', member=member)



def loadImage():
    pass


@app.errorhandler(404)
def error404(error):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(debug=True)
