from flask import Flask, render_template, request, Response, stream_with_context
import time
from llm_helpers import available_models

app = Flask(__name__)


def generate_chatbot_response():
    # Simulate generating chatbot tokens with a delay
    responses = [
        "Hello",
        "there!",
        "How",
        "can",
        "I",
        "help",
        "you",
        "today?"
    ]
    for token in responses:
        time.sleep(0.5)  # Simulate delay in token generation
        yield f"data:{token}\n\n"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/prior')
def prior_conversations():
    return 'Under active development!'


@app.route('/new', methods=["GET", "POST"])
def new_conversation():
    if request.method == "POST":
        selected_models = request.form.get("models")
        topic = request.form.get("topic")
        return render_template("chat.html", selected_models=selected_models, topic=topic)
    system_models = available_models()
    return render_template("config.html", models=system_models)


@app.route("/stream")
def stream():
    return Response(stream_with_context(generate_chatbot_response()), content_type='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)
