"""Retriever GUI
=======================
This cookbook demonstrates a simple GUI for the retriever using Stremlit.
"""

import os
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(1, str(Path(os.getcwd()).parents[1]))

from grag.components.multivec_retriever import Retriever


class PageHome:
    """Manages the home page interface and interactions in a web application.

    Attributes:
        app: The application instance holding components like the retriever.
    """

    def __init__(self, app):
        """Initializes the PageHome with the application instance.

        Args:
            app: The application instance.
        """
        self.app = app

    def render_sidebar(self):
        """Renders the sidebar options for the application."""
        with st.sidebar:
            st.session_state.metadata_toggle = st.toggle("Show Metadata")
            st.session_state.top_k = st.number_input(
                "Show Top K", min_value=0, value=3, step=1
            )

    def render_search_form(self):
        """Renders the search form and returns the state of the search button."""
        st.markdown("Enter query")
        with st.form("search_form"):
            st.session_state.query = st.text_input(
                "Query:", value="What is Artificial Intelligence?"
            )
            return st.form_submit_button("Search")

    def get_search_results(self, _query, _top_k):
        """Retrieves search results based on the query and top_k parameter.

        Args:
            _query: The search query.
            _top_k: The number of top results to retrieve.

        Returns:
            A list of search results with scores.
        """
        return self.app.retriever.get_chunk(_query, top_k=_top_k, with_score=True)

    def render_search_results(self):
        """Displays the search results."""
        with st.spinner("Searching for similar chunks with :" + st.session_state.query):
            results = self.get_search_results(
                st.session_state.query, st.session_state.top_k
            )
            has_results = len(results) != 0
        if not has_results:
            return st.markdown("Could not find anything similar.")
        # st.write(results)
        for i, (result, score) in enumerate(results):
            with st.expander(f":bulb:**{i}** - Similiarity Score: {score:.3f}"):
                st.write(result.page_content)
                if st.session_state.metadata_toggle:
                    st.write(result.metadata)

    def check_connection(self):
        """Checks the connection to the search backend.

        Returns:
            True if the connection is active, False otherwise.
        """
        response = self.app.retriever.vectordb.test_connection()
        if response:
            return True
        else:
            return False

    def render_stats(self):
        """Renders statistics and details about the search backend."""
        st.write(f"""
        **Chroma Client Details:** \n
            Host Address    : {self.app.retriever.vectordb.host}:{self.app.retriever.vectordb.port} \n
            Collection Name : {self.app.retriever.vectordb.collection_name} \n
            Embeddings Type : {self.app.retriever.vectordb.embedding_type} \n
            Embeddings Model: {self.app.retriever.vectordb.embedding_model} \n
            Number of docs  : {self.app.retriever.vectordb.collection.count()} \n
        """)
        if st.button("Check Connection"):
            response = self.app.retriever.vectordb.test_connection()
            if response:
                st.write(":green[Connection Active]")
            else:
                st.write(":red[Connection Lost]")

    def render(self):
        """Main rendering function for the home page, orchestrating the UI components."""
        self.render_sidebar()
        tab1, tab2 = st.tabs(["Search", "Details"])
        with tab1:
            submitted = self.render_search_form()
            if submitted:
                self.render_search_results()
        with tab2:
            self.render_stats()


class App:
    """Represents the main application for the Retriever system.

    This class initializes the application and sets up the main interface.
    """

    def __init__(self):
        """Initializes the application with a Retriever instance."""
        self.retriever = Retriever()

    def render(self):
        """Renders the application title and the home page interface."""
        st.title("Retriever App")
        PageHome(self).render()


if __name__ == "__main__":
    App().render()

# based on https://blog.streamlit.io/finding-your-look-alikes-with-semantic-search/
