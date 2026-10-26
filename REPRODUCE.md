# Reproduction

## Download

Download the public model and both datasets:

```bash
pip install huggingface_hub
python scripts/download_artifacts.py
```

## Training

Use a Linux/CUDA environment with the vendored LLaMA-Factory implementation. The observed package versions are listed in `requirements-train-observed.txt`.

```bash
python -m pip install -r requirements-train-observed.txt
python -m pip install -e ./LLaMA-Factory
python -m pip check
PYTHONPATH="$PWD/LLaMA-Factory/src:$PWD" python LLaMA-Factory/src/train.py configs/train.yaml
```

Training uses the advanced dataset, a 4,096-token context and 1,875 optimizer updates. The original configuration is also included in `provenance/`.

## Evaluation

Use a separate environment with `requirements-eval-observed.txt`. Acquire benchmark data under the source terms; GPQA requires access permission. Place each benchmark at `$BENCHMARK_DIR/<name>/test.jsonl`.

```bash
python -m reasoning.evaluate --model models/full-sft \
  --data-dir "$BENCHMARK_DIR" \
  --benchmarks amc aime25 aime math cn_math_2024 kaoyan minerva olympiadbench gpqa \
  --output runs/reproduced-evaluation --batch-size 1024 --max-num-seqs 128 \
  --max-new-tokens 32768 --record-hardware --gpu-memory-utilization .85
```

Evaluation uses eight samples per question, temperature 0.6 and top-p 0.95. Runtime and dataset differences may affect results.

## Check Packaged Results

```bash
python3 scripts/verify_submission.py
```

This checks dataset size, training progress and benchmark scores without a GPU. Detailed results are in [RESULTS.md](RESULTS.md).

Upstream Qwen, AceReason and LLaMA-Factory licenses apply.

## Build the Report

```bash
MPLCONFIGDIR=/tmp/reasoning-report-mpl python3 report/make_figures.py
cd report
tectonic report.tex
```

The LaTeX source uses standard article formatting. Install Matplotlib and NumPy to regenerate the figures; compile with Tectonic or a compatible LaTeX distribution. The published report is available as `REPORT.pdf`.
