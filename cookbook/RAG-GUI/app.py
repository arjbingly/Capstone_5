import os
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(1, str(Path(os.getcwd()).parents[1]))

st.set_page_config(page_title="RAG")

from grag.components.utils import get_config
from grag.rag.basic_rag import BasicRAG


@st.cache_data
def load_config():
    return get_config()


conf = load_config()


class RAGApp:
    def __init__(self, app, conf):
        self.app = app
        self.conf = conf
        self.selected_model = None
        self.exit_app = False

    def render_sidebar(self):
        with st.sidebar:
            st.title('RAG')
            st.subheader('Models and parameters')
            st.sidebar.selectbox('Choose a model',
                                 ['Llama-2-13b-chat', 'Llama-2-7b-chat',
                                  'Mixtral-8x7B-Instruct-v0.1', 'gemma-7b-it'],
                                 key='selected_model')
            st.sidebar.slider('Temperature',
                              min_value=0.1,
                              max_value=1.0,
                              value=0.1,
                              step=0.1,
                              key='temperature')
            st.sidebar.slider('Top-k',
                              min_value=1,
                              max_value=5,
                              value=3,
                              step=1,
                              key='top_k')
            st.button('Load Model', on_click=self.load_rag)
            st.checkbox('Show retrieved content', key='show_content')

    def load_rag(self):
        if 'rag' in st.session_state:
            del st.session_state['rag']

        llm_kwargs = {"temperature": st.session_state['temperature']}
        if st.session_state['selected_model'] == "Mixtral-8x7B-Instruct-v0.1":
            llm_kwargs['n_gpu_layers'] = 16
            llm_kwargs['quantization'] = 'Q4_K_M'
        elif st.session_state['selected_model'] == "gemma-7b-it":
            llm_kwargs['n_gpu_layers'] = 18
            llm_kwargs['quantization'] = 'f16'

        retriever_kwargs = {
            "client_kwargs": {"read_only": True, },
            "top_k": st.session_state['top_k']
        }
        st.session_state['rag'] = BasicRAG(model_name=st.session_state['selected_model'],
                                           llm_kwargs=llm_kwargs,
                                           retriever_kwargs=retriever_kwargs)
        st.session_state['loaded_temp'] = st.session_state['temperature']
        st.session_state['loaded_k'] = st.session_state['top_k']
        st.session_state['loaded_model'] = st.session_state['selected_model']

    def clear_cache(self):
        st.cache_data.clear()

    def render_main(self):
        st.title("Welcome to the RAG App")

        if 'rag' not in st.session_state:
            st.write("You have not loaded the model")
        else:
            st.write(f"Model: {st.session_state['loaded_model']}")
            st.write(f"Temperature: {st.session_state['loaded_temp']}")
            st.write(f"Top-k: {st.session_state['loaded_k']}")

            user_input = st.text_area("Enter your query:", height=20)
            submit_button = st.button("Submit")

            if submit_button and user_input:
                response, retrieved_docs = st.session_state['rag'](user_input)
                st.text_area(value=response, label='Response')
                with st.expander("Sources"):
                    for index, doc in enumerate(retrieved_docs):
                        st.markdown(f"**{index}. {doc.metadata['source']}**")
                        if st.session_state['show_content']:
                            st.markdown(f"**{doc.page_content}**")

    def render(self):
        self.render_sidebar()
        self.render_main()


if __name__ == "__main__":
    app = RAGApp(st, conf)
    app.render()
