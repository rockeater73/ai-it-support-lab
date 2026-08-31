# AI IT Support Automation Lab

A Python-based Tier 1 IT support automation project that uses a local LLM and Retrieval-Augmented Generation (RAG) to analyze support requests using company-specific SOPs.

The goal is to automate common help desk triage without hard-coding every possible IT issue while maintaining human review for unsupported or security-sensitive tickets.

## Current Architecture

```text
Support Email
      |
      v
Email Reader
      |
      v
Ticket Processor
      |
      v
Semantic SOP Retrieval
      |
      v
Relevant Company Documentation
      |
      v
Local LLM Analysis
      |
      v
Policy Enforcement
      |
      +------------------+
      |                  |
      v                  v
Tier 1 Workflow     Human Review
```

## How It Works

Support requests are converted into structured tickets and analyzed against company procedures stored in `knowledge_base/`.

1. Company SOPs are converted into embeddings using `embeddinggemma`.
2. Incoming tickets are embedded and compared against the SOP index using cosine similarity.
3. The most relevant SOP chunks are supplied to a local Llama model through Ollama.
4. The LLM generates structured support analysis grounded in the retrieved documentation.
5. A retrieval-confidence gate prevents the model from generating troubleshooting guidance when no sufficiently relevant SOP exists.
6. A deterministic policy layer enforces rules that should not depend solely on LLM judgment.

The output separates:

- User-safe troubleshooting
- Technician-only actions
- Priority and category
- Human-review requirements

## Why RAG?

The application does not contain a large decision tree for every possible IT problem.

Instead, support procedures are stored as Markdown files:

```text
knowledge_base/
├── password_reset.md
├── phishing.md
├── printer.md
├── vpn.md
└── windows_performance.md
```

New procedures can be added to the knowledge base without creating issue-specific Python logic for every new support scenario.

## Retrieval Confidence

Semantic search will always return the closest documents, even when none are actually relevant.

To reduce unsupported troubleshooting, the application uses a minimum retrieval-confidence threshold.

```text
Relevant SOP Found
       |
       v
SOP + Ticket → LLM
       |
       v
Grounded Analysis
```

For an unsupported issue:

```text
Low Retrieval Confidence
       |
       v
No Troubleshooting Generated
       |
       v
Human Review
```

For example, a webcam issue with no corresponding SOP was correctly routed for human review rather than generating instructions from unrelated documentation.

The current confidence threshold is experimental and will require further evaluation as the test set and knowledge base grow.

## Policy Enforcement

LLM decisions are not treated as the final authority.

After analysis, a deterministic policy layer can override model decisions for cases that require guaranteed handling.

For example, security-related tickets are forced into human review even if the LLM determines that escalation is unnecessary.

```text
LLM Analysis
     |
     v
Policy Validation
     |
     +--> Normal Tier 1 Issue → Continue
     |
     +--> Security Issue → Human Review
     |
     +--> Critical Issue → Human Review
```

This separates flexible AI analysis from rules that should be consistently enforced by application logic.

## Current Inbox Processing

The application currently processes a simulated email inbox containing multiple IT support requests.

Example scenarios include:

- VPN authentication failure
- Suspected phishing
- Printer offline
- Slow Windows computer
- Account lockout

The current pipeline successfully processes all five mock emails through SOP retrieval, LLM analysis, and policy enforcement.

Example summary:

```text
Emails processed: 5
Tier 1 tickets: 4
Human review required: 1
Errors: 0
```

The phishing ticket is automatically routed for human review by the policy layer.

## Retrieval Testing

A small development test suite evaluates whether semantic retrieval selects the expected SOP.

Current result:

```text
Passed: 5/5
Top-1 Retrieval Accuracy: 100.0%
```

This is a small development test set and does not represent production-level accuracy.

The project also includes initial adversarial tests for prompt-injection behavior.

## Project Structure

```text
ai-it-support-lab/
|
├── knowledge_base/       # Company SOPs
├── rag/                  # Embedding and retrieval logic
├── tests/                # Retrieval and security tests
├── data/                 # Mock email and ticket data
│
├── ai_analyzer.py        # RAG + local LLM analysis
├── ticket_processor.py   # Ticket normalization and processing
├── email_reader.py       # Email intake
├── process_inbox.py      # Batch inbox processing
├── policy.py             # Deterministic safety/routing policies
├── app.py                # Manual testing interface
│
├── README.md
└── requirements.txt
```

## Technologies

- Python
- Ollama
- Llama 3
- embeddinggemma
- Vector embeddings
- Cosine similarity
- Retrieval-Augmented Generation (RAG)
- JSON structured output
- Git / GitHub

## Current Status

### Implemented

- Local LLM integration with Ollama
- Structured IT ticket analysis
- Mock email inbox processing
- Markdown-based company SOP knowledge base
- Local embedding generation
- Semantic SOP retrieval
- RAG-grounded support analysis
- User-safe vs. technician action separation
- Low-confidence fallback to human review
- Deterministic policy enforcement
- Security-ticket escalation
- Retrieval evaluation
- Initial prompt-injection testing

### Next

- Replace the mock inbox with Outlook using Microsoft Graph
- Generate technician-reviewed response drafts
- Expand the SOP knowledge base
- Expand retrieval and adversarial test coverage
- Improve confidence-threshold evaluation
- Add persistent ticket history
- Explore controlled endpoint remediation

## Planned Outlook Integration

The next major milestone is replacing the simulated inbox with real email intake:

```text
Microsoft Outlook
       |
       v
Microsoft Graph
       |
       v
Email Reader
       |
       v
Ticket Processor
       |
       v
RAG + SOP Retrieval
       |
       v
Local LLM
       |
       v
Policy Enforcement
       |
       +--> Tier 1
       |
       +--> Human Review
```

Initial versions will keep a human in the loop rather than automatically sending AI-generated responses.

## Security

Because emails and retrieved documents are untrusted inputs, the project also explores AI-specific security risks including:

- Prompt injection
- Indirect prompt injection
- Knowledge-base poisoning
- Retrieval manipulation
- Unsafe LLM recommendations
- Unauthorized instruction overrides

Future automated remediation will use explicitly approved actions enforced by application logic. LLM-generated commands will not be executed directly.

## Disclaimer

This project is a development and educational lab.

The current SOPs, policies, confidence threshold, and test results are simulated and are not intended for production deployment.