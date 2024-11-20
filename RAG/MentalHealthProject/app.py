# app.py
import streamlit as st
import requests
import json
import chromadb
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from config import GROQ_API_KEY

# Initialize ChromaDB client and collection
client = chromadb.Client()
collection_name = "mental_health"
collection = client.get_or_create_collection(collection_name)

# Embedding model setup
# Use a model with a dimension of 384


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Function to load chunks and vectors from a JSON file
def load_chunks_and_vectors_from_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    chunks = []
    vectors = []

    for entry in data:
        # Validate the structure of each entry
        if "text" in data[entry] and isinstance(data[entry]["text"], list) and len(data[entry]["text"]) > 0:
            chunks.append(data[entry]["text"][0])  # Use the first item from the list
        elif "text" in data[entry] and isinstance(data[entry]["text"], str):
            chunks.append(data[entry]["text"])  # Use the string directly
        else:
            # Skip the entry if the expected format is not met
            continue

        # Validate the structure of the embeddings
        if "vector" in data[entry]:
            if isinstance(data[entry]["vector"], list) and len(data[entry]["vector"]) > 0:
                vectors.append(data[entry]["vector"])  # Use the first item if it's a list      
            else:
                # Skip the entry if embeddings format is not met
                continue

    return chunks, vectors


# Function to save chunks and vectors to ChromaDB
def save_chunks_and_vectors_to_chromadb(chunks, chunk_vectors):
    for idx, (text, embeddings) in enumerate(zip(chunks, chunk_vectors)):
        collection.add(
            documents=[text],
            embeddings=[embeddings],
            ids=[str(idx)]
        )

# Load and save data to ChromaDB if not already done
file_path = "https://gateway.pinata.cloud/ipfs/QmeVzndKy56hyJX8R6Fm5ZSYibUEHavn2qCFb9iHBPL2mA"
try:
    # If collection is empty, load data from JSON and save to ChromaDB
    if collection.count() == 0:
        chunks, vectors = load_chunks_and_vectors_from_json(file_path)
        save_chunks_and_vectors_to_chromadb(chunks, vectors)
        # st.write("Data successfully loaded into ChromaDB.")
except Exception as e:
    st.error(f"Error loading data into ChromaDB: {e}")
# Function to perform RAG with relevance filtering
def perform_rag(query):
    # Embed the query
    query_vector = embedding_model.embed_query(query)
    # Retrieve documents from ChromaDB
    docs_chroma = collection.query(query_embeddings=[query_vector], n_results=5)
    
    # Check if "documents" exists and is not empty
    if "documents" not in docs_chroma or not docs_chroma["documents"]:
        st.write("No documents found for the given query.")
        return "No relevant documents were retrieved."

    # Ensure documents are not empty before accessing the first element
    retrieved_docs = [doc[0] for doc in docs_chroma["documents"] if len(doc) > 0]
    relevance_scores = [score[0] for score in docs_chroma["distances"] if len(score) > 0]
    # Display the retrieved documents and their relevance scores for debugging
    st.write("Retrieved Documents and Scores:")
    for doc, score in zip(retrieved_docs, relevance_scores):
        st.write(f"Document: {doc}, Relevance Score: {score}")
    # Filter documents based on a relevance threshold (lower score is better)
    relevance_threshold = 0.4
    filtered_docs = [
        doc for doc, score in zip(retrieved_docs, relevance_scores)
        if score >= relevance_threshold  # Assuming distances represent similarity, lower is better
    ]
    # st.write(filtered_docs)

    # If no relevant documents, respond accordingly
    if not filtered_docs:
        return "This system is designed to answer questions related to mental health only."

    # Combine filtered documents as context
    context_text = "\n\n".join(filtered_docs)
    # Set up prompt template
    PROMPT_TEMPLATE = """
    Answer the question based only on the following context:
    {context_text}
    Answer the question based on the above context: {question}.
    Provide a detailed answer.
    Don’t justify your answers.
    Don’t give information not mentioned in the CONTEXT INFORMATION.
    Do not say "according to the context" or "mentioned in the context" or similar.
    """
    # st.write(PROMPT_TEMPLATE)
    # prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    # prompt = prompt_template.format(context=context_text, question=query)
    # Format the prompt using str.format()
    prompt = PROMPT_TEMPLATE.format(context_text=context_text, question=query)

    # Print the whole prompt before sending it to the LLM
    # st.write("Prompt passed to the LLM:")
    # st.write(prompt)
    # Groq API call for generation
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.7,
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        response_data = response.json()
        response_text = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No output generated")
        return response_text
    else:
        return f"Failed to generate response. Error: {response.status_code}, {response.text}"


# Streamlit interface
st.title("Mental Health RAG Assistant")
st.write("Ask a question related to mental health:")

query = st.text_input("Enter your question:")
if st.button("Get Answer"):
    if query:
        with st.spinner("Generating answer..."):
            response = perform_rag(query)
            st.success("Generated Answer:")
            st.write(response)
    else:
        st.warning("Please enter a question.")
