import os
import openai
from flask import Flask, jsonify, request
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)
CORS(app)

openai.api_key = os.environ["OPENAI_API_KEY"]

def summarize_text(text):
    print(f'Text to be summarized: {text}')  # Add this line to print the text
    prompt = f'''understand what the youtubers want to convey and give summary of all important concepts in the video in bullet points: {text}''';
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=600,

    )
    # Rest of the code...


    return response.choices[0].message

@app.route('/transcript/<video_id>', methods=['GET'])
def get_transcript(video_id):
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item["text"] for item in transcript_data])
        summary = summarize_text(transcript)
        
        return jsonify({"transcript": transcript, "summary": summary})
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True)
