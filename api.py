import os.path

from flask import *

app = Flask(__name__)

UPLOAD_FOLDER = 'img_responses/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'text', 'png', 'jpg', 'jpeg', 'gif'}
#
#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def hello():
    return 'Hello PI'


@app.route('/img', methods=['POST'])
def upload_file():
    success = False
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No File'})
        resp.status_code = 400
        success = False
        return resp

    files = request.files.getlist('files[]')
    for file in files:
        if file and file.name:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            success = False

    if success:
        resp = jsonify({'message': 'Uploaded'})
        resp.status_code = 201
        return resp


if __name__ == '__main__':
    app.run(port=8090, debug=True)
