from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import numpy as np
from embed_articles import load_embeddings, load_faiss_index
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import torch
import faiss

qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Flan-T5 Model
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

# Sentence embedder for retrieving context 
embedder = SentenceTransformer("all-MiniLM-L6-v2")
embeddings, docs = load_embeddings('embeddings.pkl')
faiss_index = load_faiss_index('faiss_index.index')

def get_top_context(question, embeddings, docs, k=1):
    q_embed = embedder.encode([question]).astype('float32')
    _, top_idxs = faiss_index.search(q_embed.reshape(1, -1), k)
    return [docs[i] for i in top_idxs[0]]

# Flan-T5 to wrap BERT answer
def wrap_answer_with_flan(question, raw_answer, context):
    prompt = f"""Question: {question}
Answer: {raw_answer}
Context: {context[:1000]}

Now write a helpful, clear reply based on the above.
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        do_sample=False
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    return response

def answer_question(question, embeddings, docs):
    top_contexts = get_top_context(question, embeddings, docs, k=2)
    context = "\n\n".join([ctx['content'] for ctx in top_contexts])

    raw = qa_model(question=question, context=context)

    final_answer = wrap_answer_with_flan(question, raw['answer'], context)

    return {
        "answer": final_answer,
        "score": raw['score'],
        "context": context[:1000] + "..."
    }
