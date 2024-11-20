import json

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
                vectors.append(data[entry]["vector"][0])  # Use the first item if it's a list      
            else:
                # Skip the entry if embeddings format is not met
                continue

    return chunks, vectors


# Load and save data to ChromaDB if not already done
file_path = r'C:\Users\kumar\Desktop\Sem_5\DL\mental_health_rag\chunk_vectors.json'

chunks, vectors = load_chunks_and_vectors_from_json(file_path)

print(len(chunks), len(vectors))