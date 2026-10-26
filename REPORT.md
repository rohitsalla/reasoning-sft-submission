# Data Selection and Reasoning SFT: Interim Project Report

**Rohit Kumar Salla · Manoj Saravanan · Haissam Adam** · October 26, 2026

[PDF report](REPORT.pdf) · [LaTeX source](report/report.tex) · [Rubric evidence](RUBRIC.md) · [All nine results](RESULTS.md)

## Experimental setup

We fine-tune Qwen2.5-3B-Instruct with LLaMA-Factory using original AceReason targets. The core comparison includes original-model evaluation and two completed full-parameter SFT runs: random and advanced route-selected subsets of 15,000 examples. Both use a 4,096-token context, batch one with accumulation eight, 1,875 updates / one epoch, LR 2e-6, cosine schedule, 3% warmup, weight decay .01, clipping 1, BF16, Qwen template, SDPA, gradient checkpointing and seed/data seed 42. Prompt loss and packing are disabled. The selection cutoff was 8,192, so some responses may be truncated during 4K training; the original loader did not explicitly map the system column.

Our best measured extension uses assistance-associated utility and coverage to select a different 15,000 original examples. It changes training to 16,384-token context, LR 5e-6, zero warmup and three epochs / 5,625 updates, with effective batch eight across four ranks. Training recovered across allocations and completed the full history. Its recipe and exact data differ from the one-epoch comparison, so we report it separately.

## Dataset selection

The preparation pipeline normalizes, deduplicates and excludes recognizable benchmark overlap, then reserves validation before selection. Random sampling uses seed 42. The advanced route strategy filters answer completeness and repetition, clusters prompts, applies square-root quotas and selects diverse lexical reasoning routes. The assistance extension combines supported normal-versus-prefix-assisted outcomes with cluster/length coverage, selecting 3,672 by positive utility and 11,328 by coverage. Original targets are unchanged. [DATA_SELECTION.md](DATA_SELECTION.md) explains the hypothesis, implementation, counts and limitations.

## Evaluation and results

Each of four models completed the same 1,974 records across all nine benchmarks, eight answers each: 15,792 samples/model. Generation uses one B200, seed 0, temperature .6, top-p .95, maximum new/total-context tokens 32,768, batch 1,024, maximum sequences 128, tensor parallelism one and memory utilization .85. The original prompt, extraction and grader are retained. Pass@1 is mean sample correctness; pass@8 is the fraction solved at least once. The seven-task mean excludes AIME 2024 and MATH-500.

| Model | Seven-task pass@1 | Seven-task pass@8 | Truncated responses |
|---|---:|---:|---:|
| Original | 23.5497% | 49.5474% | 141 |
| Random SFT | 21.1928% | 50.6262% | 2,494 |
| Advanced route SFT | 21.8526% | 51.5222% | 1,964 |
| Assistance + coverage | 22.9398% | 52.4773% | 2,324 |

The best single model meets **3/9 fixed historical targets**, AIME 2025 (8/30), Minerva (128/272) and GPQA (140/198). It misses AMC, AIME 2024, MATH, CN Math, Kaoyan and OlympiadBench. These local thresholds do not establish an official LiveBenchmark rank or top-five bonus.

## Findings and limitations

Advanced route selection exceeds random by 0.8960 percentage points in the seven-task pass@8 mean under matching one-epoch training settings. The best extension exceeds random by 1.8510 points and the original by 2.9298 points, but longer context, more epochs and a different learning rate confound attribution to selection. All are single-seed exploratory results; no significance claim follows from the differences. The earlier advanced-versus-original paired intervals remain available, but do not apply to the best/random comparisons.

The best model's average pass@1 remains below the original, and truncation rises from 141 to 2,324 samples. It regresses on several tasks, including Minerva and GPQA against our original even while meeting their lower historical reference thresholds. Lexical features are proxies, assistance utility is associative, prefix leakage has not been ruled out, and overlap filtering does not prove contamination absence. Lower training loss does not establish reasoning improvement.

Next work should address termination while retaining the fixed evaluation protocol, compare selection under equal context/token/update budgets and repeat training seeds. Ongoing runs are excluded until training and evaluation complete; no predicted 9/9 is reported. GPU constraints limited follow-up scope and scheduling.

## Artifact availability and reproduction

[REPRODUCE.md](REPRODUCE.md) gives environments, commands and seeds. Both original random/advanced exports and the earlier advanced full model are public on Hugging Face. The public model corresponds to 51.5222%, **not** the best extension. Best-model weights, its distinct assistance dataset and random-model weights remain unpublished. Public score vectors, finish reasons and finite training histories allow CPU recomputation of the results, not replay of missing weights or regrading of private generations. [RUBRIC.md](RUBRIC.md) records all remaining submission gaps explicitly.
