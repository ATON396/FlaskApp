import os
from markupsafe import Markup, escape
from werkzeug.utils import secure_filename
from flask import Flask ,render_template, redirect, url_for, flash, request, send_from_directory

# PartUploadFunction
UPLOAD_FOLDER = './UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','docx','mp3', 'mp4'}

app = Flask(__name__)

# PartUploadFunction
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



# Rutas Erros 404
@app.errorhandler(404)
def page_not_found(error):
    titlePage = '| Page Not Found 404'
    return render_template('page_not_found.html', titlePage= titlePage), 404
# Fin Rutas Erros 404


# Rutas index
@app.route('/')
def index():

    titlePage = '| The Aton Code Blog'
    text = { 'content': 'Welcome to Aton Code' }  
    Titleparagraf ={'content': 'The WarGames Movie'}
    paragrafOne= {'content': 'Movie in Spanish'}

    Titleparagraf2= {'content': 'The BrainStrom Movie'} 
    paragraf2= {'content': 'Movie in Spanish'}
   
    return render_template(

        "index.html",
        titlePage= titlePage, 
        paragrafOne= paragrafOne,
        text = text,
        Titleparagraf=Titleparagraf,
        Titleparagraf2=Titleparagraf2,
        paragraf2=paragraf2
        
        )
    
# Fin Rutas index


# Ruta Interactiva
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    print(username)
    return 'User %s' % escape(username)
# Fin Ruta Interactiva
 

# Upload Files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
#---------------HTML-------------------------------#
    titlePage= '| Upload New File'

#---------------------------------------------------#
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename=filename))

    return render_template('upload.html', titlePage= titlePage)


filename = "../../../../home/username/.bashrc"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

# Fin UploadFile


if __name__ == "__main__":
    app.run()