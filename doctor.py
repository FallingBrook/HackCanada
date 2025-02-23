from flask import Flask, request, render_template
import os
import CancerClassifier  # Assuming this is a Python file that has a checkForCancer() function

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist


@app.route('/')
def home():
    return render_template("doctor.html")  # This is your HTML file for the front-end


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    # Create a new filename
    filename = "image"
    file_extension = file.filename.split('.')[-1]  # Get the file extension (e.g., 'jpg', 'png')

    # Make sure the new filename is unique by checking if the file exists
    counter = 1
    new_filename = f"{filename}.{file_extension}"

    while os.path.exists(os.path.join(UPLOAD_FOLDER, new_filename)):
        new_filename = f"{filename}_{counter}.{file_extension}"
        counter += 1

    # Define the file path where to save it
    filepath = os.path.join(UPLOAD_FOLDER, new_filename)

    # Save the file with the new name
    file.save(filepath)

    # Call the CancerClassifier and get the confidence score
    confidenceScore = CancerClassifier.checkForCancer(
        filepath)  # Assuming this function exists in the CancerClassifier file

    # Return the page with a success message and confidence score
    return render_template('doctor.html', confidenceScore=confidenceScore, image_url=f'/static/uploads/{new_filename}')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
