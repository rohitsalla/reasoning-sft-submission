"""Recompute the packaged results without a GPU."""
from pathlib import Path
import json,gzip,math,statistics
root=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
state=read(root/'provenance/training/trainer_state.json')
assert state['global_step']==1875
for record in state['log_history']:
    for key in ('loss','grad_norm'):
        if key in record:assert math.isfinite(float(record[key]))
with gzip.open(root/'artifacts/datasets-final-8k/advanced.json.gz','rt') as f:
    assert len(json.load(f))==15000
suites={}
for label in ('base','full-sft'):
    folder=root/'results'/label
    metrics=read(folder/'metrics.json');manifest=read(folder/'manifest.json')
    assert len(metrics)==9
    suites[label]=(metrics,manifest)
    for bench,values in metrics.items():
        rows=read(folder/bench/'correctness.json')
        assert len(rows)==manifest['problem_counts'][bench]
        identifiers=[r['problem_id'] for r in rows]
        assert len(set(identifiers))==len(rows)
        assert set(identifiers)==set(manifest['problem_ids'][bench])
        assert all(len(r['answers_correctness'])==8 and all(type(v) is bool for v in r['answers_correctness']) for r in rows)
        p1=statistics.mean(sum(r['answers_correctness'])/8 for r in rows)
        p8=statistics.mean(any(r['answers_correctness']) for r in rows)
        assert abs(p1-values['pass_at_1'])<1e-12
        assert abs(p8-values['pass_at_8'])<1e-12
for key in set(suites['base'][1])|set(suites['full-sft'][1]):
    if key not in ('model','lora_adapter'):
        assert suites['base'][1].get(key)==suites['full-sft'][1].get(key),key
print('PASS: 15,000 training examples; 1,875 finite training updates; matched benchmark settings; all nine scores recomputed.')
