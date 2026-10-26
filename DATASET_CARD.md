---
task_categories:
- text-generation
language:
- en
---
# Reasoning SFT Datasets

Two 15,000-example datasets derived from [AceReason-100K](https://huggingface.co/datasets/redsgnaoh/acereason11_100k):

| File | Selection |
|---|---|
| `random.json` | Random sampling with seed 42 |
| `advanced.json` | Quality filtering and reasoning-route diversity |

Each record contains `instruction`, `input`, `output` and `system` fields. The published advanced model was trained on `advanced.json`. A matching one-epoch full-parameter random model has also completed all nine benchmarks; see [the four-model results](RESULTS.md). The best assistance-and-coverage model uses a separate dataset that is not part of this public dataset release.

## Load

```python
from datasets import load_dataset

data = load_dataset(
    "json",
    data_files={"random": "random.json", "advanced": "advanced.json"},
)
```

Download the JSON files first, or use their local paths. The datasets are publicly downloadable.

[Trained model](https://huggingface.co/rohitspider/reasoning-sft-submission-full-15k) · [Academic report (PDF)](https://github.com/rohitsalla/reasoning-sft-submission/blob/main/REPORT.pdf) · [Code and report](https://github.com/rohitsalla/reasoning-sft-submission)

Upstream AceReason dataset terms apply.
