# AegisOps AI X — AI Security Operations & Business Risk Intelligence

**Six-hour portfolio reference build | Synthetic data only | Not production-ready**

An integrated Python/FastAPI/SQLite/Streamlit project demonstrating seven technologies:
Sigma YAML detection selection, CISA KEV enrichment, scikit-learn synthetic classification, LangGraph investigation orchestration, promptfoo local adversarial checks, OpenTelemetry console traces, and Trivy repository scanning.

**Start here:** [Six-hour step-by-step guide](docs/SIX_HOUR_BUILD.md).

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
cp .env.example .env
# Edit .env to set AEGIS_API_KEY
set -a; source .env; set +a
python -m pytest -q
python scripts/check_all.py
python -m uvicorn app.main:app --reload
```

In a second terminal with the same environment:
```bash
python -m streamlit run dashboard/app.py
```

## Architecture
Synthetic events → FastAPI/SQLite → deterministic detections + Sigma selection → risk and CISA KEV context → experimental ML → LangGraph + Ollama investigation → human review status → Streamlit. OpenTelemetry instruments API requests. promptfoo and Trivy provide separate test evidence.

## Security and limitations
- Shared demo API key, not user identity or RBAC. Keep localhost only.
- The Sigma file is parsed by a deliberately limited selector; it is not a general Sigma execution engine.
- CISA KEV offline fixture is not current. The synthetic asset/CVE mapping is hypothetical.
- ML labels are derived from rules on generated synthetic features; metrics cannot be generalized to real incidents.
- LangGraph review gate only records `PENDING_HUMAN_REVIEW`; it does not perform actions or persist approvals.
- Promptfoo config checks model prompt behavior, not the complete API/agent pipeline.
- OpenTelemetry uses console spans and may include request metadata; do not publish sensitive traces.
- Trivy findings require human triage; a passing scan does not guarantee security.
- AI summaries are advisory, evidence IDs are validated but natural-language claims still require review.

## Evidence
Capture screenshots as specified in [the runbook](docs/SIX_HOUR_BUILD.md), and add selected images here after you have actually captured them.

## Business evaluation
See [business case](docs/business-case.md). Measure analyst time and correctness before claiming productivity gains.
