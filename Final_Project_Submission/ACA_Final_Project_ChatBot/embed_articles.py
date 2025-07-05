from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import faiss

def embed_documents(docs, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    texts = [doc['content'] for doc in docs]
    embeddings = model.encode(texts, show_progress_bar=True)
    return np.array(embeddings)

def save_embeddings(embeddings, docs, path='embeddings.pkl'):
    with open(path, 'wb') as f:
        pickle.dump({'embeddings': embeddings, 'docs': docs}, f)

def load_embeddings(path='embeddings.pkl'):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data['embeddings'], data['docs']

def save_faiss_index(embeddings, index_path='faiss_index.index'):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype('float32'))
    faiss.write_index(index, index_path)

def load_faiss_index(index_path='faiss_index.index'):
    return faiss.read_index(index_path)