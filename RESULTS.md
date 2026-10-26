# Completed results: best measured 3/9

Snapshot: October 26, 2026. **One fixed assistance-and-coverage model meets 3 of the 9 fixed project targets: AIME 2025, Minerva Math and GPQA-Diamond.** All nine benchmarks completed for each model below. The three targets are historical reference thresholds, not an official leaderboard rank. We do not combine different models' best scores per benchmark.

All table entries are **pass@8**, except where labeled. A question is solved if at least one of eight answers is correct.

| Benchmark | Base | Random SFT | Advanced SFT | Best: assistance + coverage | Best solved | Required solved | Target |
|---|---:|---:|---:|---:|---:|---:|---|
| AMC | 77.50% | 77.50% | 70.00% | 70.00% | 28/40 | 33 | Below |
| AIME 2025 | 13.33% | 13.33% | 20.00% | 26.67% | 8/30 | 8 | Met |
| AIME 2024 | 23.33% | 20.00% | 16.67% | 20.00% | 6/30 | 8 | Below |
| MATH-500 | 85.20% | 84.20% | 85.00% | 88.20% | 441/500 | 451 | Below |
| CN Math 2024 | 23.33% | 30.00% | 33.33% | 33.33% | 10/30 | 14 | Below |
| Kaoyan | 56.78% | 55.78% | 59.80% | 66.83% | 133/199 | 138 | Below |
| Minerva Math | 49.63% | 46.32% | 48.90% | 47.06% | 128/272 | 95 | Met |
| OlympiadBench | 49.48% | 49.63% | 49.33% | 52.74% | 356/675 | 385 | Below |
| GPQA-Diamond | 76.77% | 81.82% | 79.29% | 70.71% | 140/198 | 121 | Met |

The integer targets implement strict exceedance of the fixed historical percentages. AIME 2024 and MATH-500 are included in the nine-target check but excluded from the assignment's seven-task average.

## Matched evaluation summary

| Completed model | Seven-task pass@1 | Seven-task pass@8 | Truncated / 15,792 |
|---|---:|---:|---:|
| Original model | 23.5497% | 49.5474% | 141 |
| Random SFT | 21.1928% | 50.6262% | 2,494 |
| Advanced route SFT (published) | 21.8526% | 51.5222% | 1,964 |
| Assistance + coverage (best measured) | 22.9398% | 52.4773% | 2,324 |

The seven-task average is the unweighted mean of AIME 2025, CN Math 2024, Kaoyan, AMC, Minerva Math, OlympiadBench and GPQA. It is not the mean of all nine or a question-weighted total.

## What the comparisons support

- **Advanced versus random:** 51.5222% versus 50.6262% average pass@8, a **+0.8960 percentage-point** descriptive difference. Both use full-parameter SFT, 15,000 examples, 4,096-token context, 1,875 updates, effective batch eight, learning rate 2e-6, cosine schedule, 3% warmup and seed 42. Data selection and resulting token exposure differ. One seed does not establish a robust causal benefit.
- **Best versus random:** 52.4773% versus 50.6262%, **+1.8510 points**. Best versus original: **+2.9298 points**. The best model also changes context to 16,384, learning rate to 5e-6, warmup to zero and training to three epochs / 5,625 updates. These differences prevent attributing its gain solely to selection.
- **Tradeoffs:** the best model regresses from the original on AMC, AIME 2024, Minerva and GPQA. Its average pass@1 is below the original, and it has 2,324 truncated responses versus 141 for the original. Meeting historical Minerva/GPQA targets does not imply beating our matched base on those tasks.
- **Uncertainty:** these are observed single-seed results from exploratory model development. Earlier advanced-versus-base paired intervals are retained in `results/comparison.json`; they do not apply to the best model or to the random comparison. No uncomputed confidence interval or statistical-significance claim is attached to the new comparisons.

## Evidence and scope

[summary.json](results/rubric-comparison/summary.json) stores all four score sets and the integer target check. [correctness.json.gz](results/rubric-comparison/correctness.json.gz) contains 7,896 matched question records and 63,168 Boolean correctness flags, plus finish reasons. [protocol.json](results/rubric-comparison/protocol.json) records the shared sampling settings, software versions and B200 hardware. Public row IDs are positional aliases for the original matched order; original IDs and full audit evidence stay private. Generated reasoning, answers and restricted benchmark text are not included.

Run `python3 scripts/verify_submission.py` to recompute all four suites, aggregates, truncation counts and the 3/9 count without a GPU. This checks packaged outcomes; it does not rerun inference, regrade raw generations or prove model-weight identity.

The existing Hugging Face model is the **51.5222% advanced route model**, not the 52.4773% best model. Best-model weights and its distinct assistance-selected dataset are not published in the current artifact release. Ongoing exploration has no score in this snapshot.
