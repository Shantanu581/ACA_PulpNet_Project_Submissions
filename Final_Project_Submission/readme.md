# 📚 Vox Populi IITK Chatbot

A local, transformer-powered chatbot that answers questions based on editorial articles from Vox Populi, IIT Kanpur. It uses semantic search with FAISS, BERT for extraction, and Flan-T5 for natural language generation. The interface is built using Streamlit.

---

## Features

- Context-aware answers from Vox editorial content
- Fast semantic search using FAISS
- Accurate extractive QA with BERT
- Natural response generation using Flan-T5
- Clean Streamlit frontend

---

## 📦Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/vox-iitk-chatbot.git
cd vox-iitk-chatbot
```
### 2. Run the ` runner.py ` script to load the ` embeddings.pkl ` and ` faiss.index ` file.
Note : Make sure in the current folder while loading this

### 3. Type the following in the command prompt :
```bash
streamlit run app.py
```
Note : Again make sure you are in the same folder as of embeddings.pkl and faiss.index to run the bot

### 4. Done. The Bot opens in a new browser tab
