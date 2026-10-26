# Academic report

The current report covers original-model, random-SFT, advanced-route-SFT and best assistance-and-coverage results. It maps the submission to the instructor's rubric and distinguishes the **3/9 measured outcome** from artifact-release gaps and ongoing work.

- [Report PDF](../REPORT.pdf)
- [LaTeX source](report.tex)
- [Figures](figures/)
- [Grading evidence index](../RUBRIC.md)

## Build

Install Tectonic and add it to `PATH`, then run from the repository root:

```bash
pip install -r requirements-report.txt
python report/build_report.py
```

The build regenerates figures from the packaged evaluation metrics, correctness summaries and complete training histories. Existing base-versus-advanced figures and intervals remain available as historical evidence; the new report uses the four-model `rubric_*` figures. Building does not run training, inference or grading. Tectonic may download standard TeX resources on its first run.
