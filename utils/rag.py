import uuid

from haystack import Document, Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack_integrations.components.generators.ollama import OllamaGenerator

from constants import ModelNames


class Rag(object):
    def __init__(self):
        pass

    @staticmethod
    def generate_response(query, using_model: str, context: list[str]) -> list[str]:
        docs = [Document(content=content, id=str(uuid.uuid4())) for content in context]
        document_store = InMemoryDocumentStore()
        document_store.write_documents(docs)

        template = """
        Given only the following information, answer the question.
        Ignore your own knowledge.

        Context:
        {% for document in documents %}
            {{ document.content }}
        {% endfor %}

        Question: {{ query }}?
        """

        pipeline = Pipeline()

        pipeline.add_component(
            "retriever", InMemoryBM25Retriever(document_store=document_store)
        )
        pipeline.add_component("prompt_builder", PromptBuilder(template=template))
        pipeline.add_component(
            "llm",
            OllamaGenerator(
                model=ModelNames.GEMMA_INSTRUCT.value,
                url="http://localhost:11434/api/generate",
            ),
        )
        pipeline.connect("retriever", "prompt_builder.documents")
        pipeline.connect("prompt_builder", "llm")

        response = pipeline.run(
            {"prompt_builder": {"query": query}, "retriever": {"query": query}}
        )

        return response["llm"]["replies"]
