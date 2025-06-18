from flask import Flask, render_template, url_for, request, redirect,abort
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
logger = app.logger

photo_members_dict = {}
UPLOAD_FOLDER = 'static/userData/images/'
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


@app.route('/sendNew', methods=['POST', 'GET'])
def createNewMember():
    if request.method == "POST":
        # param
        
        member_id = int(request.form.get('id'))
        if not member_id:
            abort(404)

        textAboutMember = request.form['textAboutMember']

        # save image

        f = request.files['image']
            
        filename = secure_filename(f.filename)  # Sanitize filename
        pathPhotoOnServ = os.path.join(UPLOAD_FOLDER, filename) # правильное создание пути
        f.save(os.path.join(app.root_path, pathPhotoOnServ)) # правильный save
            
        newMember = PhotoMember(member_id, pathPhotoOnServ, textAboutMember) #  Use correct member_id
        photo_members_dict[newMember.id] = newMember

        user_url = url_for('show_user_profile', user_id=member_id, _external=True) # Correct function name, id parameter
        return user_url, {'Content-Type': 'text/plain; charset=utf-8'}

    else:
        return render_template("testAdd.html")


@app.route('/user/<int:user_id>')
def show_user_profile(user_id):
    member = photo_members_dict.get(user_id)

    if not member:
            abort(404)

    if member is not None:
        return render_template('user.html', member=member)



def loadImage():
    pass


@app.errorhandler(404)
def error404(error):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(debug=True)
