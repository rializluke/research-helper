from fastapi import FastAPI, HTTPException
from pydantic import BaseModel # Data Validation
import requests # Used to make requests
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os

# Instancing Fastapi
app = FastAPI()

# Represents the input from the user, containing the search text and an optional limit on the number of results
class Query(BaseModel):
    text: str
    limit: Optional[int] = 10

# Represents a single research paper's metadata, including title, abstract, URL, year of publication, authors, and citation count
class Paper(BaseModel):
    title: str
    abstract: str
    url: str
    year: Optional[int]
    authors: List[str]
    citationCount: Optional[int]

# Represents the response structure containing a list of Paper objects
class PapersResponse(BaseModel):
    papers: List[Paper]

# Fetching papers from Semantic Scholar
def fetch_papers_from_semantic_scholar(query: str, limit: int = 10):
    """Fetch papers from Semantic Scholar API"""
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers = {
        "Accept": "application/json"
    }
    
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,abstract,url,year,authors,citationCount"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Semantic Scholar API error: {response.text}"
        )
    
    return response.json()

# Processes the raw data returned from the Semantic Scholar API, filtering out any papers that do not have a title or abstract and converting them into Paper objects
def process_papers(papers_data: dict) -> List[Paper]:
    """Process and filter papers data"""
    processed_papers = []
    
    for paper in papers_data.get('data', []):
        if not paper.get('title') or not paper.get('abstract'):
            continue
            
        processed_papers.append(Paper(
            title=paper.get('title', ''),
            abstract=paper.get('abstract', ''),
            url=paper.get('url', ''),
            year=paper.get('year'),
            authors=[author.get('name', '') for author in paper.get('authors', [])],
            citationCount=paper.get('citationCount')
        ))
    
    return processed_papers

# API route to fetch papers

@app.post("/fetch_papers/", response_model=PapersResponse)
async def fetch_papers(query: Query):
    """Endpoint to fetch and process research papers"""
    try:
        # Fetch papers from Semantic Scholar
        papers_data = fetch_papers_from_semantic_scholar(query.text, query.limit)
        
        # Process and filter papers
        processed_papers = process_papers(papers_data)
        
        return {"papers": processed_papers}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# This endpoint listens for POST requests at /fetch_papers/, accepts a Query object as input, fetches relevant papers using the previously defined functions, processes them into a structured format, and returns them as a PapersResponse