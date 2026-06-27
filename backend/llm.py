from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from config import MODEL_NAME, GOOGLE_API_KEY
from prompt import SYSTEM_PROMPT

import traceback

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")


llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=SYSTEM_PROMPT
)


def build_context(documents):

    if not documents:
        return "No relevant documents found."

    context_parts = []

    for doc in documents:

        filename = doc.metadata.get("document", "Unknown")
        page = doc.metadata.get("page", "Unknown")

        context_parts.append(
            f"""
Document:
{filename}

Page:
{page}

Content:
{doc.page_content}
"""
        )

    return "\n\n".join(context_parts)


def generate_answer(question, documents):

    try:
        context = build_context(documents)

        print("=" * 50)
        print("Context Length:", len(context))
        print("Question:", question)
        print("=" * 50)

        chain = prompt | llm

        response = chain.invoke({
            "context": context,
            "question": question
        })

        print("Gemini Response Received")

        return response.content

    except Exception as e:
        print("LLM ERROR:")
        print(traceback.format_exc())

        return "Error: Unable to generate answer from LLM."