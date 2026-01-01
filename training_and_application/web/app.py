import os

import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

FINE_TUNED_MODEL = os.getenv('FINE_TUNE_MODEL_ID')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    readme_text = request.form.get('readme_text')

    system_prompt = (
        "You are an intelligent system that analyzes README files from "
        "Hugging Face models. Your task is to extract and classify 8 key "
        "components from the README content provided below. Identify whether "
        "each component is present or absent and provide the content of each "
        "present component."
    )

    response = openai.chat.completions.create(
        model=FINE_TUNED_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"README Content:\n---\n{readme_text}\n---"
            }
        ]
    )

    output_text = response.choices[0].message.content

    return render_template('result.html', output_text=output_text)


if __name__ == '__main__':
    app.run(debug=True)
