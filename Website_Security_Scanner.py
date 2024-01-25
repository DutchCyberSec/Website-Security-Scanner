from flask import Flask, render_template, request, jsonify
import requests
import os
from werkzeug.utils import secure_filename
from urllib.parse import urljoin

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded successfully!'
        else:
            return 'Invalid file or file type not allowed.'

    ip = request.args.get('ip')
    website = request.args.get('website')

    if ip and website:
        ip = ip.strip()
        website = website.strip()
        if not (ip.isalnum() and website.isalnum()):
            return 'Invalid IP or website.'

        url = urljoin(f"http://{ip}/", website)
        response = requests.get(url)
        return f"Request sent to {url}. Response: {response.text}"

    return render_template('upload.html')

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
