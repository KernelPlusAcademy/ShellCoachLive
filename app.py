from flask import Flask, request, render_template
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    explanation = ""
    if request.method == "POST":
        command = request.form.get("command", "")
        prompt = f"Explain this Linux command in simple terms and flag any risks: {command}"
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            explanation = response.choices[0].message.content.strip()
        except Exception as e:
            explanation = f"Error: {str(e)}"
    return render_template("index.html", explanation=explanation)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
