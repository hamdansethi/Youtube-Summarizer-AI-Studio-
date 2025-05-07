from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask import render_template


load_dotenv()

app = Flask(__name__)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/summarize", methods=["POST"])

def summarize():
    data = request.get_json()
    video_url = data.get("video_url")

    if not video_url:
        return jsonify({"error": "Missing video_url"}), 400

    try:
        video_id = video_url.split("v=")[-1].split("&")[0]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([t["text"] for t in transcript_list])

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(f"Summarize this YouTube transcript:\n{full_text}")

        return jsonify({"summary": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
