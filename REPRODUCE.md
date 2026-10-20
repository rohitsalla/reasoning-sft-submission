# Reproduction and artifact verification

The exact evaluated model is uploaded and verified; download it using the immutable revision in `submission_manifest.json`. The source checkpoint remains preserved at `/projects/tealab/rohit/reasoning-sft-20261011/runs/lmf-full-15000-sft` on ARC. The model and both exact 15K datasets passed upload verification. This is distinct from the new 16K experiment.

## Training

Use separate Linux/CUDA Python 3.10 environments for training and evaluation. `provenance/training/environment.txt` records the actual original training runtime; `results/full-sft/manifest.json` records the evaluator's versions and hardware. The older general `requirements-selection.txt` and `requirements-eval.txt` are retained as source history, not as an exact lock of the completed run. The `*-observed.txt` files reproduce the main observed packages; they are not a complete dependency lock.

The vendored LLaMA-Factory source is recovered from research snapshot `a271825`, before later experimental loss modifications. Its complete Python source-tree hash exactly matches the original training receipt: `05aa58cebdff9cb78fc06a5b94014dbad4f5c3d66d6de0a210bb2c4ef5a0af75`. The Git commit printed in the raw runtime environment is retained as observed metadata and is not used as an independently verified upstream trainer revision. Install the vendored project with its dependencies and the observed compatible versions in a dedicated environment. CUDA/driver compatibility remains host-specific.

```bash
python -m pip install -r requirements-train-observed.txt
python -m pip install -e ./LLaMA-Factory
python -m pip check
python scripts/download_artifacts.py
PYTHONPATH="$PWD/LLaMA-Factory/src:$PWD" python LLaMA-Factory/src/train.py configs/train.yaml
```

This is a reproduction command, not part of the automated research monitor. It needs explicit GPU resources and will start a new training run only if invoked by the reader. `configs/train.yaml` changes only host paths/output path and explicitly pins the original base revision; `provenance/lmf-full-15000-sft.yaml` is the original configuration. The original mapping and 4,096 trainer cutoff are intentionally preserved so that this remains a faithful reproduction of the measured artifact. Advanced selection cutoff was 8,192; do not describe this run as full-length 16K training.

## Evaluation

Acquire the benchmark datasets under their original terms; GPQA requires Hugging Face access approval. Gated question text is not redistributed in this repository. Place each suite at `$BENCHMARK_DIR/<name>/test.jsonl`. Compare data hashes and question IDs against `results/base/manifest.json`. AIME25 is separately sourced; its exact saved identity is bound in the manifests and must not be silently replaced with another version. No exact historical leaderboard equivalence is asserted.

Install the observed evaluator environment separately. With a downloaded local checkpoint:

```bash
python -m reasoning.evaluate --model models/full-sft \
  --data-dir "$BENCHMARK_DIR" \
  --benchmarks amc aime25 aime math cn_math_2024 kaoyan minerva olympiadbench gpqa \
  --output runs/reproduced-evaluation --batch-size 1024 --max-num-seqs 128 \
  --max-new-tokens 32768 --record-hardware --gpu-memory-utilization .85
```

The evaluator fixes eight samples, temperature .6 and top-p .95 with deterministic question seeds, and uses the unchanged assignment grading code. A new runtime/hardware/dataset produces a new manifest and may not be comparable to the recorded run. To audit the existing measured result, run `python3 scripts/verify_submission.py`; no GPU or new benchmark run is needed.

## Artifacts and licensing

The Qwen base model retains its upstream license and AceReason source data retains upstream terms. This submission does not grant a new license to either. Vendored LLaMA-Factory includes its upstream LICENSE. Raw generated text and optimizer state remain in the original research workspace/ARC; this repository includes original metrics/manifests/CI comparisons and compact per-question correctness arrays sufficient to recompute the reported pass rates. Hashes bind original weight shards to the evaluated model. No authentication tokens or user credentials are included.
