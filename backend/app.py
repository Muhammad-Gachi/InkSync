print("APP.PY IS RUNNING")
import os
import base64
from flask import Flask, request, send_file
from docx import Document
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/upload", methods=["POST"])
def upload():
    # Get uploaded image
    file = request.files["image"]
    image_path = os.path.join("uploads", file.filename)
    file.save(image_path)

    # Convert image to base64
    with open(image_path, "rb") as img:
        base64_image = base64.b64encode(img.read()).decode("utf-8")

    # Send to GPT‑4o for handwriting transcription
    result = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Transcribe the handwriting in this image."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )

    # Extract text from GPT response
    text = result.choices[0].message.content

    # Create Word document
    doc = Document()
    doc.add_paragraph(text)
    output_path = os.path.join("output", "converted.docx")
    doc.save(output_path)

    # Return the file to the frontend
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)