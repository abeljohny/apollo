from typing import Optional

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
from utils.persistence import Persistence

app = Flask(__name__)
config = Config()
persistence = Persistence()
arena: Optional[Arena] = None


@app.route("/")
def index():
    return render_template(Templates.INDEX.value)


@app.route("/new", methods=["GET", "POST"])
def new_conversation():
    global arena
    if request.method == "POST":
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
            discussion_topic,
            {"file_name": filename, "file_contents": file},
            config,
            persistence,
        )
    return render_template(Templates.CHAT.value)


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


@app.route("/prior")
def prior():
    record_keys = persistence.database.instance.keys()
    records = []
    for key in record_keys:
        records.append(persistence.database.instance.hgetall(key))
    return render_template(
        Templates.PRIOR.value,
        records=sorted(records, key=lambda record: record["timestamp"], reverse=True),
    )


@app.route("/prior_instance")
def prior_instance():
    conversation = request.args.get("conversation")
    return render_template(Templates.PRIOR_INSTANCE.value, conversation=conversation)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        sysprompt = request.form.get(ElementNames.SYSPROMPT.value)
        max_n_o_turns = request.form.get(ElementNames.MAX_N_O_TURNS.value)
        selected_agents = request.form.getlist(ElementNames.SELECTED_AGENTS.value)
        agent_behavior = request.form.get(ElementNames.AGENT_BEHAVIOR.value)
        view = request.form.get(ElementNames.VIEW_TOGGLE.value)
        bias = request.form.get(ElementNames.BIAS_TOGGLE.value)
        lawyer = request.form.get(ElementNames.LAWYER_TOGGLE.value)
        config.set_system_prompt(sysprompt)
        config.set_max_turns(int(max_n_o_turns))
        config.set_agents(selected_agents)
        config.set_agent_behavior(agent_behavior)
        config.set_view(view)
        config.set_bias(bias)
        config.set_lawyer_mode(lawyer)

    return render_template(
        Templates.SETTINGS.value,
        models=Arena.available_system_models(),
        behaviors=Agent.agent_behaviors(config.agent_behavior),
        sysprompt=config.system_prompt,
        max_turns=config.max_n_o_turns,
        view=config.view,
        bias=config.bias,
        lawyer=config.lawyer,
        default_models=config.selected_agents,
    )


if __name__ == "__main__":
    app.run(debug=False)
