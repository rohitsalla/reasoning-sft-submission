# Verified ordinary full-SFT results

| Benchmark | Base pass@8 | Full SFT pass@1 | Full SFT pass@8 | Solves | Gate | Cleared |
|---|---:|---:|---:|---:|---:|:---:|
| aime | 23.33% | 4.58% | 16.67% | 5/30 | 8 | No |
| aime25 | 13.33% | 3.33% | 20.00% | 6/30 | 8 | No |
| math | 85.20% | 64.00% | 85.00% | 425/500 | 451 | No |
| cn_math_2024 | 23.33% | 7.92% | 33.33% | 10/30 | 14 | No |
| kaoyan | 56.78% | 21.23% | 59.80% | 119/199 | 138 | No |
| amc | 77.50% | 37.50% | 70.00% | 28/40 | 33 | No |
| minerva | 49.63% | 27.30% | 48.90% | 133/272 | 95 | Yes |
| olympiadbench | 49.48% | 26.33% | 49.33% | 333/675 | 385 | No |
| gpqa | 76.77% | 29.36% | 79.29% | 157/198 | 121 | Yes |

Seven-task macro: base **49.55%**, full SFT **51.52%** pass@8; full SFT **21.85%** pass@1 versus base **23.55%**.

Improves over the matched base on **4/9** benchmarks (AIME25, CN Math, Kaoyan, GPQA); clears **2/9** frozen historical gates (Minerva, GPQA). These are different comparisons. No 9/9 claim is made.

The +1.97-point pass@8 macro gain has paired 95% CI [-1.89,+5.74] percentage points. Pass@1 declines by 1.70 points, CI [-3.16,-0.22]. Full SFT produces 1,964/15,792 truncated samples, versus 141/15,792 for base. Intervals are per benchmark and not multiplicity-adjusted. Historical dataset/runtime equivalence is unverified.

Exact metrics, sampling and artifact manifests, paired comparisons, and per-question eight-sample correctness vectors are in `results/`. Raw generation text remains preserved in the research workspace/ARC and is not duplicated here.
