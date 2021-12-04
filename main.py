from flask import Flask, json, request, jsonify, render_template, flash, redirect, url_for
import os
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from PIL import Image

from torch_utils import transform_image, get_prediction
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "i-dont-know-bro"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'jpg'}
CAT_IMAGE = "cat.jpg"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        #Clean all files
        filelist = [ f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith(".jpg") ]
        for f in filelist:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        #flash('Image successfully uploaded')
        prediction = predict(filename)
        flash('The predicted breed is : '+prediction.upper())
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - jpg')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/predict',methods=['POST'])
def predict(filename):
    #load image
    #transform it to tensor
    #make prediction
    #return json
    print("inside predict file:" + filename)
    if request.method == 'POST' or 1:
        file = request.files.get('file')
        #file=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as fp:
        #    file = FileStorage(fp)
        #file = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        #if file is None or file.filename=="":
        #    return jsonify({'error':'no file'})
        #if not allowed_file(file.filename):
         #   return jsonify({'error':'format not supported'})    
        #print("inside if file:" + file)

        #try:
        #print("inside try file:" + file)
        #img_bytes = file.read()
        img_bytes = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb').read()
        tensor = transform_image(img_bytes)
        print("before pred")
        prediction = get_prediction(tensor)
        print("after pred")
        data = {'prediction':prediction}
        #return jsonify(data)
        return prediction
        #except:
        #    print("inside except file:" + file)
        #    return jsonify({'error':'error during prediction'})

#return jsonify({'result':1})

if __name__ == "__main__":
    app.run()