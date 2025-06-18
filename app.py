from flask import Flask,render_template,url_for,request,redirect,make_response
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
logger = app.logger

photo_members_dict = {}
UPLOAD_FOLDER = 'static/userData/images/' 


class PhotoMember():
    id = 0
    pathPhotoOnServ = "defaultPath"
    textAboutMember = "InfoText"

    def __init__(self, id=0, pathPhotoOnServ="defaultPath", textAboutMember="InfoText"):
        self.id = id
        self.pathPhotoOnServ = pathPhotoOnServ
        self.textAboutMember = textAboutMember

    def __str__(self):
        return f"PhotoMember(id={self.id}, pathPhotoOnServ='{self.pathPhotoOnServ}', textAboutMember='{self.textAboutMember}')"



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sendNew', methods = ['POST','GET'])
def createNewMember():
    if request.method == "POST":
        #param
        id = int(request.form['id'])
        textAboutMember = request.form['textAboutMember']

        #save image
        f = request.files['image']
        pathPhotoOnServ = f'{UPLOAD_FOLDER}{secure_filename(f.filename)}'
        f.save(pathPhotoOnServ)


        newMember = PhotoMember( id, pathPhotoOnServ, textAboutMember)
        photo_members_dict[newMember.id] = newMember
    
        user_url = url_for('user', id=id, _external=True)  

        return user_url, {'Content-Type': 'text/plain; charset=utf-8'}  

    else:    
        return render_template("testAdd.html")
    
@app.route('/user/<int:user_id>')
def show_user_profile(user_id):
    member = photo_members_dict.get(user_id)
    if member is not None:
        return render_template('user.html', member=member)
    else:
        return redirect('/')
    

def loadImage():
    pass