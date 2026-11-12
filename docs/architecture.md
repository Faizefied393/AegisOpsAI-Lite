# Architecture and threat model

Synthetic events -> FastAPI validation -> SQLite -> deterministic detection -> risk scoring -> Streamlit dashboard.

A selected alert and its referenced evidence are sent to a local Ollama model. The model receives no tools or system privileges. Pydantic validates the output schema; every finding must reference supplied evidence IDs. Invalid outputs fall back to deterministic summaries.

## Trust boundaries

1. Incoming events are untrusted and schema validated.
2. Protected API routes require a local demo API key.
3. The model is untrusted: event text can contain malicious instructions and must be treated as data.
4. The dashboard is a display layer; it does not issue containment commands.

## Production gaps

Authentication, per-user authorization, HTTPS, audit trail, rate limiting, immutable evidence retention, data minimization, logging, alert deduplication, scalability, monitoring, formal AI evaluation, and real integrations.
