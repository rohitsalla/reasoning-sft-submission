"""Download the model and datasets for the project."""
from pathlib import Path
import json
from huggingface_hub import snapshot_download
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'submission_manifest.json').read_text())
for typ,target in [('model',root/'models/full-sft'),('dataset',root/'artifacts/datasets-final-8k')]:
    snapshot_download(repo_id=m[typ+'_repository'],repo_type=typ,revision=m[typ+'_revision'],local_dir=str(target))
