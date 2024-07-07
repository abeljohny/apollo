import ollama


def available_models():
    return ["model1", "model2"]


def chat(input_text):
    stream = ollama.chat(
        model="gemma",
        messages=[{"role": "user", "content": f"{input_text}"}],
        stream=True,
    )

    for chunk in stream:
        yield f'data:{chunk["message"]["content"]}\n\n'
