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

See [RESULTS.md](RESULTS.md) for every score and gate. Observed seven-task pass@8 rises 49.55% to 51.52%, +1.97 points, paired 95% CI [-1.89,+5.74]. That interval includes no improvement. Seven-task pass@1 falls from 23.55% to 21.85%, and truncations increase from 141 to 1,964 out of 15,792. Improvements occur on four of nine benchmarks; five regress. Only Minerva and GPQA clear the frozen historical thresholds. The model has **not** achieved the author's strict all-nine goal. Historical runtime/data equivalence is unverified, so these are matched internal results, not an official leaderboard-equivalence claim.

The random dataset is provided as required, but this snapshot does not claim a matched completed nine-suite full-parameter random-data ablation. Earlier pilot/adapter experiments are not interchangeable with this final full-parameter result. The later TIES merge scored 51.59% pass@8 but also cleared 2/9; this snapshot uses ordinary SFT as explicitly requested. A future candidate must be fully trained and evaluated before replacing this artifact; partial checkpoints and lower training loss are not submission score evidence.
