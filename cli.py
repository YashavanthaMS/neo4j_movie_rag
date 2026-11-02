from rag import ask

print("Movie Graph RAG  (type 'exit' to quit)")
while True:
    q = input("\nYou: ").strip()
    if q.lower() in {"exit", "quit", ""}:
        break
    r = ask(q)
    print(f"\n[template={r['template']} params={r['params']} rows={len(r['rows'])}]")
    print(f"Bot: {r['answer']}")
