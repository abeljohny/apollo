import ollama


def available_models():
    system_models = ollama.list()
    return [model['name'] for model in system_models["models"]]


def chat(input_text):
    stream = ollama.chat(
        model="gemma",
        messages=[{"role": "user", "content": f"{input_text}"}],
        stream=True,
    )

    for chunk in stream:
        yield f'data:{chunk["message"]["content"]}\n\n'
