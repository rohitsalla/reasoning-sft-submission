# Assignment handoff

Selected submission: ordinary full-parameter 15K SFT, not TIES and not the later assistance recovery.

- GitHub code, report and results: https://github.com/rohitsalla/reasoning-sft-submission
- Model: https://huggingface.co/rohitspider/reasoning-sft-submission-full-15k
- Both random and advanced datasets: https://huggingface.co/datasets/rohitspider/reasoning-sft-submission-data-15k
- Report: REPORT.md in the GitHub repository (included in the downloadable package).

## Text for the course submission

We submit a full-parameter Qwen2.5-3B-Instruct model fine-tuned on 15,000 advanced-selected AceReason examples. Across the assignment's seven AVG benchmarks, pass@8 is 51.52% versus the base model's 49.55%. The linked repository contains code, the training configuration, benchmark results, analysis and the project report. The model and both selected datasets are available through the Hugging Face links above.

A matched completed full-parameter random-data nine-suite ablation is not available; the random 15K dataset is supplied. The report documents the actual 4,096 training cutoff, differing from the assignment's 16K example configuration, and all observed limitations.

## Access and final action

All three submission repositories are private. Graders must be granted access before final course handoff. Hugging Face revisions and upload verification are recorded in submission_manifest.json when complete. Do not describe this package as submitted to the course until the submission page returns a receipt.
