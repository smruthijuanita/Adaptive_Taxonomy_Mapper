

TAXONOMY = {
    "Fiction": {
        "Romance": ["Slow-burn", "Enemies-to-Lovers", "Second Chance"],
        "Thriller": ["Espionage", "Psychological", "Legal Thriller"],
        "Sci-Fi": ["Hard Sci-Fi", "Space Opera", "Cyberpunk"],
        "Horror": ["Psychological Horror", "Gothic", "Slasher"]
    }
}

VALID_LEAVES = {
    leaf
    for genre in TAXONOMY["Fiction"].values()
    for leaf in genre
}

assert len(VALID_LEAVES) > 0, "Taxonomy has no leaf categories"
