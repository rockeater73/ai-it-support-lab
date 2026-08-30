# AI IT Support Automation Lab

A Python-based IT support automation project that uses a local LLM and retrieval-augmented generation (RAG) to analyze support requests using company-specific SOPs and procedures.

## Project Goal

The goal is to build an AI-assisted Tier 1 IT support system that can:

- Ingest support requests from email
- Convert emails into structured support tickets
- Retrieve relevant company SOPs using semantic search
- Use a local LLM to analyze tickets using retrieved documentation
- Provide user-safe troubleshooting guidance
- Route or escalate tickets when appropriate
- Eventually integrate with Microsoft Graph for Outlook email intake
- Evaluate the system against prompt injection and other AI security risks

## Current Architecture

Support Email
    ↓
Email Reader
    ↓
Ticket Processor
    ↓
SOP Retrieval (RAG)
    ↓
Local LLM (Ollama)
    ↓
Ticket Analysis / Routing

## Current Status

Implemented:

- Local Ollama LLM integration
- Structured IT ticket analysis
- Modular ticket processing
- Mock email inbox processing
- Basic escalation rules
- Baseline evaluation tests
- Prompt injection test suite
- Initial SOP knowledge base
- Local embeddings using embeddinggemma
- Semantic SOP retrieval using cosine similarity

In Progress:

- Expanding the SOP knowledge base
- Measuring retrieval accuracy
- Connecting retrieved SOPs to the ticket analysis pipeline

Planned:

- Microsoft Graph / Outlook integration
- Persistent ticket storage
- Human-in-the-loop response generation
- RAG security testing
- Prompt injection mitigations
- Controlled IT remediation actions