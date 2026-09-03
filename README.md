# AI IT Support Automation Lab

I'm building this project to learn how AI could realistically be used in a Tier 1 IT support workflow.

The basic idea is to take an incoming support email, find the company's relevant IT procedure, and give that information to a local LLM instead of relying on the model to make up troubleshooting steps.

## Current Workflow

```text
Outlook Email
     ↓
Microsoft Graph
     ↓
Ticket Processing
     ↓
SOP Retrieval (RAG)
     ↓
Local Llama 3 Model
     ↓
Policy Checks
     ↓
Tier 1 Guidance / Human Review
```

## What Works So Far

- Reads real emails from a test Outlook inbox using Microsoft Graph
- Uses OAuth delegated `Mail.Read` permission
- Stores IT procedures as Markdown files
- Creates embeddings locally with Ollama
- Retrieves relevant SOPs using cosine similarity
- Sends the ticket + retrieved SOPs to Llama 3
- Separates user troubleshooting from technician actions
- Sends low-confidence tickets to human review
- Forces security and critical tickets through additional policy checks

## Example

**Incoming ticket:**

> GlobalProtect says authentication failed, but I can sign into Microsoft 365 normally.

**Retrieved SOPs:**

```text
vpn.md                0.7345
password_reset.md     0.4110
printer.md            0.3996
```

**Result:**

```text
Category: VPN
Priority: High

User Steps:
1. Close and reopen the VPN client.
2. Confirm Microsoft 365 login works.
3. Get the exact VPN error message.

Human Review: False
```

![VPN ticket being processed](docs/images/vpn-demo.png)

## Things I Changed While Building It

The first version was basically an LLM ticket classifier. I realized pretty quickly that hard-coding troubleshooting for every possible IT problem wasn't realistic.

I changed the project to use RAG so the model could reference company procedures instead.

That created another problem: semantic search always returns *something*. A webcam ticket was matching unrelated Windows and VPN documentation, and the model was still generating troubleshooting from it.

I added a retrieval-confidence threshold so tickets without a strong SOP match are sent to a human instead.

I also found that the LLM sometimes made escalation decisions I didn't agree with. A phishing ticket was classified correctly as Security but still returned `requires_human_review: False`. I added a separate deterministic policy layer so security and critical tickets don't rely entirely on the model's judgment.

## Testing

Current retrieval test set:

```text
VPN                  PASS
Account lockout      PASS
Printer              PASS
Phishing             PASS
Windows performance  PASS

Top-1: 5/5
```

This is still a very small test set. One of my next goals is to expand it with ambiguous, unsupported, and adversarial tickets instead of treating 5/5 as meaningful production accuracy.

I also have adversarial tests for prompt injection. The early version failed all four initial injection tests, which is something I plan to revisit after the main workflow is complete.

## Tech I'm Using

Python • Ollama • Llama 3 • embeddinggemma • Microsoft Graph • Microsoft Entra ID • OAuth • RAG • Git/GitHub

## Next

- Finish Outlook → RAG processing end-to-end
- Generate technician-reviewed response drafts
- Expand the evaluation dataset
- Re-test prompt injection against the newer architecture
- Document the security improvements and results

This is a learning project and isn't intended to be a production help desk system.
