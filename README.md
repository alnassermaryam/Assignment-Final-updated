# LLM Application Engineering Project
**Date:** 15 September 2026

A production-style bilingual AI application that maps directly to the supplied grading rubric: provider boundary, structured outputs, real tool execution controls, prompt/security pipeline, versioned evaluation, cost/latency telemetry, commercial-vs-open-weight comparison, regression gating, and reproducible delivery.

## One entry point: from clone to a running conversation
```bash
git clone <repository-url>
cd project
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .
python -m ai_engineering.cli --interactive
```
The default `mock` backend makes the application runnable without secrets. For a live provider, set `AI_MODEL_ALIAS=commercial_primary`, `commercial_fallback`, or `open_weight` and provide the corresponding API key/base URL.

## Exact rubric coverage
### 1) Architecture and model boundary
- A provider SDK is actually called in `providers.py` (OpenAI Responses and Anthropic SDK paths).
- `ProviderBoundary` is an ABC typed boundary; business logic never calls SDKs directly.
- Model IDs are resolved from `config.yaml` aliases.
- Retry/backoff is at the boundary; fallback rules are documented in `docs/ADR-001.md`.
- ADR records model/provider decisions.

### 2) Structured outputs and function/tool execution
- `schemas.py` defines a Pydantic contract with validators.
- Provider-native schema-constrained generation is requested.
- `service.py` implements validate -> retry -> repair.
- `providers.py` contains strict tool definitions; `tools.py` contains the real implementation.
- The execution path is bounded and authorization-gated.

### 3) Prompt path and safety barriers
- Prompts are versioned files in `prompts/`, not business-logic literals.
- Arabic and English deterministic injection patterns are tested.
- Saudi ID/mobile PII is masked before model/log exposure.
- An outbound wall checks system-prompt leakage and outbound PII.
- Request stages are named and individually testable.

### 4) Evaluation platform, golden set, and regression gate
- `data/golden_set.json` is a versioned, stratified dataset.
- `eval_runner.py` runs the golden set through the application.
- Deterministic safety claims use contains/not-contains/schema/Python checks.
- `eval/JUDGE_RUBRIC.md` defines one-dimension-at-a-time LLM judging.
- `eval/calibrate_judge.py` computes agreement and Cohen's kappa after real human labels are supplied.
- `scripts/regression_gate.py` can block a build when the committed baseline is violated.

### 5) Cost, latency, and caching
- Every request records input/output/cached-input tokens and latency.
- `costing.py` turns observed usage into a cost record.
- Prompt-cache use is marked `observed_prompt_cache` from actual provider metadata; it is never assumed.
- Stable system prefix and volatile user tail are deliberate and documented.
- `cache.py` includes all answer-changing dimensions in the response-cache key.
- Backend reports can place the evaluation verdict beside cost/latency for before/after analysis.

### 6) Commercial vs open-weight comparison
Use the same golden set for both:
```bash
AI_MODEL_ALIAS=commercial_primary python scripts/run_backend.py eval/commercial.json
AI_MODEL_ALIAS=open_weight python scripts/run_backend.py eval/open_weight.json
python scripts/compare_backends.py eval/commercial.json eval/open_weight.json
```
The comparison is by slice, not one overall number. The open-weight alias is OpenAI-compatible so it can target vLLM or another compatible self-hosted server.

Self-host break-even is computed only from measured throughput:
```bash
python scripts/break_even.py --infra-hourly-usd 1.20 --measured-rps 12.5 --api-cost-per-request-usd 0.0008
```
Replace the example arguments with measured deployment values; the project does not invent benchmark results.

## Evaluation and tests
```bash
python -m ai_engineering.eval_runner
pytest -q
python scripts/regression_gate.py eval/summary.json
```
Optional Promptfoo live comparison:
```bash
npx promptfoo@latest eval -c eval/promptfooconfig.yaml --no-cache
```

## Deliverables
- `README.md`: direct run instructions.
- `RUBRIC_EVIDENCE.md`: grader-oriented evidence map.
- `EVALUATION_REPORT.md`: executed local run + known limitations.
- `docs/ADR-001.md`: architecture decision record.
- `eval/`: golden-set results, judge rubric, calibration utility, Promptfoo suite.
- `scripts/`: backend comparison, break-even, and regression gate.
- `tests/`: deterministic safety/schema tests.

## Integrity note
The included deterministic local run is real and reproducible. Live commercial/open-weight measurements, prompt-cache hits, throughput, and human-judge calibration must come from actual credentials/infrastructure/reviewers; this repository provides the complete executable path and does not fabricate those measurements.
