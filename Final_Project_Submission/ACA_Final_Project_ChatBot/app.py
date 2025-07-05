import streamlit as st
from load_data import load_all_articles
from embed_articles import load_embeddings
from qa_bot import answer_question

st.set_page_config(page_title="Vox IITK Chatbot", page_icon="🤖")
st.title("📚 Vox IITK QA Bot")
st.markdown("Ask me anything about Vox Populi IIT Kanpur content!")

question = st.text_input("Ask a question:")

if 'embeddings' not in st.session_state:
    with st.spinner("Loading data and embeddings..."):
        embeddings, docs = load_embeddings('embeddings.pkl')
        st.session_state['embeddings'] = embeddings
        st.session_state['docs'] = docs

if question:
    with st.spinner("Finding the answer..."):
        result = answer_question(question, st.session_state['embeddings'], st.session_state['docs'])
        st.subheader("Answer:")
        st.markdown(f"**{result['answer']}**")
        with st.expander("Show source context"):
            st.markdown(result['context'])
