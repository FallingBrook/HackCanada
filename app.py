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
    user_text = Perplexity.GetPerplexityResponse(user_text, "Respond as a doctor. Make suggestions based on the symptoms given. Respond in under 100 words no matter what.")

    return jsonify({"result": user_text})


@app.route('/process_poopy', methods=['POST'])
def process_poopy():
    data = request.json
    user_text2 = data.get("text", "")
    print("Processing poopy AI")
    user_text2 = Perplexity.GetPerplexityResponse(user_text2, "Be super rude and answer with 1 or 2 words max")

    return jsonify({"result": user_text2})

if __name__ == '__main__':
    app.run(debug=True)
