#!/usr/bin/env python
import os
import warnings
from flask import Flask, request, jsonify
from waitress import serve
from reddit_content_creator.crew import RedditContentCreator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# Initialize the Flask app
app = Flask(__name__)

# Define a sample route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Reddit content creator agent!"}), 200

# Define another route to handle POST requests
@app.route("/", methods=["POST"])
def data_handler():
    try:
        # Get JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        inputs = {
            'subreddit': data.get('subreddit'),
            'post_subject': data.get('post_subject')
        }
        result = RedditContentCreator().crew().kickoff(inputs=inputs)
        return result.raw, 200
        

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=os.environ.get("PORT", 8080))
