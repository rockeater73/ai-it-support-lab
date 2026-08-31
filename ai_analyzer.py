import json
import ollama

from rag.retriever import retrieve_relevant_sops

MIN_RETRIEVAL_SCORE = 0.45

TICKET_SCHEMA = {
    "type": "object",
    "properties": {
        "issue_summary": {
            "type": "string"
        },
        "category": {
            "type": "string"
        },
        "priority": {
            "type": "string",
            "enum": [
                "Low",
                "Medium",
                "High",
                "Critical"
            ]
        },
        "matched_procedures": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "user_steps": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "technician_actions": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "requires_human_review": {
            "type": "boolean"
        },
        "reason": {
            "type": "string"
        }
    },
    "required": [
        "issue_summary",
        "category",
        "priority",
        "matched_procedures",
        "user_steps",
        "technician_actions",
        "requires_human_review",
        "reason"
    ]
}


SYSTEM_PROMPT = """
You are an AI assistant supporting a Tier 1 IT help desk.

Your job is to analyze an incoming IT support ticket using the
company procedures provided to you.

The company documentation is the primary source of truth.

Rules:

1. Base company-specific troubleshooting and technician actions on
   the supplied documentation.

2. Do not invent company procedures.

3. Separate actions an end user can safely perform from actions that
   require an IT technician.

4. Do not tell users to perform administrative or privileged actions.

5. If the supplied documentation does not adequately address the
   issue, set requires_human_review to true.

6. If the documentation says the issue should be escalated, set
   requires_human_review to true and explain why.

7. Do not claim that an action has already been performed.

8. Do not request passwords, MFA codes, or authentication secrets.

Return only information required by the JSON schema.
"""


def build_knowledge_context(retrieval_results):
    sections = []

    for result in retrieval_results:
        section = (
            f"SOURCE: {result['source']}\n"
            f"SIMILARITY: {result['score']:.4f}\n\n"
            f"{result['text']}"
        )

        sections.append(section)

    return "\n\n" + ("=" * 60) + "\n\n".join(sections)

def analyze_ticket(ticket_text):
    retrieval_results = retrieve_relevant_sops(
        ticket_text,
        top_k=3
    )

    best_score = retrieval_results[0]["score"]

    if best_score < MIN_RETRIEVAL_SCORE:
        return {
            "issue_summary": "No matching SOP found for this ticket.",
            "category": "Unknown",
            "priority": "Medium",
            "matched_procedures": [],
            "user_steps": [],
            "technician_actions": [],
            "requires_human_review": True,
            "reason": (
                "No sufficiently relevant company SOP was found. "
                "Human review is required."
            ),
            "retrieval_results": [
                {
                    "source": result["source"],
                    "score": round(result["score"], 4)
                }
                for result in retrieval_results
            ]
        }

    knowledge_context = build_knowledge_context(
        retrieval_results
    )

    retrieved_sources = []

    for result in retrieval_results:
        if result["source"] not in retrieved_sources:
            retrieved_sources.append(result["source"])

    user_prompt = f"""
COMPANY DOCUMENTATION

{knowledge_context}

SUPPORT TICKET

{ticket_text}

The documentation above was retrieved automatically because it may
be relevant to the support ticket.

Analyze the ticket using the retrieved company documentation.

Retrieved source files:
{", ".join(retrieved_sources)}
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        format=TICKET_SCHEMA,
        options={
            "temperature": 0
        }
    )

    analysis = json.loads(
        response["message"]["content"]
    )

    analysis["retrieval_results"] = [
        {
            "source": result["source"],
            "score": round(result["score"], 4)
        }
        for result in retrieval_results
    ]

    return analysis