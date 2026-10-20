# Submission report: full-parameter reasoning SFT

## Objective and model

Fine-tune Qwen2.5-3B-Instruct on 15,000 selected AceReason examples and compare it to the same pinned base under a matched internal evaluator. Base revision: `aa8e72537993ba99e69dfaafa59ed015b17504d1`. The selected completed model is `runs/lmf-full-15000-sft`; training finished all 1,875 optimizer updates with finite logs. It is separate from the later full-length 16K/three-epoch experiment.

## Data selection

The pipeline normalizes and deduplicates prompts, excludes benchmark overlaps, reserves validation data before selection, and computes source-text features. The final advanced export uses the frozen `route` strategy at selection cutoff 8,192: lexical reasoning-route signatures, clustering, quality/complete-answer and repetition filters, and square-root quotas for diversity. This is a heuristic adaptation, not proof of reasoning quality. Random selection uses the same prepared candidate pool, size 15,000 and seed 42. Exact selected IDs, quotas and arguments are in `artifacts/datasets-final-8k/selection_manifest.json`; both exact exports have been uploaded and verified in the private Hugging Face dataset repository. Immutable revisions are pinned in submission_manifest.json.

The advanced JSON SHA-256 is `dfd90ba66bf97bfe649befcb7edf009e5a539296790a22e0b12c19336d19d10a`. **Selection cutoff 8,192 differs from the actual trainer cutoff 4,096.** Long selected targets can therefore be truncated during this completed run. The saved original dataset mapping also omitted an explicit system-column mapping; the later full-length experiment corrects that loader issue, but no accuracy effect is established. The submission preserves the actual earlier configuration and does not relabel it as the assignment's longer reference recipe.

## Training hyperparameters

Full parameters; plain response-only cross-entropy; Qwen template; SDPA attention; cutoff 4,096; 15,000 samples; 1,875 updates; one B200; per-device batch 1; accumulation 8 (effective batch 8); learning rate 2e-6; cosine schedule; warmup ratio 0.03; weight decay 0.01; maximum gradient norm 1; BF16 mixed precision; gradient checkpointing; seed/data seed 42; no packing and no prompt loss. The exact saved configuration and actual software environment are in `provenance/`.

## Evaluation

All nine suites: AIME24, AIME25, MATH, CN Math 2024, Kaoyan, AMC, Minerva, OlympiadBench and GPQA. 1,974 questions, eight samples/question (15,792 samples). Temperature 0.6, top-p 0.95, maximum new tokens 32,768, total context 32,768, seed 0 with stable per-question seeds, batch 1,024, maximum active sequences 128, tensor parallelism 1, GPU memory utilization 0.85 on one B200. The assignment grader is retained unchanged. Base and candidate use matching protocol and question manifests. Prompt tokens count toward total context, so some responses stop before the new-token maximum.

## Findings and limitations

See [RESULTS.md](RESULTS.md) for the complete benchmark table. Seven-task average pass@8 increases from 49.55% to 51.52%. The +1.97 percentage-point difference has a paired 95% confidence interval of −1.89 to +5.74 points, so the observed average improvement is not statistically conclusive.

Average pass@1 decreases from 23.55% to 21.85%. Truncated responses increase from 141 to 1,964 out of 15,792 samples. These results show mixed performance across benchmarks and a substantial increase in response truncation.

The random dataset is provided alongside the advanced dataset. A matched completed full-parameter random-data evaluation is not available, so these experiments do not isolate the effect of advanced selection relative to random-data training. The submitted artifact is the completed ordinary full-SFT model described above.
