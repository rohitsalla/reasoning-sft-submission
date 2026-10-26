---
library_name: transformers
base_model: Qwen/Qwen2.5-3B-Instruct
pipeline_tag: text-generation
---
# Qwen2.5-3B Reasoning SFT

Qwen2.5-3B-Instruct fine-tuned on 15,000 advanced-selected AceReason examples using full-parameter supervised fine-tuning.

This card identifies the **published one-epoch advanced route model**, with seven-task pass@8 **51.5222%**. The project's best measured assistance model reaches **52.4773%, 3/9 fixed targets**, but its weights are not in this release. See [artifact identities and results](RESULTS.md).

## Results

The seven-benchmark average pass@8 is **51.52%**, compared with **49.55%** for the base model. Performance improves on AIME 2025, CN Math 2024, Kaoyan and GPQA, with regressions on the remaining evaluated benchmarks.

See the [project README](https://github.com/rohitsalla/reasoning-sft-submission) for the complete comparison and the [report](https://github.com/rohitsalla/reasoning-sft-submission/blob/main/REPORT.md) for analysis and limitations.

## Training

| Parameter | Value |
|---|---|
| Training examples | 15,000 |
| Context length | 4,096 tokens |
| Learning rate | 2e-6 |
| Effective batch size | 8 |
| Optimizer updates | 1,875 |
| Seed | 42 |

## Usage

Load with Transformers using `AutoTokenizer` and `AutoModelForCausalLM`, and apply the Qwen chat template. The model is publicly downloadable.

[Training datasets](https://huggingface.co/datasets/rohitspider/reasoning-sft-submission-data-15k) · [Academic report (PDF)](https://github.com/rohitsalla/reasoning-sft-submission/blob/main/REPORT.pdf) · [Code and report](https://github.com/rohitsalla/reasoning-sft-submission)

The model can produce incorrect answers. Upstream Qwen and AceReason license terms apply.
