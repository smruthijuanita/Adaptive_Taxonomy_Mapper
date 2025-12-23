# Adaptive Taxonomy Mapper

## Overview
The Adaptive Taxonomy Mapper is a prototype inference engine that converts noisy, user-generated tags and story descriptions into a structured internal taxonomy. The system is designed to handle misleading tags, ambiguous inputs, and out-of-scope content while strictly adhering to a predefined taxonomy hierarchy.

The mapper prioritizes semantic context over surface-level tags, provides transparent reasoning for each decision, and avoids hallucinating categories that do not exist in the taxonomy.

---

## Problem Context
User-generated content is often tagged imprecisely (e.g., “Love”, “Scary”, “Action”), while recommendation systems require high-precision classifications such as *Enemies-to-Lovers* or *Psychological Horror*.

This project bridges that gap by mapping messy inputs to a clean, internal taxonomy using a combination of:
- Context-driven reasoning
- Taxonomy-aware validation
- Controlled LLM inference

---

## Design Principles

### 1. Context Wins Rule
When user tags conflict with the story description, the system prioritizes narrative context.

**Example**  
User tag: `Action`  
Story: Courtroom cross-examination  
→ Mapped to **Legal Thriller**, not Action & Adventure.

---

### 2. Honesty Rule
If a story does not belong to any category in the taxonomy, the system outputs:
[UNMAPPED]

This prevents forced or misleading classifications.

---

### 3. Hierarchy Rule
All outputs must strictly follow the taxonomy hierarchy:

Fiction → Genre → Sub-Genre


The system never invents new categories or sub-genres.

---

## Taxonomy Structure
The internal taxonomy is defined in `taxonomy.json` and follows this structure:

```json
{
  "Fiction": {
    "Romance": ["Slow-burn", "Enemies-to-Lovers", "Second Chance"],
    "Thriller": ["Espionage", "Psychological", "Legal Thriller"],
    "Sci-Fi": ["Hard Sci-Fi", "Space Opera", "Cyberpunk"],
    "Horror": ["Psychological Horror", "Gothic", "Slasher"]
  }
}
```

## How the System Works
1. Input Ingestion:
- User tags and story description are processed together.
2. LLM Reasoning
- The model analyzes semantic meaning, ignoring misleading tags when necessary.
- A short reasoning explanation is generated.
3. Taxonomy Validation
- Outputs are checked against the taxonomy JSON.
- Invalid or unknown categories are rejected.
4. Final Output
- Returns either a valid sub-genre or [UNMAPPED]
- Includes a concise reasoning log.

## Running the code:
1. Set environment variables: Create a .env file locally
   GROQ_API_KEY=your_api_key_here

2. Run : python app.py

## Security Notes
- API keys are managed using environment variables
- Secrets are excluded from version control via .gitignore
- No credentials are stored in code or commits

