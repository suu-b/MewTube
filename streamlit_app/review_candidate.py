import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from config.config import OUTPUT_DIR, logger
from candidates_service.main import get_candidates
from models.candidate import Candidate
import streamlit as st
import json

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

title = "Review Candidates GUI"

@st.cache_resource
def log_init_app():
    logger.info("%s is up", title)

log_init_app()
st.set_page_config(page_title=title, layout="wide")
st.title(title)
logger.info("Collecting the candidates...")    
candidates = []

@st.cache_data
def load_candidates():
    logger.info("Loading candidates from disk")
    with open(OUTPUT_DIR / "pool_candidates_pool.jsonl", "r", encoding="utf-8") as f:
        return [Candidate.model_validate_json(line) for line in f]

candidates = load_candidates()
if not candidates:
    logger.warning("No candidate found.")

@st.cache_resource
def log_once(n):
    logger.info("Collected %d candidates", n)

log_once(len(candidates))

if "votes" not in st.session_state:
    st.session_state.votes = {}

def vote(candidate_id: str, value: int):
    st.session_state.votes[candidate_id] = value

cols = st.columns(3)

@st.cache_data
def get_image(url):
    return url


for i, item in enumerate(candidates):
    cid = item.id if hasattr(item, "id") else str(i)

    with cols[i % 3]:
        with st.container(border=True):
            st.image(item.thumbnail_url, width='stretch')
            st.markdown(f"**{item.title}**")
            st.caption(item.channel_title)
            st.write(item.description)

            choice = st.radio(
                "choice",
                ["👍", "👎"],
                index=st.session_state.votes.get(cid),
                key=f"vote_{cid}",
                horizontal=True,
                label_visibility="collapsed",
            )

            if choice is not None:
                st.session_state.votes[cid] = 0 if choice == "👎" else 1






    
