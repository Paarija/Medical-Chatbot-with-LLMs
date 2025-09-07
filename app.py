from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os


# ----------------------
# Flask App Setup
# ----------------------
app = Flask(__name__)

# Load environment variables from .env
load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Ensure env vars are available for downstream libs
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY


# ----------------------
# Pinecone + Embeddings
# ----------------------
embeddings = download_hugging_face_embeddings()

index_name = "medical-chatbot"

# Connect to Pinecone vector DB
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})


# ----------------------
# Gemini Chat Model
# ----------------------
chatModel = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GEMINI_API_KEY  # ✅ use key from .env, skip ADC
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Retrieval-Augmented Generation (RAG) chain
question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


# ----------------------
# Flask Routes
# ----------------------
@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    print("User:", msg)

    response = rag_chain.invoke({"input": msg})
    answer = response["answer"]

    print("Response:", answer)
    return str(answer)


# ----------------------
# Run App
# ----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
