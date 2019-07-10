import os
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pathlib import Path

UPLOAD_DIR: Path = Path(__file__).parent / 'uploads'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
api = Api(app)
CORS(app)

items = [{'brand': 'Fender', 'model': 'Stratocaster'}]
items.append({'brand': 'Gibson', 'model': 'SG'})


def is_valid_upload(upload) -> bool:
    # some validation logic
    return Path(upload.filename).suffix.lower() in ['.jpg', '.jpeg']


@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == "POST":
        uploaded_files = request.files.getlist('images')
        print(uploaded_files)
        if not uploaded_files or not uploaded_files[0].filename:
            return 'invalid request', 400

        valid_uploads = list(filter(is_valid_upload, uploaded_files))
        if not valid_uploads:
            return 'invalid image(s)', 400

        for upload in valid_uploads:
            filename = secure_filename(upload.filename)
            save_path = str(UPLOAD_DIR / filename)

            upload.save(save_path)

        return 'uploaded'


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
