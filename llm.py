"""LLM calls (Gemini): (1) route a question to a Cypher template, (2) write a grounded answer."""
import json
import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types
from queries import TEMPLATES

load_dotenv()
MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")
_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def _ask(system: str, user: str, max_tokens: int = 2048) -> str:
    resp = _client.models.generate_content(
        model=MODEL,
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=max_tokens,
            temperature=0.2,
        ),
    )
    return (resp.text or "").strip()


def _template_catalog() -> str:
    return "\n".join(
        f'- {name}: {t["description"]} params={json.dumps(t["params"])}'
        for name, t in TEMPLATES.items()
    )


ROUTER_SYSTEM = f"""You convert movie questions into a graph query plan.
Graph: (Person)-[:ACTED_IN|DIRECTED|PRODUCED|WROTE|REVIEWED]->(Movie).
Available templates:
{_template_catalog()}

Reply with ONLY JSON: {{"template": "<name>", "params": {{...}}}}
Use the exact movie title / person name as written in the question (fix obvious typos).
If no template fits, reply {{"template": "none", "params": {{}}}}."""


def route_question(question: str) -> dict:
    raw = _ask(ROUTER_SYSTEM, question)
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    try:
        plan = json.loads(match.group(0)) if match else {}
    except json.JSONDecodeError:
        plan = {}
    return {"template": plan.get("template", "none"), "params": plan.get("params", {})}


ANSWER_SYSTEM = """You are a movie assistant answering from a knowledge graph.
Rules:
- Use ONLY the facts in the provided graph data. Do not add outside knowledge.
- If the data is empty or does not answer the question, say you couldn't find it in the database.
- For recommendations, explain WHY (e.g. shared actors or director) using the data.
- Be concise and friendly."""


def generate_answer(question: str, template: str, rows: list[dict]) -> str:
    context = json.dumps(rows, ensure_ascii=False, default=str)[:8000]
    user = f"Question: {question}\n\nQuery used: {template}\nGraph data (JSON):\n{context}"
    return _ask(ANSWER_SYSTEM, user)
