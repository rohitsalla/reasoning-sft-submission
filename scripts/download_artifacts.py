"""Download approved published artifacts at immutable revisions; never launch GPU work."""
from pathlib import Path
import json
from huggingface_hub import snapshot_download
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'submission_manifest.json').read_text())
if not m.get('upload_verified'):
    raise SystemExit('Hugging Face upload approval/verification is pending; see SUBMISSION_CHECKLIST.md.')
for typ,target in [('model',root/'models/full-sft'),('dataset',root/'artifacts/datasets-final-8k')]:
    snapshot_download(repo_id=m[typ+'_repository'],repo_type=typ,revision=m[typ+'_revision'],local_dir=str(target))
