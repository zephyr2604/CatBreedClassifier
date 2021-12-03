from flask import Flask, json, request, jsonify

from torch_utils import transform_image, get_prediction
app = Flask(__name__)


ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict',methods=['POST'])
def predict():
    #load image
    #transform it to tensor
    #make prediction
    #return json
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None or file.filename=="":
            return jsonify({'error':'no file'})
        if not allowed_file(file.filename):
            return jsonify({'error':'format not supported'})    
    
        try:
            img_bytes = file.read()
            tensor = transform_image(img_bytes)
            print("before pred")
            prediction = get_prediction(tensor)
            print("after pred")
            data = {'prediction':prediction}
            return jsonify(data)
        except:
            return jsonify({'error':'error during prediction'})

    return jsonify({'result':1})