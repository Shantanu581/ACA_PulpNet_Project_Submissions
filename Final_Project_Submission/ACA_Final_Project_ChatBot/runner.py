from load_data import load_all_articles
from embed_articles import embed_documents, save_embeddings, save_faiss_index

docs = load_all_articles('C:/Users/chhon/Python Notebooks/ACA_PulpNet_Summer Project/ACA_Final_Project_ChatBot/Data')
embeddings = embed_documents(docs)
save_embeddings(embeddings, docs)
save_faiss_index(embeddings)