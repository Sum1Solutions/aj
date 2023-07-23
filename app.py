from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        prompt = request.json['prompt']
    except KeyError as e:
        return jsonify({'error': f"Invalid JSON payload: Missing 'prompt' field. {e}"}), 400

    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.5,
            max_tokens=100
        )
    except Exception as e:
        return jsonify({'error': f"Error generating text with OpenAI: {e}"}), 500

    try:
        generated_text = response['choices'][0]['text'].strip()
    except Exception as e:
        return jsonify({'error': f"Error parsing OpenAI response: {e}"}), 500

    return jsonify({'generated_text': generated_text})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
