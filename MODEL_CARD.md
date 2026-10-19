---
library_name: transformers
base_model: Qwen/Qwen2.5-3B-Instruct
pipeline_tag: text-generation
---
# Ordinary full-parameter 15K SFT submission checkpoint

Completed 1,875-update full-parameter SFT from base revision aa8e72537993ba99e69dfaafa59ed015b17504d1, advanced data hash dfd90ba66bf97bfe649befcb7edf009e5a539296790a22e0b12c19336d19d10a. Actual trainer cutoff 4,096; selection cutoff 8,192; LR 2e-6; effective batch 8; seed 42. This card does not change upstream model or data license terms; users must comply with the original Qwen and AceReason terms.

Matched internal nine-suite evaluation: seven-task pass@8 51.52%, pass@1 21.85%, versus base 49.55%/23.55%. Improves over base on 4/9 suites; clears 2/9 frozen historical gates. 1,964 of 15,792 generated samples truncated. No 9/9 or official historical-equivalence claim. See the GitHub submission report and bound source manifest for details.

Use `AutoTokenizer.from_pretrained` and `AutoModelForCausalLM.from_pretrained` with this repository's immutable published revision. Apply the Qwen chat template. Evaluation system prompt: “Please reason step by step, and put your final answer within \boxed{}.” This checkpoint may produce lengthy, incorrect reasoning and should not be used as an authority for high-stakes decisions.
