# Benchmark Results

| Benchmark | Base pass@8 | Fine-tuned pass@1 | Fine-tuned pass@8 | Solved questions |
|---|---:|---:|---:|---:|
| AIME 2024 | 23.33% | 4.58% | 16.67% | 5/30 |
| AIME 2025 | 13.33% | 3.33% | 20.00% | 6/30 |
| MATH-500 | 85.20% | 64.00% | 85.00% | 425/500 |
| CN Math 2024 | 23.33% | 7.92% | 33.33% | 10/30 |
| Kaoyan | 56.78% | 21.23% | 59.80% | 119/199 |
| AMC | 77.50% | 37.50% | 70.00% | 28/40 |
| Minerva Math | 49.63% | 27.30% | 48.90% | 133/272 |
| OlympiadBench | 49.48% | 26.33% | 49.33% | 333/675 |
| GPQA-Diamond | 76.77% | 29.36% | 79.29% | 157/198 |

The assignment's seven-benchmark average pass@8 is **49.55%** for the base model and **51.52%** for the fine-tuned model. Average pass@1 is **23.55%** and **21.85%**, respectively.

The pass@8 difference is +1.97 percentage points, with a paired 95% confidence interval of −1.89 to +5.74 points. The pass@1 difference is −1.70 points, with an interval of −3.16 to −0.22 points. Truncated responses total 1,964 of 15,792 samples for the fine-tuned model, compared with 141 for the base model.

The average covers AIME 2025, CN Math 2024, Kaoyan, AMC, Minerva Math, OlympiadBench and GPQA. Evaluation metrics, per-question correctness records and paired comparisons are in [results/](results/). See [REPORT.md](REPORT.md) for the method and analysis.
