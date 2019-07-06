import os
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
CORS(app)

items = [{'brand': 'Fender', 'model': 'Stratocaster'}]
items.append({'brand': 'Gibson', 'model': 'SG'})


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():

    print(request.files)
    if request.method == "POST":
        uploaded_files = request.files.getlist('images')
        print("Uploaded files:", uploaded_files,
              "Filename:", uploaded_files[0].filename)

        # check if the post request has the file part
        if 'file' not in request.files:

            print('No file part')
            return make_response("No File Part", 400)
        file = request.files["file"]
        # if user does not select file, browser also submit an empty part
        # without filename
        if file.filename == '':
            print('No selected file')
            return make_response("No Selected File", 400)
        if file and allowed_file(file.filename):
            # filenames can be dangerous!
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return make_response("Success", 201)


class Buy(Resource):
    def get(self):
        return items


class Sell(Resource):
    def post(self):
        print("test")
        print(Resource)
        print(request)
        return 200


api.add_resource(Buy, '/buy')
api.add_resource(Sell, '/sell')

if __name__ == '__main__':
    app.run(debug=True)
