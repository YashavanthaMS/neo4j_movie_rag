import streamlit as st
from rag import ask

st.set_page_config(page_title="Movie Graph RAG", page_icon="🎬", layout="centered")

# ---- Dark theme polish (base colours come from .streamlit/config.toml) ----
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&display=swap');
    :root { --amber:#E0A458; --ink:#12141A; --panel:#1B1F2A; --line:#2B3142; --muted:#9AA0AE; }

    .stApp { background: var(--ink); }
    header[data-testid="stHeader"] { background: transparent; }

    h1 { font-family:'Fraunces', Georgia, serif !important; font-weight:700 !important;
         letter-spacing:-0.01em; }
    h3 { font-family:'Fraunces', Georgia, serif !important; font-weight:600 !important; }

    section[data-testid="stSidebar"] { background: var(--panel); border-right:1px solid var(--line); }
    section[data-testid="stSidebar"] .stButton > button {
        width:100%; text-align:left; background:transparent; color:#E8E6E1;
        border:1px solid var(--line); border-radius:8px; padding:.55rem .75rem;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        border-color: var(--amber); color: var(--amber);
    }
    section[data-testid="stSidebar"] .stButton > button:focus-visible {
        outline:2px solid var(--amber); outline-offset:2px;
    }

    .stTextInput input {
        background: var(--panel); color:#E8E6E1; border:1px solid var(--line); border-radius:8px;
    }
    .stTextInput input:focus { border-color: var(--amber); box-shadow:0 0 0 1px var(--amber); }

    /* answer block */
    .answer-box { background: var(--panel); border:1px solid var(--line);
                  border-left:3px solid var(--amber); border-radius:8px; padding:1rem 1.25rem; }

    details[data-testid="stExpander"] { background: var(--panel); border:1px solid var(--line);
                                        border-radius:8px; }
    code, pre { background:#0E1016 !important; }
    .stCaption, [data-testid="stCaptionContainer"] { color: var(--muted); }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎬 Movie Graph RAG")
st.caption("Neo4j Movies knowledge graph + LLM")

EXAMPLES = [
    "Who acted in The Matrix?",
    "Which movies did Tom Hanks appear in?",
    "Who directed Cloud Atlas?",
    "Which actors worked most with Keanu Reeves?",
    "Recommend movies similar to Jerry Maguire",
    "What are the top rated movies?",
    "How is Kevin Bacon connected to Keanu Reeves?",
    "Movies released between 1995 and 2000",
    "What do reviewers say about Jerry Maguire?",
]
with st.sidebar:
    st.subheader("Try an example")
    for ex in EXAMPLES:
        if st.button(ex):
            st.session_state["q"] = ex

q = st.text_input("Ask a movie question", key="q")
if q:
    with st.spinner("Querying the graph..."):
        r = ask(q)
    st.markdown("### Answer")
    with st.container(border=True):
        st.write(r["answer"])
    with st.expander("How this was answered (grounding)"):
        st.write("**Template:**", r["template"])
        st.write("**Parameters:**", r["params"])
        if r["cypher"]:
            st.code(r["cypher"].strip(), language="cypher")
        st.write("**Retrieved rows:**")
        st.json(r["rows"])