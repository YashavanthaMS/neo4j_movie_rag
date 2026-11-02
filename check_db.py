"""Sanity check: verifies the Movies graph is loaded and every template runs."""
from graph_db import run_query
from queries import TEMPLATES

print("Node counts:", run_query("MATCH (n) RETURN labels(n)[0] AS label, count(*) AS n"))
print("Rel counts :", run_query("MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS n"))

samples = {"name": "Tom Hanks", "title": "Matrix", "start": 1995, "end": 2000,
           "name1": "Kevin Bacon", "name2": "Keanu Reeves"}
for name, t in TEMPLATES.items():
    params = {k: samples[k] for k in t["params"]}
    rows = run_query(t["cypher"], params)
    print(f"{'OK ' if rows else 'EMPTY'} {name:28s} -> {len(rows)} rows")
