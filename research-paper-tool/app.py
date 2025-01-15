import streamlit as st
import requests
from typing import Dict, Any

# Takes a single paper's data as input and formats it for display.
def display_paper(paper: Dict[Any, Any]):
    """Display a single paper with formatting"""
    st.markdown(f"### [{paper['title']}]({paper['url']})")
    
    # Display authors
    if paper['authors']:
        authors = ", ".join(paper['authors'])
        st.markdown(f"**Authors:** {authors}")
    
    # Display year and citations
    meta_info = []
    if paper['year']:
        meta_info.append(f"Year: {paper['year']}")
    if paper['citationCount'] is not None:
        meta_info.append(f"Citations: {paper['citationCount']}")
    
    if meta_info:
        st.markdown(" | ".join(meta_info))
    
    # Display abstract
    if paper['abstract']:
        with st.expander("Show Abstract"):
            st.write(paper['abstract'])
    
    st.markdown("---")

def main():
    st.title("Research Paper Query Tool")
    st.write("Search for academic papers related to your research topic.")
    
    # Input fields
    user_query = st.text_input("Enter your research query:")
    num_papers = st.slider("Number of papers to retrieve", 5, 50, 10)
    
    if st.button("Search Papers"):
        if user_query:
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/fetch_papers/",
                    json={"text": user_query, "limit": num_papers}
                )
    # When the user clicks the "Search Papers" button, it sends a POST request to the FastAPI endpoint (/fetch_papers/) with the user's query and desired limit
                
                if response.status_code == 200:
                    papers = response.json()["papers"]
                    
                    if not papers:
                        st.warning("No papers found for your query.")
                    else:
                        st.write(f"Found {len(papers)} papers:")
                        for paper in papers:
                            display_paper(paper)
                else:
                    st.error(f"Error: {response.text}")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()