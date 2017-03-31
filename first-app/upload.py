import os
from flask import Flask, request, redirect, url_for, send_from_directory
from flask import render_template, jsonify, abort, make_response
from werkzeug.utils import secure_filename


CODE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.dirname(CODE_DIR))

UPLOAD_FOLDER = os.path.join(PROJECT_DIR, 'uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg'])

MAX_CONTENT_LENGTH = 1024 ** 3

app = Flask(__name__)
app.config.update(DEBUG=True, TESTING=True, PROPAGATE_EXCEPTIONS=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH



@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html', filelist=generate_filelist())

    # check if the post request has the file part
    if 'file' not in request.files:
        abort(400, {'message': 'no file in the request'})

    file = request.files['file']
    if file.filename == '':
        abort(400, {'message': 'invalid file'})
    if not file or not allowed_file(file.filename):
        abort(400, {'message': 'filename is not allowed'})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(filepath):
        abort(409, {'message': 'File with same name already uploaded.'})
    file.save(filepath)
    filesize = stringify_filesize(os.path.getsize(filepath))
    return jsonify(
        url=url_for('download_file', filename=filename),
        name=filename,
        size = filesize
    )


@app.route('/files/')
def get_files():
    files_uploaded = generate_filelist()
    return jsonify(files_uploaded)

@app.route('/files/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(400)
def custom400(error):
    return make_response(jsonify({'message': error.description['message']}),400)

@app.errorhandler(409)
def custom409(error):
    return make_response(jsonify({'message': error.description['message']}),409)

def allowed_file(filename):
    """ return True if the filename is acceptable """
    return '.' in filename

def stringify_filesize(size):
    suffix = None
    if size >= 1073741824:
        size /= 1073741824
        suffix = 'GB'
    elif size >= 1048576:
        size /= 1048576
        suffix = 'MB'
    elif size >= 1024:
        size /= 1024
        suffix = 'KB'
    else:
        suffix = 'B'
    return str(round(size,2)) + suffix

def generate_filelist():
    files_uploaded = list()
    for name in os.listdir(app.config['UPLOAD_FOLDER']):
        file_dict = dict()
        file_dict['name'] = name
        file_dict['url'] = url_for('download_file', filename=name)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], name)
        file_dict['size'] = stringify_filesize(os.path.getsize(filepath))
        files_uploaded.append(file_dict)
    return files_uploaded

if __name__ == '__main__':
    app.run()