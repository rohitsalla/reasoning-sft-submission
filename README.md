# Reasoning SFT — submission snapshot

This is the **ordinary full-parameter 15,000-example SFT model** selected by the author as the submission fallback while the separate full-length experiment is pending. It is a completed, evaluated checkpoint, not the unfinished 16K/three-epoch model.

**Measured outcome:** seven-task pass@8 **51.52%** versus matched base **49.55%**; improves over base on **4/9** benchmarks and clears **2/9** frozen historical gates. It has not achieved 9/9. See [results](RESULTS.md) and [report](REPORT.md).

- Model: https://huggingface.co/rohitspider/reasoning-sft-submission-full-15k
- Random and advanced datasets: https://huggingface.co/datasets/rohitspider/reasoning-sft-submission-data-15k
- Research repository: https://github.com/rohitsalla/reasoning-sft-llm-results

**Hugging Face upload is staged but pending explicit transfer approval; the links above currently point to empty private repositories.** The exact source model and both datasets remain preserved on ARC.

Repositories are private. Grant the intended graders access to this GitHub repository and both Hugging Face repositories before submitting these links. The live research run is not controlled by this submission snapshot.

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
