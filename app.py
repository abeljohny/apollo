from flask import Flask, Response, render_template, request, stream_with_context

from arena import Arena
from config import Config
from constants import ElementNames, Templates
from database import Database
from util import Util

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
    return render_template(Templates.INDEX.value)


@app.route("/new", methods=["GET", "POST"])
def new_conversation():
    global arena
    if request.method == "POST":
        # selected_models = request.form.get(DatabaseKeys.MODELS.value)
        discussion_topic = request.form.get(ElementNames.DISCUSSION_TOPIC.value)
        file = request.form.get(ElementNames.FILE_CONTENTS.value)
        global arena
        arena = Arena(discussion_topic, config)
        return render_template(Templates.CHAT.value)
    #     arena = Arena(discussion_topic, selected_models)
    #     return render_template(
    #         "chat.html", selected_models=selected_models, topic=discussion_topic
    #     )
    # system_models = UtilLLM.available_models()
    # return render_template("config.html", models=system_models)


@app.route("/stream")
def stream():
    global arena
    return Response(
        stream_with_context(arena.execute()),
        content_type="text/event-stream",
    )


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        sysprompt = request.form.get(ElementNames.SYSPROMPT.value)
        max_n_o_turns = request.form.get(ElementNames.MAX_N_O_TURNS.value)
        selected_agents = request.form.getlist(ElementNames.SELECTED_AGENTS.value)
        agent_behavior = request.form.get(ElementNames.AGENT_BEHAVIOR.value)
        config.set_system_prompt(sysprompt)
        config.set_max_turns(int(max_n_o_turns))
        config.set_agents(selected_agents)
        config.set_agent_behavior(agent_behavior)

    return render_template(
        Templates.SETTINGS.value,
        models=Util.available_system_models(),
        behaviors=Util.agent_behaviors(),
        sysprompt=config.system_prompt,
        max_turns=config.max_n_o_turns,
        default_models=config.selected_agents,
    )


@app.route("/prior")
def prior_conversations():
    return "Under active development!"


if __name__ == "__main__":
    app.run(debug=False)
