from flask import (
    Flask,
    Response,
    jsonify,
    render_template,
    request,
    stream_with_context,
)

from agent import Agent
from arena import Arena
from config import Config
from constants import ElementNames, Templates
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
    return render_template(Templates.INDEX.value)


@app.route("/new", methods=["GET", "POST"])
def new_conversation():
    global arena
    if request.method == "POST":
        # selected_models = request.form.get(DatabaseKeys.MODELS.value)
        discussion_topic = request.form.get(ElementNames.DISCUSSION_TOPIC.value)
        if discussion_topic is not None:
            config.set_discussion_topic(discussion_topic)
        elif config.discussion_topic is not None:
            discussion_topic = config.discussion_topic

        file = request.form.get(ElementNames.FILE_CONTENTS.value)
        if file is not None:
            config.set_filecontent(file)
        elif config.filecontent is not None:
            file = config.filecontent

        filename = request.form.get(ElementNames.FILE_NAME.value)
        if filename is not None:
            config.set_filename(filename)
        elif config.filename is not None:
            filename = config.filename

        global arena
        arena = Arena(
            discussion_topic, {"file_name": filename, "file_contents": file}, config
        )
    return render_template(Templates.CHAT.value)
    #     arena = Arena(discussion_topic, selected_models)
    #     return render_template(
    #         "chat.html", selected_models=selected_models, topic=discussion_topic
    #     )
    # system_models = UtilLLM.available_models()
    # return render_template("config.html", models=system_models)


@app.route("/toggle_pause", methods=["POST"])
def toggle_pause():
    paused: bool = not config.is_paused
    config.set_paused(paused)
    return jsonify(paused=paused)


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
        view = request.form.get(ElementNames.VIEW_TOGGLE.value)
        config.set_system_prompt(sysprompt)
        config.set_max_turns(int(max_n_o_turns))
        config.set_agents(selected_agents)
        config.set_agent_behavior(agent_behavior)
        config.set_view(view)

    return render_template(
        Templates.SETTINGS.value,
        models=Arena.available_system_models(),
        behaviors=Agent.agent_behaviors(config.agent_behavior),
        sysprompt=config.system_prompt,
        max_turns=config.max_n_o_turns,
        view=config.view,
        default_models=config.selected_agents,
    )


@app.route("/prior")
def prior_conversations():
    return "Under active development!"


if __name__ == "__main__":
    app.run(debug=False)
