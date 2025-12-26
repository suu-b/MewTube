from datetime import datetime, timezone
import sys
from pathlib import Path
import json
import streamlit as st

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from config.config import OUTPUT_DIR, logger
from models.candidate import Candidate
from models.reviewed_candidate import ReviewedCandidate

# Title
TITLE = "Review Candidates GUI"
st.set_page_config(page_title=TITLE, layout="wide")
st.title(TITLE)

# Logging
@st.cache_resource
def log_init():
    logger.info("%s is up", TITLE)

log_init()

# Load Candidates
@st.cache_data
def load_candidates():
    logger.info("Loading candidates from disk")
    with open(OUTPUT_DIR / "pool_candidates_pool.jsonl", "r", encoding="utf-8") as f:
        return [Candidate.model_validate_json(line) for line in f]

candidates = load_candidates()
# Just for testing
# candidates = candidates[0:14]

n = len(candidates)
logger.info("Collected %d candidates", n)

if not candidates:
    st.warning("No candidates found.")
    st.stop()

# Session state for votes
if "votes" not in st.session_state:
    st.session_state.votes = {}

if "page" not in st.session_state:
    st.session_state.page = 0;

# Pagination
# Streamlit application at each interaction with the UI triggers a rerun of the whole script consequently of the cards as well. We do 
# not want hundreds of cards being loaded all over again at our each choice. Therefore, instead we use pagination.
PAGE_SIZE = 12
MAX_PAGE = (n - 1) // PAGE_SIZE

all_voted = len(st.session_state.votes) == n

# Submits Review
def submit_reviewer(reviewed_candidates):
    with open(OUTPUT_DIR / f"reviewed_candidates.jsonl", "a", encoding="utf-8") as f:
        for c in reviewed_candidates:
            f.write(json.dumps(c.model_dump(mode="json"), ensure_ascii=False) + "\n")
    logger.info("Reviewed Submitted!")

def to_reviewed_candidate(c, liked, reviewed_at) -> ReviewedCandidate:
    return ReviewedCandidate(**c.model_dump(), liked = liked, reviewed_at = reviewed_at)

if st.button("Submit", disabled=not all_voted):
    votes = st.session_state.votes
    reviewed_at = datetime.now(timezone.utc)
    reviewed_candidates = [to_reviewed_candidate(c, liked = votes[c.video_id], reviewed_at = reviewed_at) for c in candidates]
    submit_reviewer(reviewed_candidates)
    logger.info(st.session_state.votes)

# Buttons for going prev or next
col_prev, col_info, col_next = st.columns([1, 2, 1])

with col_prev:
    if st.button("← Prev", disabled=st.session_state.page == 0):
        st.session_state.page -= 1
        st.rerun()

with col_next:
    _, right = st.columns([3, 1])
    with right:
        if st.button("Next →", disabled=st.session_state.page == MAX_PAGE):
            st.session_state.page += 1
            st.rerun()

# Printing the page info on top
with col_info:
    _, center, _ = st.columns([1, 1, 1])
    with center:
        st.markdown(
            f"Page **{st.session_state.page + 1}** / **{MAX_PAGE + 1}**"
        )

# Pagination in action
start = st.session_state.page * PAGE_SIZE
end = start + PAGE_SIZE
page_candidates = candidates[start:end]


# Define each card to render individually than the whole page. This will let it be isolated without triggering other cards to render
@st.fragment
def render_card(item: Candidate, cid: str):
    with st.container(border=True, key=f"card_{cid}"):
        st.image(item.thumbnail_url, width='stretch')
        st.markdown(f"**{item.title}**")
        st.caption(item.channel_title)
        st.write(item.description)

        choice = st.radio(
            "vote",
            ["👍", "👎"],
            index=st.session_state.votes.get(cid),
            key=f"vote_{cid}",
            horizontal=True,
            label_visibility="collapsed",
        )

        if choice is not None:
            st.session_state.votes[cid] = 1 if choice == "👍" else 0

# Render the grid
cols = st.columns(3)
for i, item in enumerate(page_candidates):
    cid = item.video_id
    with cols[i % 3]:
        render_card(item, cid)
