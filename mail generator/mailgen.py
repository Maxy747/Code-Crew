# app.py
from flask import Flask, request, render_template
import gemini

app = Flask(__name__)

# Set your Gemini API key
gemini.api_key = 'AIzaSyDsp-Q1M2CM548oSCoAAO_UCAaeM2dOdVI'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_email', methods=['POST'])
def generate_email():
    prompt = request.form['prompt']
    response = gemini.Completion.create(
        engine="text-davinci-003",
        prompt=f"Write an email based on the following prompt: {prompt}",
        max_tokens=150
    )
    email_content = response.choices[0].text.strip()
    return render_template('index.html', prompt=prompt, email_content=email_content)

if __name__ == '__main__':
    app.run(debug=True)