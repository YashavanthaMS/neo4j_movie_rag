"""RAG pipeline: question -> template + params -> Cypher -> rows -> grounded answer."""
from graph_db import run_query
from llm import route_question, generate_answer
from queries import TEMPLATES

FALLBACK = ("Sorry, I can't map that question to something in the movie graph. "
            "Try asking about actors, directors, cast, years, reviews or recommendations.")


def ask(question: str) -> dict:
    plan = route_question(question)
    name, params = plan["template"], plan["params"]

    if name not in TEMPLATES:
        return {"answer": FALLBACK, "template": None, "params": {}, "cypher": None, "rows": []}

    tpl = TEMPLATES[name]
    clean = {}
    for key, typ in tpl["params"].items():
        if key not in params:
            return {"answer": f"I need more info ({key}) to answer that.",
                    "template": name, "params": params, "cypher": tpl["cypher"], "rows": []}
        clean[key] = int(params[key]) if typ == "int" else str(params[key]).strip()

    rows = run_query(tpl["cypher"], clean)
    answer = generate_answer(question, name, rows)
    return {"answer": answer, "template": name, "params": clean,
            "cypher": tpl["cypher"], "rows": rows}
