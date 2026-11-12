# AegisOps AI X — Six-hour zero-to-demo runbook

## 0:00–0:40 | Setup
- Extract ZIP in WSL Ubuntu; `cd aegisops-ai-lite && code .`
- `python3 -m venv .venv && source .venv/bin/activate`
- `python -m pip install -e '.[dev]'`
- `cp .env.example .env`; replace `AEGIS_API_KEY` with a long random secret from `python -c "import secrets; print(secrets.token_urlsafe(32))"`.
- `set -a; source .env; set +a`
- `python -m pytest -q && python scripts/check_all.py`
- Screenshot 01: VS Code Explorer, save `docs/screenshots/01-project.png`.

## 0:40–1:20 | API and seed
- Terminal 1: `python -m uvicorn app.main:app --reload`
- Open `http://127.0.0.1:8000/docs`; screenshot 02 `02-api.png`.
- Terminal 2: activate environment and source .env.
- `curl -s -X POST http://127.0.0.1:8000/demo/seed -H "X-API-Key: $AEGIS_API_KEY"`
- `curl -s http://127.0.0.1:8000/alerts -H "X-API-Key: $AEGIS_API_KEY" | python -m json.tool`
- Screenshot 03 `03-alerts.png`. Verify unauthenticated request returns 401.

## 1:20–2:10 | Sigma, CISA KEV, ML
- Inspect `detections/sigma/failed_logins.yml` and `app/sigma.py`: selection interpreter only; Python correlator handles five failures in ten minutes.
- `curl -s http://127.0.0.1:8000/extensions/sigma -H "X-API-Key: $AEGIS_API_KEY" | python -m json.tool`; screenshot 04 `04-sigma.png`.
- `python scripts/run_live_kev.py` to fetch CISA KEV; if offline use `data/kev_sample.json`. Screenshot 05 `05-kev.png`. Demo CVE-to-asset mapping is fictional, not a verified software inventory.
- `python ml/train.py`; inspect `artifacts/ml_metrics.json`. Screenshot 06 `06-ml.png`. Labels are synthetic and rule-generated, so model performance is not real-world detection quality.

## 2:10–3:10 | Ollama and LangGraph
- `ollama pull llama3.2:3b`; check `curl http://127.0.0.1:11434/api/tags`. If Windows Ollama is unreachable from WSL, follow Microsoft WSL networking guidance and set OLLAMA_URL.
- `curl -s -X POST http://127.0.0.1:8000/extensions/agent/AUTH-BRUTE-FORCE-auth-fail-5 -H "X-API-Key: $AEGIS_API_KEY" | python -m json.tool`
- Confirm `review_status: PENDING_HUMAN_REVIEW` and report mode. Screenshot 07 `07-agent.png`.
- Read `app/agent.py`: graph enrich -> investigate -> review gate. Review gate marks pending only; it does not implement a persisted approval system.

## 3:10–3:55 | promptfoo evaluation
- Requires Node.js >=22.22.0 (see promptfoo docs). `node --version`
- `npx promptfoo@latest eval -c evaluations/promptfooconfig.yaml`
- Screenshot 08 `08-promptfoo.png` with pass/fail counts. These are local prompt robustness smoke tests against Ollama, NOT a full end-to-end red-team assessment. They may fail; document findings.
- Avoid default hosted red-team generation if you need local-only processing.

## 3:55–4:35 | OpenTelemetry + Trivy
- Restart FastAPI with `export AEGIS_ENABLE_TRACING=1; python -m uvicorn app.main:app --reload`.
- Call `/health`; observe JSON trace spans in server console. Screenshot 09 `09-tracing.png`.
- Install Trivy from official docs, then `bash scripts/scan.sh`. Inspect `artifacts/trivy.json`; screenshot 10 `10-trivy.png` with a concise terminal summary. Review findings before publishing.

## 4:35–5:20 | Integrated dashboard and tests
- Terminal 3: activate env and load .env; `python -m streamlit run dashboard/app.py`.
- Seed demo, inspect alerts and new extension buttons. Screenshot 11 `11-dashboard.png`.
- `python -m pytest -v`; screenshot 12 `12-tests.png`.

## 5:20–6:00 | GitHub + business demo
- Read `docs/business-case.md`; record actual elapsed investigation times, do not invent ROI.
- Include screenshots in README using `![Dashboard](docs/screenshots/11-dashboard.png)` etc.
- `git init && git branch -M main && git add . && git status`; ensure .env, DB, model artifacts, scan results, and tokens are NOT staged.
- `git commit -m "Build AegisOps AI X seven-tool security reference platform"`; publish using VS Code Source Control.
- Verify Actions tab. Screenshot 13 `13-ci.png`, commit it.
- Five-minute demo: business problem (30s), detection (60s), KEV + ML (60s), LangGraph + AI (90s), promptfoo + Trivy + traces (45s), business limitations (15s).

## Troubleshooting
- `ModuleNotFoundError`: activate .venv and install dependencies.
- `401`: source .env in BOTH backend and CLI terminals.
- Ollama fallback: verify URL and model; fallback is labeled, not LLM success.
- promptfoo unavailable: record as pending external dependency and continue.
- KEV unavailable: use bundled offline fixture, explicitly labeled as not current.
- Trivy unavailable: record pending scan; do not claim clean results.

## References
- https://fastapi.tiangolo.com/tutorial/
- https://github.com/SigmaHQ/sigma
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- https://scikit-learn.org/stable/
- https://docs.langchain.com/oss/python/langgraph/overview
- https://docs.ollama.com/api
- https://www.promptfoo.dev/docs/getting-started/
- https://opentelemetry.io/docs/languages/python/
- https://trivy.dev/docs/latest/getting-started/installation/
- https://docs.github.com/en/actions
