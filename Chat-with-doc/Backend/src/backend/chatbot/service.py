from openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.db import collection
import os
from dotenv import load_dotenv
from backend.chatbot.schema import ChatPayload

load_dotenv() 

openai_client = OpenAI(
    api_key= os.getenv("OPEN_AI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)
textEmbeddingModel = "text-embedding-3-large"

def store_data_from_doc():
    try:
        path = r"F:\WorkSpace\Chat-with-doc\Backend\docs\Gokul Sureshkumar – Resume.pdf"
        loader = PyPDFLoader(path)

        data = loader.load
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap=40)
        documents = text_splitter.split_documents(data)

        docs_to_insert = [
            {
                "title": doc.page_content[:50],  # Short title/preview
                "text": doc.page_content,      # Original document text
                "embeddings": get_embeddings(doc.page_content)
            } for doc in documents
        ]

        collection.insert_many(docs_to_insert)

        return "Data inserted into DB collection"
    except:
        return "exception"
    finally:
        return "Error"


def get_embeddings(text, input_type = "documet"):
    try:
        respone = openai_client.embeddings.create(
            input=text,
            model=textEmbeddingModel
        )

        return respone.data[0].embedding
    except:
        return "Model error"

def chat_with_data(payload: ChatPayload):
    #return get_user_query_result(payload.message)
    quried_result = get_user_query_result(payload.message)
    context = get_context_from_results(quried_result)
    modal_response = get_modal_response(payload.message, context)

    return modal_response
   
def get_user_query_result(input_query):
    user_input = input_query
    user_input_embedding = get_embeddings(user_input, input_type="user_input")

    pipeline = [
        {
            "$vectorSearch" : {
                "index":"vector_index",
                "path" :"embeddings",
                "queryVector":user_input_embedding,
                "numCandidates" : 100,
                "limit" :5
            }
        },
        {
            "$project" : {
                "_id" : 0,
                "content": 1
            }
        }
    ]    
    
    results = list(collection.aggregate(pipeline))
    
    return results

def get_context_from_results(results):
    context = ""
    context = "\n\n".join(
        doc["content"]
        for doc in results
        if doc.get("content")
    )
    
    return context

def get_modal_response(question, context):
    messages = [
        {
            "role": "system",
            "content": (
                "Answer the question using only the provided context. "
                "If the answer isn't available in the context, "
                "say you couldn't find that information."
            ),
        },
        {
            "role": "user",
            "content": f"Context: {context}\nQuestion: {question}",
        },
    ]
    response = openai_client.chat.completions.create(
        model="gemma-4-26b-a4b-it",
        messages=messages
    )

    return response.choices[0].message.content