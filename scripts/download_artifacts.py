"""Download the model and datasets for the project."""
from pathlib import Path
import json
from huggingface_hub import snapshot_download
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'submission_manifest.json').read_text())
for typ,target in [('model',root/'models/full-sft'),('dataset',root/'artifacts/datasets-final-8k')]:
    snapshot_download(repo_id=m[typ+'_repository'],repo_type=typ,revision=m[typ+'_revision'],local_dir=str(target))

# Register both published subsets for the training configurations.
info_path = root / 'artifacts/datasets-final-8k/dataset_info.json'
info = json.loads(info_path.read_text()) if info_path.exists() else {}
for subset in ('advanced', 'random'):
    info[subset] = {'file_name': subset + '.json'}
info_path.write_text(json.dumps(info, indent=2) + '\n')
