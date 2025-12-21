import streamlit as st
import json

st.set_page_config(page_title="MewTube | Dummy Client", layout="wide")
st.image("./mew.png", width=200)
st.title("MewTube Client")

with open("../output.json", "r") as f:
    cards = json.load(f)

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

for row_idx, row_cards in enumerate(chunk_list(cards, 3)):
    cols = st.columns(len(row_cards))
    for col_idx, (col, card) in enumerate(zip(cols, row_cards)):
        with col:
            title = card["snippet"]["title"]
            thumbnail = card["snippet"]["thumbnails"]["high"]["url"]
            description = card["snippet"]["description"]

            video_id = card.get("id", f"{row_idx}-{col_idx}")

            st.image(thumbnail)
            st.markdown(f"### {title}")
            st.write(description)

            st.button(
                "Watch",
                key=f"watch-{video_id}"
            )
