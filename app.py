from flask import Flask,render_template,url_for,request

app = Flask(__name__)
logger = app.logger

photo_members_dict = {}


class PhotoMember():
    id = 0
    pathPhotoOnServ = "defaultPath"
    textAboutMember = "InfoText"

    def __init__(self, id=0, pathPhotoOnServ="defaultPath", textAboutMember="InfoText"):
        """
        Конструктор класса PhotoMember.

        Args:
            id (int, optional): Уникальный идентификатор участника. Defaults to 0.
            pathPhotoOnServ (str, optional): Путь к фотографии участника на сервере. Defaults to "defaultPath".
            textAboutMember (str, optional): Текстовая информация об участнике. Defaults to "InfoText".
        """
        self.id = id
        self.pathPhotoOnServ = pathPhotoOnServ
        self.textAboutMember = textAboutMember

    def __str__(self):
        """
        Возвращает строковое представление объекта для удобной отладки.
        """
        return f"PhotoMember(id={self.id}, pathPhotoOnServ='{self.pathPhotoOnServ}', textAboutMember='{self.textAboutMember}')"



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sendNew', methods = ['POST','GET'])
def createNewMember():
    if request.method == "POST":
        id = request.form['id']
        pathPhotoOnServ = request.form['pathPhotoOnServ']
        textAboutMember = request.form['textAboutMember']

        newMember = PhotoMember( id, pathPhotoOnServ, textAboutMember)
        photo_members_dict[newMember.id] = newMember

        logger.debug(newMember.id)
        logger.debug(newMember.pathPhotoOnServ)
        logger.debug(newMember.textAboutMember)

    else:    
        return render_template("testAdd.html")