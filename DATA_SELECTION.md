# Dataset preparation and advanced selection

## Motivation and hypothesis

A random sample can overrepresent common topics, repetitive reasoning and similar solution styles. We hypothesize that combining answer-completeness filters, topic coverage and diverse reasoning routes can improve multi-sample reasoning performance at a fixed example count. This is a hypothesis tested through the random-versus-advanced comparison, not a guarantee that lexical diversity measures valid reasoning.

## Shared preparation and random sampling

The source is [AceReason-1.1 100K](https://huggingface.co/datasets/redsgnaoh/acereason11_100k). [prepare.py](reasoning/prepare.py) normalizes instruction/input/output/system fields, removes invalid and duplicate prompts, excludes benchmark overlap using normalized exact matches and character-shingle overlap, and reserves validation data before selection. This reduces recognizable overlap; it cannot prove absence of semantic contamination or pretraining exposure.

[select.py](reasoning/select.py) samples 15,000 examples from the prepared pool using seed 42. Both `random.json` and `advanced.json` are [public on Hugging Face](https://huggingface.co/datasets/rohitspider/reasoning-sft-submission-data-15k/tree/course-submission-20261020-authors). Downloading the pinned release is the direct reproduction path for the completed one-epoch comparison.

## Published advanced route subset

[features.py](reasoning/features.py) and [routes.py](reasoning/routes.py) implement source-text selection. Advanced eligibility requires at least 128 response tokens, a complete boxed answer, repeated word-eight-gram fraction ≤0.35, and a serialized sequence fitting the 8,192-token selection limit with a 32-token reserve. Box detection and repetition checks do not certify correctness.

Topic features use character TF–IDF, SVD and MiniBatch K-means. The advanced export has 113 populated eligible clusters. Quotas allocate each next slot to the non-full cluster maximizing `sqrt(capacity) / (quota + 1)`, balancing prevalence and coverage. Within clusters, a 180-dimensional lexical route vector captures cue counts, late-response cues, cue transitions and presence across 12 reasoning cue families. Standardized, clipped, normalized vectors feed a greedy farthest-point selection with 80% diversity and 20% low-repetition quality. Seed 42 fixes the output shuffle.

The original targets are retained. Both trained arms use a 4,096-token training context even though selection allowed 8,192; longer targets may therefore be truncated. The random and advanced sets also differ in eligibility filtering and token exposure, so the experiment tests the combined selection procedure.

## Best measured extension: assistance + coverage

The best model uses a **different** 15,000-example original-target dataset. [assistance_selection.py](reasoning/assistance_selection.py) provides the original scoring and quota-selection functions in a portable CPU-only module. A saved source-only scoring study compares two normally finished, supported samples per condition: no assistance versus an original-response prefix. With Laplace smoothing, `p_normal = (normal_correct + 1)/4`, `p_assisted = (assisted_correct + 1)/4`, and utility is `(1 - p_normal) * max(p_assisted - p_normal, 0)`. Missing, censored or unsupported observations remain unscored.

The selector splits each topic cluster into response-length quartiles, applies capped square-root quotas, uses positive utility for at most half of each cell, and fills the remaining slots by a deterministic source-ID ordering. Saved selection evidence records 56,673 eligible originals, 23,014 scored prompts and 3,672 utility-selected plus 11,328 coverage-selected examples. All training targets remain the original AceReason responses; generated scoring outputs are not replacement labels. Native preprocessing recorded 105,389,717 supervised response tokens per epoch.

Assistance association is not a causal estimate of learnability. Prefix assistance can reveal useful answer information, and absence of semantic leakage was not established. The exact saved measurement ledger and this distinct assistance dataset are not in the current public artifact release. The portable selector requires provenance-validated inputs; it does not reproduce the missing scorer evidence.

## Comparison and interpretation

The matched one-epoch random and advanced route runs reach **50.6262%** and **51.5222%** seven-task pass@8 (+0.8960 percentage points). The assistance model reaches **52.4773%**, but uses 16K context, learning rate 5e-6 and three epochs instead of 4K, 2e-6 and one epoch. The extra compute and context confound selection attribution. All three are full-parameter LLaMA-Factory SFT with original targets. See [RESULTS.md](RESULTS.md) for all regressions, truncation and target checks.
