# EVALUATION REPORT
**Date:** 15 September 2026

## Reproducible run included with the submission
The packaged evaluation was executed against the deterministic local backend so it can be rerun without API keys. It exercises the application request path, Pydantic contract, bilingual injection checks, Saudi PII masking, bounded authorized tool execution, outbound wall, usage/cost record creation, stratified golden-set reporting, tests, and regression gate.

## Results
See `eval/summary.json` and `eval/results.json`. Results are reported by slice rather than only as one aggregate number.

## Live-provider protocol
Run the exact same `data/golden_set.json` against `commercial_primary` and `open_weight`, save each result file, then run `scripts/compare_backends.py`. This prevents cherry-picking different test sets.

## Cost / latency protocol
For each request capture input, cached-input, output tokens, latency, evaluation verdict, and calculated cost. Prompt-cache usage counts only when the provider reports cached input. For self-hosting, measure throughput on the deployed hardware and pass it to `scripts/break_even.py`.

## LLM judge protocol
Use the written rubric one dimension at a time. Before using the judge as a release gate, obtain actual human labels for the calibration cases and run `eval/calibrate_judge.py` to report raw agreement and Cohen's kappa.

## Known limitations
This package does not include fabricated API benchmarks, fabricated open-weight throughput, fabricated cache-hit rates, or fabricated human labels. Those require actual credentials, infrastructure, and reviewers. The implementation and commands required to produce those artifacts are included.
