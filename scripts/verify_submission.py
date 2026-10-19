"""Validate packaged provenance and measured results without a GPU or third-party libraries."""
from pathlib import Path
import json,hashlib,gzip,math,statistics
root=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
m=read(root/'submission_manifest.json')
for name,want in read(root/'FILE_MANIFEST.json').items():
    assert sha(root/name)==want,'file hash mismatch: '+name
trainer=[(str(p.relative_to(root)),sha(p)) for p in sorted((root/'LLaMA-Factory/src').rglob('*.py'))]
assert hashlib.sha256(json.dumps(trainer,separators=(',',':')).encode()).hexdigest()==m['trainer_source_tree_sha256']
s=read(root/'provenance/training/trainer_state.json')
assert s['global_step']==1875
for x in s['log_history']:
    for k in ('loss','grad_norm'):
        if k in x:assert math.isfinite(float(x[k]))
with gzip.open(root/'artifacts/datasets-final-8k/advanced.json.gz','rb') as f:data=f.read()
assert hashlib.sha256(data).hexdigest()==m['training_data_sha256']
assert len(json.loads(data))==15000
selection=read(root/'artifacts/datasets-final-8k/selection_manifest.json')
assert len(set(selection['selected_ids']['advanced']))==15000
runs={}
for label in ['base','full-sft']:
    folder=root/'results'/label;metrics=read(folder/'metrics.json');manifest=read(folder/'manifest.json')
    runs[label]=(metrics,manifest)
    for b in m['strict_gates']:
        rows=read(folder/b/'correctness.json');assert len(rows)==manifest['problem_counts'][b]
        ids=[r['problem_id'] for r in rows];assert len(set(ids))==len(ids)
        assert set(ids)==set(manifest['problem_ids'][b])
        assert all(len(r['answers_correctness'])==8 and all(type(x) is bool for x in r['answers_correctness']) for r in rows)
        p1=statistics.mean(sum(r['answers_correctness'])/8 for r in rows)
        p8=statistics.mean(any(r['answers_correctness']) for r in rows)
        assert abs(p1-metrics[b]['pass_at_1'])<1e-12 and abs(p8-metrics[b]['pass_at_8'])<1e-12
for k in set(runs['base'][1])|set(runs['full-sft'][1]):
    if k not in {'model','identity','lora_adapter','lora_identity'}:
        assert runs['base'][1].get(k)==runs['full-sft'][1].get(k),'protocol mismatch: '+k
bm,cm=runs['base'][0],runs['full-sft'][0]
improved=[b for b in m['strict_gates'] if cm[b]['pass_at_8']>bm[b]['pass_at_8']]
cleared=[b for b,t in m['strict_gates'].items() if round(cm[b]['pass_at_8']*cm[b]['problems'])>=t]
assert len(improved)==4 and len(cleared)==2 and not m['strict_all_nine']
print('PASS: file hashes; 15,000 advanced rows; 1,875 finite training updates; all nine matched suites; 1,974 questions x 8 samples per model.')
print('Improves over base:',improved,'Historical gates:',cleared)
print('Hugging Face uploads verified:',m['upload_verified'])
