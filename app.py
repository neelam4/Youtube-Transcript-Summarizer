import json

import js
from flask import Flask, jsonify, make_response, abort, Response, request
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime
from transformers import T5ForConditionalGeneration, T5Tokenizer
from pydantic import BaseModel, parse
from pydantic_webargs import webargs
from urllib.parse import urlparse, parse_qs
import urllib.parse
from werkzeug.middleware.proxy_fix import ProxyFix

# define a variable to hold your app
app = Flask(__name__)


# defining 2 endpoints
@app.route('/')
def hello_world():
    return "Its working"


@app.route('/time', methods=['GET'])
def get_time():
    x = datetime.now()
    return str(x)


# Error handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/summarize/check', methods=['GET'])
# Get the transcript from the Youtube Transcript API
def transcript(video_id):
    Transc = YouTubeTranscriptApi.get_transcript(video_id)
    print(Transc)
    string = ''
    for i in Transc:
        string = string + i['text'] + ''
    print(string)
    resp = jsonify(Transc)
    resp.status = 200
    return string, resp


@app.route('/summarize/summary', methods=['GET'])
def summary(string):
    # initialize the model tokenizer
    tokenizer = T5Tokenizer.from_pretrained('t5-base')
    # initialize the model architecture and weights
    print("reached here")
    model = T5ForConditionalGeneration.from_pretrained('t5-base', force_download=True)

    # encode the text into tensor of integers using the appropriate tokenizer
    inputs = tokenizer.encode("summarize:" + string[0], return_tensors="pt", max_length=512, truncation=True)
    print(inputs)
    # generate the summarization output
    outputs = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4,
                             no_repeat_ngram_size=2, num_return_sequences=4,
                             early_stopping=True)
    print(outputs)
    print(tokenizer.decode(outputs[0]))

    return tokenizer.decode(outputs[0])


class QueryModel(BaseModel):
    name: str


class BodyModel(BaseModel):
    age: int


@app.route('/summarize/api', methods=['GET'])
def get_summarize(youtube_url):
    youtube_url = request.args.get('youtube_url')
    # youtube_url="https://www.youtube.com/watch?v=cs1e0fRyI18&list=RDcs1e0fRyI18&start_radio=1"
    url_data = urllib.parse.urlparse(youtube_url)
    query = urllib.parse.parse_qs(url_data.query)
    video_id = query["v"][0]
    print(video_id)
    # text = parse(str(video_id))
    id_u = transcript(video_id)
    print("this worked")
    sum = summary(id_u)
    data = {'responseText': sum}
    return jsonify(data), 200


# server the app when this file is run
if __name__ == '__main__':
    app.run(debug=True)
