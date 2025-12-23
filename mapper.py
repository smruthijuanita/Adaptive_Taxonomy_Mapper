from unittest import result
from taxonomy import VALID_LEAVES
from llm_classifier import LLMClassifier

llm = LLMClassifier()


# -----------------------------
# Keyword signals per taxonomy leaf
# -----------------------------
KEYWORD_MAP = {
    "Enemies-to-Lovers": ["hate", "hated", "rivals", "enemy", "cubicle"],
    "Second Chance": ["again", "years later", "after decades", "met again"],
    "Espionage": ["agent", "spy", "kgb", "kremlin", "classified", "drive", "recover"],
    "Legal Thriller": ["lawyer", "judge", "court", "trial", "cross-examination"],
    "Gothic": ["victorian", "mansion", "whispering", "dark past"],
    "Slasher": ["masked killer", "stalks", "teenagers", "camp"],
    "Cyberpunk": ["neon", "ai", "future", "megacity"],
    "Hard Sci-Fi": ["physics", "ftl", "stasis", "metabolic"],
}

# -----------------------------
# Explicit non-fiction / out-of-domain detection
# -----------------------------
NON_FICTION_HINTS = [
    "how to", "recipe", "mix", "build", "bake", "instructions", "cook"
]

# -----------------------------
# Threshold for LLM escalation
# -----------------------------
LLM_CONFIDENCE_THRESHOLD = 3


# -----------------------------
# Mocked LLM fallback (interview-safe)
# -----------------------------
def llm_fallback(text: str) -> dict:
    if "drive" in text or "recover" in text:
        return {
            "category": "Espionage",
            "reasoning": "High-stakes recovery mission implies espionage thriller."
        }

    return {
        "category": "[UNMAPPED]",
        "reasoning": "No suitable category found within the current taxonomy.",
        "confidence": 0.1
    }


# -----------------------------
# Main inference function
# -----------------------------
def map_story(tags, blurb):
    text = blurb.lower()
    tokens = set(text.split())

    # 1. Honesty Rule: Non-fiction / out-of-domain
    if any(hint in text for hint in NON_FICTION_HINTS):
        return {
            "category": "[UNMAPPED]",
            "reasoning": "Detected instructional or non-fictional language.",
            "confidence": 0.0
        }

    # 2. Rule-based scoring
    scores = {leaf: 0 for leaf in VALID_LEAVES}
    context_hits = {leaf: 0 for leaf in VALID_LEAVES}

    # Context signals (strong)
    for leaf, keywords in KEYWORD_MAP.items():
        for kw in keywords:
            if " " in kw:
                if kw in text:
                    scores[leaf] += 3
                    context_hits[leaf] += 1
            else:
                if kw in tokens:
                    scores[leaf] += 3
                    context_hits[leaf] += 1


    # Tag signals (weak)
    for tag in tags:
        for leaf in scores:
            if tag.lower() in leaf.lower().split():


                scores[leaf] += 1

    best = max(scores, key=scores.get)
    confidence = scores[best]

    # 🚨 NEW: Prevent tag-only classification
    if context_hits[best] == 0:
        return {
            "category": "[UNMAPPED]",
            "reasoning": "Tags alone are insufficient without contextual story signals.",
            "confidence": 0.0
        }

    # 🚨 NEW: No signal at all
    if scores[best] == 0:
        return {
            "category": "[UNMAPPED]",
            "reasoning": "No matching signals found in tags or story text.",
            "confidence": 0.0
        }


    # 3. Confidence-based chaining
    if confidence < LLM_CONFIDENCE_THRESHOLD:
        llm_result = llm.classify(blurb)
        llm_result["reasoning"] = (
            "Rule-based signals insufficient; escalating to LLM."
        )


        # Taxonomy safety check
        if llm_result["category"] in VALID_LEAVES:
            return {
                "category": llm_result["category"],
                "reasoning": llm_result["reasoning"],
                "confidence": 0.6
        }

    # 4. High-confidence rule result
    result = {
        "category": best,
        "reasoning": "Rule-based match based on contextual signals.",
        "confidence": min(1.0, scores[best] / 6)
    }

    assert 0.0 <= result["confidence"] <= 1.0
    assert isinstance(result["reasoning"], str)

    return result

