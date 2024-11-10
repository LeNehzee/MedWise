from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import pytesseract
import google.generativeai as genai
from gtts import gTTS
import requests
import os
import json

# Configure your Google Generative AI API key
genai.configure(api_key="AIzaSyBtTPZg5XbRORR8srTWPGdyjeCiDlnSMNo")  # Replace with your Google API key

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"  # Folder for storing uploaded images
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if file is in request
    if 'file' not in request.files:
        return "No file uploaded.", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file.", 400

    # Save uploaded image
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Process the image with pytesseract
    image = Image.open(filepath)
    resultant_text = pytesseract.image_to_string(image)

    # Generate summary using Generative AI
    default_prompt = "Summarize the information from this text regarding medication, there might be random letters but it is safe to ignore. Explain briefly what function it serves. List the common uses of said medication."
    prompt = default_prompt + resultant_text
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    generated_text = response.text
    
    lang_choice = request.form.get('langChoice', '1')  # Default to English
    language = 'en' if lang_choice == '1' else 'zh-TW'
    summary_text = response.text
    if lang_choice == '2':  # If Chinese is selected, re-translate using the API
        translate_prompt = "Translate the following to Chinese: " + summary_text
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(translate_prompt)
        summary_text = response.text  # Reassign the translated summary text
    
    # Convert summary text to audio
    tts = gTTS(text=summary_text, lang=language, slow=False)
    audio_path = os.path.join("static", "audio", "medicine_summary.mp3")
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)  # Ensure directory exists
    tts.save(audio_path)

    # Get nearest healthcare locations from Geoapify API
    geoapify_url = "https://api.geoapify.com/v2/places?categories=healthcare&filter=circle:101.5920668,3.0513718,5000&bias=proximity:101.5920668,3.0513718&limit=20&apiKey=a38d47a9369642ca99480749f4933524"  # Replace with your Geoapify API key
    response = requests.get(geoapify_url)
    json_data = response.json()

    # Extract doctor information
    doctors_info = []
    for feature in json_data.get("features", []):
        name = feature["properties"].get("name", "Unknown")
        distance = feature["properties"].get("distance", "N/A")
        doctors_info.append(f"Name: {name}, Distance: {distance}")

    # Render results in the HTML template, passing the uploaded image filename
    return render_template('results.html', generated_text=summary_text, doctors_info=doctors_info, uploaded_image=file.filename, audio_path=audio_path)

if __name__ == '__main__':
    app.run(debug=True)
