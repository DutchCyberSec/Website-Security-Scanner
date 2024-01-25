from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save('uploads/' + file.filename)
        return 'File uploaded successfully!'

    ip = request.args.get('ip')
    website = request.args.get('website')

    if ip and website:
        response = requests.get(f"http://{ip}/{website}")
        return f"Request sent to {ip}/{website}. Response: {response.text}"

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
