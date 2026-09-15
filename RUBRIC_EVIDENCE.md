# RUBRIC EVIDENCE MAP
**Date:** 15 September 2026

This file is the grader's shortest path through the submission.

| Rubric requirement | Evidence |
|---|---|
| Provider SDK actually called | `src/ai_engineering/providers.py` - OpenAI Responses / Anthropic SDK |
| Typed model boundary | `ProviderBoundary(ABC)` in `providers.py` |
| Model IDs from config/aliases | `config.yaml`, `config.py::resolve_model` |
| Retry/backoff/fallback policy | `service.py`; `docs/ADR-001.md` |
| ADR / decisions record | `docs/ADR-001.md` |
| Pydantic output contract | `schemas.py::AssistantOutput` |
| Schema-constrained generation | `providers.py::generate_structured` |
| Validate -> retry -> repair | `service.py::handle_request` |
| Real tool definitions/execution | `providers.py::TOOL_DEFINITIONS`, `tools.py` |
| Bounded loop + authorization gate | `service.py`, `tools.py::AuthorizationContext` |
| Versioned prompts | `prompts/system_ar.txt`, `prompts/system_en.txt` |
| Injection tests both languages | `safety.py`, `tests/test_safety.py`, golden set |
| Saudi PII before model/log | `safety.py::mask_saudi_pii`, first service stage |
| Outbound canary/leak + PII wall | `safety.py::outbound_wall` |
| Named testable request stages | `service.py` usage `stages` record |
| Versioned stratified golden set | `data/golden_set.json` |
| Harness runs golden set | `eval_runner.py` |
| Deterministic safety assertions | `eval_runner.py`, Promptfoo config |
| LLM-as-judge written rubric | `eval/JUDGE_RUBRIC.md` |
| Judge calibration + Cohen's kappa | `eval/calibrate_judge.py` (requires real human labels) |
| Regression gate can block | `scripts/regression_gate.py` |
| Per-request usage -> cost record | `costing.py` |
| Prompt-cache observed | provider usage -> `cached_input_tokens` -> `observed_prompt_cache` |
| Stable prefix / volatile tail | prompt files + ADR |
| Safe response-cache key | `cache.py` |
| Before/after cost + eval verdict path | backend result JSON + comparison script |
| Commercial and open-weight adapters | `config.yaml`, `providers.py` |
| Same golden set / by-slice comparison | `scripts/run_backend.py`, `compare_backends.py` |
| Self-host break-even from throughput | `scripts/break_even.py` |
| One-entry-point README | `README.md` |
| Evaluation report + limitations | `EVALUATION_REPORT.md` |

## Evidence status
- **Executed in this package:** deterministic mock golden-set run, unit tests, regression gate.
- **Executable but requires external evidence:** commercial live run, open-weight live endpoint run, observed provider prompt-cache hits, measured self-host throughput, and human-label judge calibration.
- These external measurements are deliberately not fabricated.
