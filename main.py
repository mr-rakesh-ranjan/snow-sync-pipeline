
from vertexai.preview import rag
from vertexai.preview.generative_models import GenerativeModel, Tool
import vertexai

from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

# Project setup
project_id = os.getenv('PROJECT_ID')
display_name = os.getenv('DISPLAY_NAME')
# paths = os.getenv('PATHS')
# paths = ['https://drive.google.com/file/d/1IMEQ3PJgrxHq9J3zHOlatyG3SkkoCmM3','https://drive.google.com/file/d/18j4jWSWsKVGXF_d-3Dy-pyegqyR-jELn', 'https://drive.google.com/file/d/1L8hii4Fk979G8RpknGvguGCSS9AdpsHe']
paths = ['https://drive.google.com/file/d/1IMEQ3PJgrxHq9J3zHOlatyG3SkkoCmM3']
# print(f"{project_id} '\n' {display_name} '\n' {paths}")

vertexai.init(project=project_id, location='us-central1')

rag_corpus = rag.create_corpus(display_name=display_name)
# print(rag_corpus)

response = rag.import_files(
    rag_corpus.name,
    paths,
    chunk_size=512,
    chunk_overlap=100
)

response = rag.retrieval_query(
    rag_resources=[
        rag.RagResource(
            rag_corpus=rag_corpus.name
        )
    ],
    text="what is spam?",
    similarity_top_k=10,
    vector_distance_threshold=0.5
)

print(rag_corpus)


# Enhance generation
# Create a RAG retrieval tool
rag_retrieval_tool = Tool.from_retrieval(
    retrieval=rag.Retrieval(
        source=rag.VertexRagStore(
            rag_resources=[
                rag.RagResource(
                    rag_corpus=rag_corpus.name,
                )
            ],
            similarity_top_k=10,  # Optional
            vector_distance_threshold=0.1,  # Optional
        ),
    )
)

# print(rag_corpus)
# Create a gemini-pro model instance
rag_model = GenerativeModel(
    model_name="gemini-1.0-pro-002", tools=[rag_retrieval_tool]
)

# Generate response
# response = rag_model.generate_content("What is Spam?")
# response = rag_model.generate_content(" copyrigt application using in computer are legal or illegal?")
# response = rag_model.generate_content("how to get my policy details?")
# print(response.text)

# questions and answers in loop
while True:
    query=input("\nEnter a query: ")
    if query == "exit":
        break
    #Print the result
    print("\n\n> Question:")
    print (query)
    answer = rag_model.generate_content(query)
    print (answer.text)