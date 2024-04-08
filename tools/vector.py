import streamlit as st
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from llm import llm, embeddings
from langchain.chains import RetrievalQA

neo4jvector = Neo4jVector.from_existing_index(
    embeddings,                              
    url=st.secrets["NEO4J_URI"],             
    username=st.secrets["NEO4J_USERNAME"],   
    password=st.secrets["NEO4J_PASSWORD"],   
    index_name="moviePlots",                 
    node_label="Movie",                      
    text_node_property="plot",               
    embedding_node_property="plotEmbedding", 
    retrieval_query="""
RETURN
    node.plot AS text,
    score,
    {
        title: node.title,
        directors: [ (person)-[:DIRECTED]->(node) | person.name ],
        actors: [ (person)-[r:ACTED_IN]->(node) | [person.name, r.role] ],
        tmdbId: node.tmdbId,
        source: 'https://www.themoviedb.org/movie/'+ node.tmdbId
    } AS metadata
"""
)

retriever = neo4jvector.as_retriever()
kg_qa = RetrievalQA.from_chain_type(
    llm,
    chain_type = "stuff",
    retriever = retriever,
)