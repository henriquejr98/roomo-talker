from flask import Flask
from flask_cors import CORS
from openai_assistant import ask

app = Flask(__name__)
CORS(app)

app.add_url_rule('/query_bot', 'query_bot', ask, methods=['POST'])


if __name__ == "__main__":
    app.run()