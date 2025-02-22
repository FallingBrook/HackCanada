from flask import Flask, request, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist


@app.route('/')
def home():
    return render_template("doctor.html")  # Ensure your HTML file is in "templates/"


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400
    file.filename = "image"
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)  # Save the image
    os.rename(filepath, "static/uploads/image.jpg")

    return f"File uploaded successfully! <br><img src='/{filepath}' width='300px'>"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
