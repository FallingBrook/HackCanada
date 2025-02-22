from flask import Flask, request, jsonify, render_template
import Perplexity
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML
 # Serve the HTML

@app.route('/process_medi', methods=['POST'])
def process_medi():
    data = request.json
    user_text = data.get("text", "")
    print("Processing medi AI")
    user_text = Perplexity.GetAiDoctorResp(user_text)

    return jsonify({"result": user_text})


@app.route('/process_poopy', methods=['POST'])
def process_poopy():
    print("Processing poopy AI")

    data = request.json
    user_message = data.get("message", "")



    user_message = Perplexity.GetAiTherapistResp(user_message)

    return jsonify({"response": user_message})

if __name__ == '__main__':
    app.run(debug=True)
