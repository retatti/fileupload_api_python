import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from fileupload import fileupload

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/uploadpdf", methods=["POST"])
def upload():
    if 'slide' not in request.files:
        return redirect('/')
    
    slide = request.files['slide']

    if slide.filename == '':
        return redirect('/')
    if slide and allowed_file(slide.filename):
        filename = secure_filename(slide.filename)
        fpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        slide.save(fpath)
        fileupload(fpath, filename)
        os.remove(fpath)
        return redirect('/')

    return redirect(request.url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)