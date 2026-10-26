# Full-Parameter Reasoning SFT

**Rohit Kumar Salla · Manoj Saravanan · Haissam Adam**

[Read the academic report (PDF)](REPORT.pdf) · [LaTeX source](report/report.tex)

## Objective and model

This project fine-tunes Qwen2.5-3B-Instruct on 15,000 selected AceReason examples and evaluates the model against the original base model under matching settings. Training completed 1,875 optimizer updates.

## Data selection

The pipeline normalizes and deduplicates prompts, excludes benchmark overlaps, reserves validation data, and computes source-text features. Advanced selection combines lexical reasoning-route signatures, clustering, answer-completeness and repetition filters, and square-root quotas for diversity. Random selection samples 15,000 examples from the same prepared candidate pool with seed 42. Both datasets are available on Hugging Face.

Data selection uses an 8,192-token cutoff; training uses a 4,096-token context, so longer targets can be truncated. The original loader configuration does not explicitly map the system column. These details are reflected in the provided training configuration.

## Training hyperparameters

Full parameters; plain response-only cross-entropy; Qwen template; SDPA attention; cutoff 4,096; 15,000 samples; 1,875 updates; one B200; per-device batch 1; accumulation 8 (effective batch 8); learning rate 2e-6; cosine schedule; warmup ratio 0.03; weight decay 0.01; maximum gradient norm 1; BF16 mixed precision; gradient checkpointing; seed/data seed 42; no packing and no prompt loss. The training configuration is in `configs/train.yaml`; observed package versions are listed in the requirements files.

## Evaluation

All nine suites: AIME24, AIME25, MATH, CN Math 2024, Kaoyan, AMC, Minerva, OlympiadBench and GPQA. 1,974 questions, eight samples/question (15,792 samples). Temperature 0.6, top-p 0.95, maximum new tokens 32,768, total context 32,768, seed 0 with stable per-question seeds, batch 1,024, maximum active sequences 128, tensor parallelism 1, GPU memory utilization 0.85 on one B200. The assignment grader is retained unchanged. Base and candidate use matching protocol and question manifests. Prompt tokens count toward total context, so some responses stop before the new-token maximum.

## Findings and limitations

See [RESULTS.md](RESULTS.md) for the complete benchmark table. Seven-task average pass@8 increases from 49.55% to 51.52%. The +1.97 percentage-point difference has a paired 95% confidence interval of −1.89 to +5.74 points, so the observed average improvement is not statistically conclusive.

Average pass@1 decreases from 23.55% to 21.85%. Truncated responses increase from 141 to 1,964 out of 15,792 samples. These results show mixed performance across benchmarks and a substantial increase in response truncation.

The random dataset is provided alongside the advanced dataset. A matched completed full-parameter random-data evaluation is not available, so these experiments do not isolate the effect of advanced selection relative to random-data training.
