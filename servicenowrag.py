import os
import json
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core.memory import ChatMemoryBuffer
from flask import Flask, request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")
index_storage_dir = "index_servicenow_storage"
data_dir = "servicenow_data"

Settings.embed_model = GeminiEmbedding(
    model_name="models/embedding-001", api_key=api_key
)

Settings.llm = Gemini(api_key=api_key, temperature=0)


if not os.path.exists(index_storage_dir):
    print("Creating new index...")
    # load the documents and create the index
    reader = SimpleDirectoryReader(input_dir=data_dir, encoding='latin-1')
    documents = reader.load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=index_storage_dir)
else:
    # load the existing index
    print("Loading existing index...")
    storage_context = StorageContext.from_defaults(persist_dir=index_storage_dir)
    index = load_index_from_storage(storage_context)
    
print("Index loaded successfully.")

memory = ChatMemoryBuffer.from_defaults(token_limit=4000)

chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt=(
        """You are a friendly chatbot, able to have normal interactions.
        You help the users with their questions. Return answers from the stored documents only.
        Take inference from the incidents, always return the incident number,
        summarize the entire incident and return the shortest response.
        Do not make up your own answers. """
    ),
)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def home():
    return "Service Now API"

@app.route('/service', methods=['GET','POST'])
@cross_origin()
def get_bot_response():
    prompt = request.args.get('prompt')
    print("Received prompt:", prompt)
    response = chat_engine.chat(prompt)
    output_dict = {"response": response.response}
    output_json = json.dumps(output_dict)
    print(f"Response: {response.response}")
    return output_json

if __name__ == "__main__":
    app.run(debug=True, port=9090)