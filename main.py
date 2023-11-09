from flask import Flask, render_template, request , flash
from werkzeug.utils import secure_filename
import os
import cv2



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename,operation):
    print(f"operation : {operation} and file name : {filename} " )
    
    img=cv2.imread(f"uploads/{filename}")
    match operation:
        case '1':
            nfile=f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(nfile, img)
            return nfile

        case '2':
            imgP=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            nfile=f"static/{filename}"
            cv2.imwrite(nfile, imgP)
            return nfile
        case '3':
            nfile=f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(nfile, img)
            return nfile
        case '4':
            nfile=f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(nfile, img)
            return nfile


app = Flask(__name__)
app.secret_key='super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/edit", methods=["POST"])
def about():
    operation = request.form.get('operation')
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return 
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return "ERROR"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename,operation)
            flash(f"Processed Image <a href ='/{new}'> here </a>")
            return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)