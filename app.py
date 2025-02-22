from flask import Flask, request, jsonify, render_template
import Perplexity
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML
 # Serve the HTML

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    user_text = data.get("text", "")

    user_text = Perplexity.GetPerplexityResponse(user_text, "Respond as a doctor. Make suggestions based on the symptoms given. Respond in under 100 words no matter what.")

    return jsonify({"result": user_text})

if __name__ == '__main__':
    app.run(debug=True)
