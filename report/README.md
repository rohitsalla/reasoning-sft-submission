# Academic Report

The report uses a numbered article layout with an abstract, mathematical definitions, experimental settings, results, discussion, references and appendices.

- [PDF](../REPORT.pdf)
- [LaTeX source](report.tex)
- [Figures](figures/)

## Build

Install [Tectonic](https://tectonic-typesetting.github.io/) and the plotting dependencies, then run from the repository root:

```bash
pip install -r requirements-report.txt
python report/build_report.py
```

The plots are generated from the recorded evaluation metrics, paired intervals and training history. Building the report does not run model training or benchmark generation.
