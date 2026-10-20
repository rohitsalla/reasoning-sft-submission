# Reasoning SFT — submission snapshot

This is the **ordinary full-parameter 15,000-example SFT model** selected by the author for the final assignment submission. It is a completed, evaluated checkpoint, separate from the later 16K/three-epoch experiments.

**Measured outcome:** seven-task pass@8 **51.52%** versus matched base **49.55%**; improves over base on **4/9** benchmarks and clears **2/9** frozen historical gates. It has not achieved 9/9. See [results](RESULTS.md) and [report](REPORT.md).

- Model: https://huggingface.co/rohitspider/reasoning-sft-submission-full-15k
- Random and advanced datasets: https://huggingface.co/datasets/rohitspider/reasoning-sft-submission-data-15k
- Research repository: https://github.com/rohitsalla/reasoning-sft-llm-results

****Model and both dataset uploads completed and verified October 20, 2026.** Immutable revisions are recorded in `submission_manifest.json`; all uploaded model shards match the evaluated checkpoint. CPU-only verification/upload job: 1213983.** The exact source model and both datasets remain preserved on ARC.

This GitHub submission repository and the Hugging Face repositories are private. The separate research repository is public. Grant the intended graders access to this GitHub repository and both Hugging Face repositories before submitting these links. The live research run is not controlled by this submission snapshot.

**Publication status:** the GitHub submission snapshot is published in this repository. The full artifact package is published on private GitHub and Hugging Face. Course form submission and grader access remain unverified. See [submission links and handoff text](SUBMIT_THIS.md).

## Inspect and verify

```bash
python3 scripts/verify_submission.py
```

This verifies the packaged file hashes, all nine metrics from 1,974 per-question correctness vectors with eight samples each, exact matched question IDs, the pinned training-data hash, and the 4/9 versus 2/9 distinction. It uses only the Python standard library and no GPU.

## Download the model and both datasets

Create a Python environment with `huggingface_hub`, authenticate to the private repositories using `hf auth login`, then run:

```bash
python scripts/download_artifacts.py
```

The download script uses the immutable Hugging Face revisions recorded in `submission_manifest.json`. Model weights are roughly 12.35 GB and are stored on Hugging Face rather than in Git. Both dataset exports contain 15,000 records. A compressed copy of the exact advanced training export is also included in this repository.

## Reproduce

See [REPRODUCE.md](REPRODUCE.md) for the original observed environment, portable training configuration, unchanged evaluation protocol, and benchmark access requirements. `provenance/` retains the exact original training configuration, training state, environment and source receipts. `LLaMA-Factory/` is the vendored training implementation with its own license; `reasoning/` and `eval/` contain selection and evaluation code.

## Submission contents

[REPORT.md](REPORT.md) covers baseline, fine-tuned performance, comparison, hyperparameters and data selection. [MODEL_CARD.md](MODEL_CARD.md) describes the artifact and limitations. [DATASET_CARD.md](DATASET_CARD.md) describes both dataset exports. [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) lists upload verification and final access handoff. No benchmark, training or evaluation job launches merely by cloning or validating this repository.
