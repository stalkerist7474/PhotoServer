from flask import Flask,render_template,url_for,request,redirect

app = Flask(__name__)
logger = app.logger

photo_members_dict = {}


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
        id = int(request.form['id'])
        pathPhotoOnServ = request.form['pathPhotoOnServ']
        textAboutMember = request.form['textAboutMember']

        newMember = PhotoMember( id, pathPhotoOnServ, textAboutMember)
        photo_members_dict[newMember.id] = newMember

        return redirect('/')

    else:    
        return render_template("testAdd.html")
    
@app.route('/user/<int:user_id>')
def show_user_profile(user_id):
    member = photo_members_dict.get(user_id)
    if member is not None:
        return render_template('user.html', member=member)
    else:
        return redirect('/')