# Installation and reproduction

## 1. Download the existing public artifacts

```bash
python3 -m venv .venv-download
source .venv-download/bin/activate
python -m pip install huggingface_hub
python scripts/download_artifacts.py
```

The script uses the readable release tags in [submission_manifest.json](submission_manifest.json). It downloads the **published one-epoch advanced route full model** to `models/full-sft`, and both `random.json` and `advanced.json` (15,000 examples each) into `artifacts/datasets-final-8k`. It registers both subsets in `dataset_info.json`.

The downloaded model has **51.5222%** seven-task pass@8. It is **not** the **52.4773% best assistance model**. The best model's weights and distinct assistance dataset are not in this public release. Its public configuration and selector describe the completed method but cannot reproduce its exact run without those artifacts and saved validated scoring observations. Random-model weights are also not published.

## 2. Training environments and commands

Use Linux/CUDA and the vendored LLaMA-Factory implementation. Create a separate environment from evaluation:

```bash
python3 -m venv .venv-train
source .venv-train/bin/activate
python -m pip install -r requirements-train-observed.txt
python -m pip install -e ./LLaMA-Factory
python -m pip check

# Completed advanced route recipe, reproduced from the original base:
PYTHONPATH="$PWD/LLaMA-Factory/src:$PWD" python LLaMA-Factory/src/train.py configs/train.yaml

# Completed random-subset control, same training settings:
PYTHONPATH="$PWD/LLaMA-Factory/src:$PWD" python LLaMA-Factory/src/train.py configs/train_random.yaml
```

Both recipes use full-parameter SFT, 15,000 original targets, context 4,096, 1,875 updates / one epoch, batch one × accumulation eight, LR 2e-6, cosine schedule, 3% warmup, weight decay .01, clipping 1, BF16, gradient checkpointing and train/data seed 42. Packing and prompt loss are disabled; the Qwen template is used. Their completed histories are in [provenance/training](provenance/training/) and [results/rubric-comparison/random-training.json](results/rubric-comparison/random-training.json).

[configs/train_assistance.yaml](configs/train_assistance.yaml) is the portable best-run recipe: four ranks, batch one × accumulation two per rank (effective batch eight), context 16,384, LR 5e-6, no warmup, three epochs / 5,625 updates. It requires the separate assistance-selected dataset, registered as `advanced` in its own directory. It must not be pointed at the published route subset and described as the same experiment. The best run was completed with recovery across training allocations; its complete 5,625-update history is packaged. A fresh equivalent run does not require the private recovery paths.

The dependency files record observed versions, not complete platform lockfiles. CUDA, GPU type, distributed topology, kernels, package resolution and nondeterministic operations can affect numerical results. Original immutable model/data/code identities are retained privately; no bitwise replay guarantee is made.

## 3. Data preparation and selection

The direct path to reproduce the completed random/advanced comparison is the pinned public export. To inspect or rerun preparation from a legally acquired local AceReason source, use the source-only pipeline:

```bash
python -m reasoning.prepare --input "$ACEREASON_JSON" --eval-dir "$BENCHMARK_DIR" \
  --output artifacts/prepared --val-size 1000 --seed 42
python -m reasoning.features --input artifacts/prepared/pool.json \
  --output artifacts/features.json --clusters 128 --seed 42
python -m reasoning.features --input artifacts/prepared/validation.json \
  --output artifacts/validation_features.json --clusters 128 --seed 42
python -m reasoning.select --pool artifacts/prepared/pool.json \
  --validation artifacts/prepared/validation.json --features artifacts/features.json \
  --validation-features artifacts/validation_features.json \
  --output artifacts/datasets-reselected --size 15000 --seed 42 --cutoff 8192 --strategy route
```

Input source versions, benchmark exclusions and tokenizer versions must match to recover the same data. Fresh clustering or changed inputs need not reproduce the published exports exactly. [DATA_SELECTION.md](DATA_SELECTION.md) explains filtering, quotas, hypothesis and the assistance extension. These commands prepare data; they do not launch model training.

## 4. Evaluation

Use a separate Linux/CUDA environment with [requirements-eval-observed.txt](requirements-eval-observed.txt). Obtain all benchmark files under their source terms, including the separately sourced AIME 2025 supplement and permission for GPQA. Each benchmark is at `$BENCHMARK_DIR/<name>/test.jsonl`.

```bash
python3 -m venv .venv-eval
source .venv-eval/bin/activate
python -m pip install -r requirements-eval-observed.txt

# Repeat with MODEL=Qwen/Qwen2.5-3B-Instruct, models/full-sft,
# or the output directory of the reproduced random training.
python -m reasoning.evaluate --model "$MODEL" --data-dir "$BENCHMARK_DIR" \
  --benchmarks amc aime25 aime math cn_math_2024 kaoyan minerva olympiadbench gpqa \
  --output "runs/eval-$LABEL" --batch-size 1024 --max-num-seqs 128 \
  --max-new-tokens 32768 --record-hardware --gpu-memory-utilization .85
```

The evaluator defaults are seed 0, eight answers/question, temperature .6, top-p .95, total context 32,768, tensor parallelism one, no repetition penalty and the original boxed-answer prompt/grader. [protocol.json](results/rubric-comparison/protocol.json) records all shared settings and software versions. All four reported suites use one B200. A different GPU or software stack requires a fresh matched baseline; historical scores are not hardware-equivalence evidence. Keep questions, order, sample count, token budget and grader fixed.

## 5. Verify recorded outcomes without a GPU

```bash
python3 scripts/verify_submission.py
```

The standard-library checker recomputes all four nine-benchmark score tables, seven-task means, truncations and the best model's 3/9 integer target count. It checks complete finite random/best training histories and matches the previously packaged base/advanced correctness. Public row IDs alias the verified common source order. Verification does not run inference or regrade raw model outputs; raw generations, restricted benchmark questions and private audit receipts are excluded.

## 6. Build the report

```bash
python -m pip install -r requirements-report.txt
python report/build_report.py
```

Install Tectonic and add it to `PATH` first. This rebuilds plots from recorded results and compiles [report/report.tex](report/report.tex) to [REPORT.pdf](REPORT.pdf). It does not train a model or generate benchmark responses.

Upstream Qwen, AceReason, benchmark and LLaMA-Factory license/access conditions apply.
