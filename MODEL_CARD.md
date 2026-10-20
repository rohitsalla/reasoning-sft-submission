---
library_name: transformers
base_model: Qwen/Qwen2.5-3B-Instruct
pipeline_tag: text-generation
---
# Qwen2.5-3B Reasoning SFT

Qwen2.5-3B-Instruct fine-tuned on 15,000 advanced-selected AceReason examples using full-parameter supervised fine-tuning.

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

Load with Transformers using `AutoTokenizer` and `AutoModelForCausalLM`, and apply the Qwen chat template. Authentication is required for this private repository.

[Training datasets](https://huggingface.co/datasets/rohitspider/reasoning-sft-submission-data-15k) · [Code and report](https://github.com/rohitsalla/reasoning-sft-submission)

The model can produce incorrect answers. Upstream Qwen and AceReason license terms apply.
