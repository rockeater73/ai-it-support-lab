# AI IT Support Automation Lab

I'm building this project to explore how AI can be used in a realistic Tier 1 IT support workflow without relying on the model to know or invent company-specific procedures.

The system takes support requests, retrieves relevant IT procedures from a local knowledge base, and provides that context to a locally running LLM. The goal is to automate parts of ticket triage while keeping uncertain and security-sensitive decisions under human control.

## Architecture

```text
Outlook
   │
   ▼
Microsoft Graph
   │
   ▼
Email / Ticket Processing
   │
   ▼
Semantic SOP Retrieval
   │
   ▼
Local LLM (Ollama)
   │
   ▼
Policy Validation
   │
   ├── Tier 1 Guidance
   │
   └── Human Review
```

## Current Features

- Real Outlook email retrieval through Microsoft Graph
- OAuth authentication with delegated mailbox permissions
- Markdown-based IT procedure knowledge base
- Local embeddings and semantic SOP retrieval
- RAG-grounded ticket analysis using Llama 3
- Structured priority, category, and troubleshooting output
- Separation of user-safe and technician-only actions
- Confidence-based fallback when no relevant SOP is found
- Deterministic policy checks for security-sensitive tickets
- Retrieval and adversarial testing

## Why I Built It This Way

The project originally started as a simple LLM ticket classifier with predefined troubleshooting logic.

As I worked on it, I realized that approach wouldn't scale. A real IT team can't hard-code every possible issue an employee might submit. I changed the design so company SOPs could be added as documents and retrieved dynamically using embeddings.

That introduced a different problem: semantic search always returns the closest result, even when none of the available documents are actually relevant. An unsupported ticket could therefore retrieve unrelated documentation and give the LLM misleading context. I added a confidence threshold and human-review fallback to handle those cases.

I also separated policy enforcement from the LLM. The model can analyze a ticket, but decisions that should be consistently enforced, such as requiring review of security-related tickets, are handled by application logic instead.

These changes moved the project from a basic classifier toward the architecture below:

```text
Untrusted Support Request
          │
          ▼
    SOP Retrieval
          │
          ▼
   Confidence Check
          │
          ▼
     LLM Analysis
          │
          ▼
   Policy Validation
          │
     ┌────┴────┐
     ▼         ▼
 Tier 1     Human
 Guidance   Review
```

## Microsoft Graph Integration

The project is being connected to a dedicated Outlook test mailbox to move beyond simulated JSON tickets.

Microsoft Graph currently provides read-only email access using delegated `Mail.Read` permission. The application can authenticate through Microsoft Entra ID and retrieve messages from the test inbox.

The next step is connecting those messages directly to the existing RAG pipeline and generating technician-reviewed response drafts.

## Security

Because both support emails and retrieved documents can contain untrusted content, I'm also using the project to explore security problems specific to LLM-based automation.

Areas being tested include:

- Prompt injection through support requests
- Malicious or misleading retrieved content
- Unsupported LLM-generated procedures
- Unsafe escalation decisions
- Excessive permissions
- Risks of allowing model output to trigger automated actions

The LLM is currently advisory. Security policies and future automated actions are intended to be constrained by application logic rather than allowing arbitrary model-generated commands to execute.

## Project Structure

```text
knowledge_base/    IT SOPs used for retrieval
rag/               Embedding, indexing, and retrieval
tests/             Retrieval and adversarial tests
data/              Mock development data

ai_analyzer.py     RAG and LLM analysis
email_reader.py    Mock email ingestion
outlook_reader.py  Microsoft Graph email ingestion
ticket_processor.py
policy.py          Deterministic policy enforcement
process_inbox.py   End-to-end ticket processing
```

## Technologies

**Python · Microsoft Graph · Microsoft Entra ID · OAuth · Ollama · Llama 3 · embeddinggemma · RAG · Vector Embeddings · Git**

## Current Status

The core local RAG and policy pipeline is working, and Microsoft Graph can retrieve messages from a dedicated Outlook test mailbox.

I'm currently working on connecting the real mailbox directly to the ticket-processing pipeline. After that, I plan to add human-reviewed response drafting and expand the security/evaluation side of the project.

This is a learning lab, not a production help desk system.
