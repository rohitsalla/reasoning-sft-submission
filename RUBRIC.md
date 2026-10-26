# Project 1 grading evidence

Snapshot: October 26, 2026. The points below are the instructor’s weights, **not self-awarded grades**. Best fully measured performance is **3/9** fixed targets. Official LiveBenchmark placement and the top-five bonus are not claimed.

## Environment setup and reproducibility (10 points available)

| Subcriterion | Points | Evidence | Status / limit |
|---|---:|---|---|
| GitHub code, configurations and scripts | 4 | [Code](reasoning/), [configs](configs/), [scripts](scripts/), [vendored trainer](LLaMA-Factory/) | Included |
| README installation, training and evaluation instructions | 3 | [README](README.md), [reproduction commands](REPRODUCE.md) | Included |
| Dependencies, commands and seeds | 3 | [Training versions](requirements-train-observed.txt), [evaluation versions](requirements-eval-observed.txt), [protocol](results/rubric-comparison/protocol.json); train/data seed 42, eval seed 0 | Included; observed versions are not complete lockfiles |

## Dataset preparation (15 points available)

| Subcriterion | Points | Evidence | Status / limit |
|---|---:|---|---|
| Random subset sampled from AceReason | 5 | [Preparation](reasoning/prepare.py), [sampler](reasoning/select.py), [dataset method](DATA_SELECTION.md) | 15,000 examples, seed 42 |
| Advanced selection subset | 5 | [Route selector](reasoning/routes.py), [method](DATA_SELECTION.md) | 15,000 original targets |
| Both datasets published on Hugging Face | 5 | [Public random.json and advanced.json](https://huggingface.co/datasets/rohitspider/reasoning-sft-submission-data-15k/tree/course-submission-20261020-authors) | Public; the separate best-model dataset is not published |

## SFT implementation and training (20 points available)

| Subcriterion | Points | Evidence | Status / limit |
|---|---:|---|---|
| Correct LLaMA-Factory SFT configuration | 5 | [Advanced](configs/train.yaml), [random](configs/train_random.yaml), [best](configs/train_assistance.yaml) | Full-parameter response-only SFT, Qwen template, BF16 |
| Random-subset SFT training | 5 | [Random history](results/rubric-comparison/random-training.json), [config](configs/train_random.yaml) | Completed 1,875 finite updates / one epoch |
| Advanced-selection SFT training | 5 | [Advanced history](provenance/training/trainer_state.json), [best history](results/rubric-comparison/best-training.json) | Advanced completed 1,875 updates; best completed 5,625 / three epochs |
| Fine-tuned model or LoRA on Hugging Face | 5 | [Public advanced full model](https://huggingface.co/rohitspider/reasoning-sft-submission-full-15k/tree/course-submission-20261020-authors) | Published 51.5222% model; best 52.4773% weights not published |

## Model evaluation (20 points available)

| Subcriterion | Points | Evidence | Status / limit |
|---|---:|---|---|
| Original model baseline | 5 | [Baseline records](results/base/), [comparison](RESULTS.md) | All nine suites completed |
| Random-subset fine-tuned model | 5 | [Four-model correctness](results/rubric-comparison/correctness.json.gz), [scores](results/rubric-comparison/summary.json) | All nine suites completed |
| Advanced-selection fine-tuned model | 5 | [Advanced records](results/full-sft/), [best comparison](results/rubric-comparison/) | All nine completed for advanced and best |
| Consistent protocol and comparison | 5 | [Protocol](results/rubric-comparison/protocol.json), [verifier](scripts/verify_submission.py), [analysis](RESULTS.md) | Same hardware/settings/question order; differing best training recipe disclosed |

## Advanced data selection strategy (20 points available)

| Subcriterion | Points | Evidence | Status / limit |
|---|---:|---|---|
| Clear motivation and hypothesis | 5 | [Selection method](DATA_SELECTION.md#motivation-and-hypothesis) | Coverage and original-target quality hypothesis |
| Meaningful implemented strategy | 10 | [Preparation](reasoning/prepare.py), [features](reasoning/features.py), [route coverage](reasoning/routes.py), [assistance selector](reasoning/assistance_selection.py) | Filtering, clustering, square-root quotas, route diversity; assistance extension |
| Analysis against random sampling | 5 | [Results](RESULTS.md#what-the-comparisons-support), [report](REPORT.pdf) | Matched one-epoch comparison; best-model confounds and single-seed limits stated |

## Report and experimental analysis (15 points available)

| Subcriterion | Points | Evidence | Status / limit |
|---|---:|---|---|
| Setup, datasets and hyperparameters | 5 | [Report](REPORT.pdf), [summary](REPORT.md), [configs](configs/) | Four-model setup and artifact identities |
| Clear result tables or figures | 5 | [All nine results](RESULTS.md), [figures](report/figures/), [report](REPORT.pdf) | Complete scores, aggregates and fixed targets |
| Findings, limitations and improvements | 5 | [Report](REPORT.md), [selection analysis](DATA_SELECTION.md) | Regressions, truncation, uncertainty, confounds and next steps |

## Remaining submission gaps

- Best-model weights and its distinct assistance-selected training export are not on Hugging Face. The existing public model and datasets support the completed original random/advanced comparison; their links must not be labeled as the best model.
- Random-model weights are not published. Its completed training history and all nine evaluation scores are included.
- No verified official leaderboard submission/rank or top-five bonus evidence is included. The fixed nine-target check is a local historical comparison.
- This is an interim evidence snapshot. Ongoing experiments have not replaced the measured result. Course-portal submission is not performed by this repository update.

GPU constraints affected scheduling and the scope of follow-up experiments. Incomplete or timed-out experiments are excluded from the completed result table. The completed random and advanced comparison is included for the instructor's stated flexible assessment.
