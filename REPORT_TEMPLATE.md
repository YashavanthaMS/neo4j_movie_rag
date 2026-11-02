# Project Report: Movie Knowledge Graph RAG

## 1. Introduction
Goal, motivation, why graph + RAG instead of plain LLM (grounding, no hallucination).

## 2. Knowledge Graph Schema
Nodes: Person {name, born}, Movie {title, released, tagline}  (~133 nodes)
Relationships: ACTED_IN {roles}, DIRECTED, PRODUCED, WROTE, REVIEWED {rating, summary}, FOLLOWS
(Insert screenshot of `CALL db.schema.visualization()`)

## 3. RAG Architecture
User question -> LLM router (picks template + extracts entities) -> parameterised Cypher
-> Neo4j rows -> LLM answer constrained to retrieved data -> UI (shows Cypher + rows for transparency).
(Insert architecture diagram)
Why templates: safe (read-only, no injection), predictable, easy to evaluate.

## 4. Cypher Templates
Table: name | purpose | parameters (see queries.py)

## 5. Implementation
Tech stack: Neo4j, Python driver, Anthropic API, Streamlit. File overview.

## 6. Example Interactions
Paste 6-8 screenshots/transcripts: cast, filmography, director, co-actors,
recommendation, top rated, connection path, an out-of-scope question.

## 7. Evaluation
Table of test questions, expected answer (verified in Neo4j Browser), actual answer, pass/fail.

## 8. Limitations
- Only questions covered by templates; small dataset (no genres/plots).
- Name matching uses CONTAINS (ambiguity, e.g. "Matrix" -> 3 films).
- Router errors on typos/complex multi-hop questions.
- Recommendations based on shared people only, no user preferences.

## 9. Possible Extensions
Text-to-Cypher fallback with read-only validation; vector embeddings of taglines;
genre/plot data (e.g. TMDB); conversation memory; user preference graph; larger dataset.

## 10. Conclusion
