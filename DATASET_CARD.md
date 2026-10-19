---
task_categories:
- text-generation
language:
- en
---
# Reasoning SFT submission datasets

Two exact saved exports, `random.json` and `advanced.json`, each 15,000 records in Alpaca-style fields instruction/input/output/system. Derived from the assignment AceReason source; no new redistribution license is asserted. Original source: https://huggingface.co/datasets/redsgnaoh/acereason11_100k and upstream https://huggingface.co/datasets/nvidia/AceReason-1.1-SFT. Follow upstream terms.

Advanced: source-only quality/complete-answer/repetition filtering and lexical route diversity with fixed quotas, selection cutoff 8,192, seed 42. Random: fixed-seed random sample from the prepared pool. The completed submitted model used the advanced export, actual trainer cutoff 4,096, and the original saved loader mapping. Random is supplied for the assignment; a matched complete random full-parameter nine-suite ablation is not claimed. See selection_manifest.json for exact IDs and artifact_manifest.json for hashes.

Load with `datasets.load_dataset("json", data_files={"random":"random.json", "advanced":"advanced.json"})` after downloading this private repository. These reasoning responses are source demonstrations, not independently certified proofs.
