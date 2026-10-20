"""Regenerate figures and compile the academic report with Tectonic."""
from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
compiler=shutil.which('tectonic')
if compiler is None:
    raise SystemExit('Install Tectonic and add it to PATH before building the report.')
subprocess.run([sys.executable,str(root/'report/make_figures.py')],check=True)
with tempfile.TemporaryDirectory(prefix='reasoning-report-') as folder:
    subprocess.run([compiler,'--outdir',folder,'report.tex'],cwd=root/'report',check=True)
    shutil.copy2(Path(folder)/'report.pdf',root/'REPORT.pdf')
print('Built REPORT.pdf')
