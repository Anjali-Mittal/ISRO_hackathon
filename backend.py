import requests
from py2neo import Graph

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "astraloom123"))

# System prompt that teaches Ollama about your graph schema
SYSTEM_PROMPT = """
You are an expert Cypher generator for a Neo4j graph of ISRO missions.

The graph has:
(:Mission)-[:ORBIT_TYPE]->(:Orbit)
(:Mission)-[:LAUNCHED_BY]->(:Vehicle)
(:Mission)-[:HAS_APPLICATION]->(:Application)
(:Mission)-[:LAUNCHED_ON]->(:Date)

Given a user question, output only the corresponding Cypher query.
"""

def get_cypher_query_from_llm(question):
    prompt = SYSTEM_PROMPT + f"\nUser: {question}\nCypher:"
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()

def run_cypher_on_neo4j(cypher_query):
    try:
        return graph.run(cypher_query).data()
    except Exception as e:
        return [{"error": str(e)}]

def explain_result(question, results):
    prompt = f"Question: {question}\nResults: {results}\nAnswer in a friendly sentence, without using the word 'friend'.Maintain a professional tone while answering the question and keep it crisp."
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()

def ask_kg(question):
    cypher = get_cypher_query_from_llm(question)
    results = run_cypher_on_neo4j(cypher)
    explanation = explain_result(question, results)
    return cypher, explanation