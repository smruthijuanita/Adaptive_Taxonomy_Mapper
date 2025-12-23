import streamlit as st
from mapper import map_story
from golden_set import TEST_CASES

st.set_page_config(page_title="Story Inference Engine", layout="wide")

st.title("📚 Story Genre Inference Engine")
st.caption("Prototype for mapping messy user tags to a strict internal taxonomy")

st.markdown("### Golden Set Evaluation")

results = []
for case in TEST_CASES:
    mapping = map_story(case["tags"], case["blurb"])
    results.append({
        "ID": case["id"],
        "User Tags": ", ".join(case["tags"]),
        "Blurb": case["blurb"],
        "Mapped Category": mapping["category"],
        "Confidence": round(mapping["confidence"], 2),
        "Reasoning": mapping["reasoning"]
    })


st.dataframe(results, use_container_width=True)

st.markdown("---")
st.markdown("### 🔍 Manual Test")

tags = st.text_input("User Tags (comma-separated)", "Love, Sad")
blurb = st.text_area("Story Blurb", "They met again after decades apart...")

if st.button("Run Inference"):
    if not tags.strip():
        st.error("Please enter at least one tag.")
        st.stop()

    if not blurb.strip():
        st.error("Please enter a story blurb.")
        st.stop()

    if len(blurb) > 2000:
        st.error("Blurb is too long.")
        st.stop()

    result = map_story(tags.split(","), blurb)
    confidence = result["confidence"]
    if confidence >= 0.75:
        st.success(f"Mapped Category: **{result['category']}**")
    elif confidence >= 0.4:
        st.warning(f"Mapped Category: **{result['category']}**")
    else:
        st.error(f"Mapped Category: **{result['category']}**")

    st.metric("Confidence Score", f"{confidence:.2f}")
    st.info(f"Reasoning: {result['reasoning']}")

    if confidence >= 0.75:
        st.caption("🟢 High confidence (rule-based match)")
    elif confidence >= 0.4:
        st.caption("🟡 Medium confidence (LLM-assisted)")
    else:
        st.caption("🔴 Low confidence (weak or unmapped)")
