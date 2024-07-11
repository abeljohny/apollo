from flask import Flask, Response, render_template, request, stream_with_context

from arena import Arena
from config import Config
from database import Database

app = Flask(__name__)
db = Database()
config = Config()
arena = None

# def generate_chatbot_response():
#     # Simulate generating chatbot tokens with a delay
#     responses = [
#         "Hello",
#         "there!",
#         "How",
#         "can",
#         "I",
#         "help",
#         "you",
#         "today?"
#     ]
#     for token in responses:
#         time.sleep(0.5)  # Simulate delay in token generation
#         yield f"data:{token}\n\n"


@app.route("/")
def index():
    # return render_template("index.html")
    # global arena
    # arena = Arena("Why is the sun hot?", "gemma:latest,llama3:latest")
    return render_template("index.html")


@app.route("/prior")
def prior_conversations():
    return "Under active development!"


@app.route("/new", methods=["GET", "POST"])
def new_conversation():
    global arena
    if request.method == "POST":
        # selected_models = request.form.get(DatabaseKeys.MODELS.value)
        discussion_topic = request.form.get("comment")
        file = request.form.get("fileContents")
        global arena
        arena = Arena(discussion_topic, "gemma:latest,llama3:latest")
        return render_template("chat.html")
    #     arena = Arena(discussion_topic, selected_models)
    #     return render_template(
    #         "chat.html", selected_models=selected_models, topic=discussion_topic
    #     )
    # system_models = UtilLLM.available_models()
    # return render_template("config.html", models=system_models)


@app.route("/stream")
def stream():
    return Response(
        stream_with_context(arena.converse()),
        content_type="text/event-stream",
    )


if __name__ == "__main__":
    app.run(debug=True)
