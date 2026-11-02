# Movie Graph RAG

Neo4j Movies knowledge graph + LLM (Cypher templates -> retrieval -> grounded answer).

## Setup
1. Create a Neo4j instance (AuraDB Free or Neo4j Desktop) and load the Movies dataset.
   - Desktop / Browser: run `:play movies`, go to slide 2, click the code block, press Run.
   - AuraDB: choose the "Movies" example dataset when creating, or run the same script in Query.
2. `python -m venv venv && source venv/bin/activate` (Windows: `venv\Scripts\activate`)
3. `pip install -r requirements.txt`
4. `cp .env.example .env` and fill in credentials.
5. `python check_db.py`   # verify data + all templates
6. `python cli.py`  or  `streamlit run app.py`
