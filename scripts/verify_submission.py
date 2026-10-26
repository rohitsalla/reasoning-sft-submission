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

# Updated rubric snapshot: four matched completed suites, with positional aliases.
packet=json.loads(gzip.open(root/'results/rubric-comparison/correctness.json.gz','rt').read())
summary=read(root/'results/rubric-comparison/summary.json')
protocol=read(root/'results/rubric-comparison/protocol.json')
assert packet['protocol']==protocol
assert protocol['n']==8 and protocol['seed']==0
assert protocol['temperature']==.6 and protocol['top_p']==.95
assert protocol['hardware'][0]['gpu']=='NVIDIA B200'
macro_keys=summary['macro_benchmarks']
assert len(macro_keys)==7
for label in ('base','random','advanced','best'):
    evidence=packet[label]
    assert set(evidence['rows'])==set(protocol['problem_counts'])
    assert sum(len(rows) for rows in evidence['rows'].values())==1974
    for bench,n in protocol['problem_counts'].items():
        rows=evidence['rows'][bench]
        assert len(rows)==n
        assert [r['problem_id'] for r in rows]==[f'{bench}:{i+1:04d}' for i in range(n)]
        assert all(len(r['answers_correctness'])==8 and
                   all(type(x)is bool for x in r['answers_correctness']) and
                   len(r['finish_reasons'])==8 for r in rows)
        metrics=evidence['metrics'][bench]
        assert abs(statistics.mean(sum(r['answers_correctness'])/8 for r in rows)-metrics['pass_at_1'])<1e-12
        assert abs(statistics.mean(any(r['answers_correctness']) for r in rows)-metrics['pass_at_8'])<1e-12
        assert sum(x=='length' for r in rows for x in r['finish_reasons'])==metrics['truncated_samples']
    assert evidence['metrics']==summary[label]['benchmarks']
    for metric in ('pass_at_1','pass_at_8'):
        assert abs(statistics.mean(evidence['metrics'][b][metric] for b in macro_keys)-
                   summary[label]['seven_benchmark_macro'][metric])<1e-12
    assert sum(v['truncated_samples'] for v in evidence['metrics'].values())==summary[label]['truncated_samples']
for new,old in (('base','base'),('advanced','full-sft')):
    for bench in protocol['problem_counts']:
        previous=read(root/f'results/{old}/{bench}/correctness.json')
        assert [r['answers_correctness'] for r in previous]==[r['answers_correctness'] for r in packet[new]['rows'][bench]]
for label,steps,epoch in (('random',1875,1),('best',5625,3)):
    history=read(root/f'results/rubric-comparison/{label}-training.json')
    assert history['global_step']==steps and history['epoch']==epoch
    updates=[r for r in history['log_history'] if 'loss' in r]
    assert len(updates)==steps and [r['step'] for r in updates]==list(range(1,steps+1))
    assert all(math.isfinite(float(r[k])) for r in updates for k in ('loss','grad_norm','learning_rate'))
expected={'amc':33,'aime25':8,'aime':8,'math':451,'cn_math_2024':14,'kaoyan':138,'minerva':95,'olympiadbench':385,'gpqa':121}
passed=[]
for bench,required in expected.items():
    solved=sum(any(r['answers_correctness']) for r in packet['best']['rows'][bench])
    assert summary['best_thresholds'][bench]==dict(solved=solved,required=required,met=solved>=required)
    if solved>=required:passed.append(bench)
assert set(passed)=={'aime25','minerva','gpqa'} and summary['thresholds_met']==3
manifest=read(root/'submission_manifest.json')
assert manifest['best_measured']['model_weights_published'] is False
assert abs(manifest['best_measured']['seven_task_pass_at_8']-summary['best']['seven_benchmark_macro']['pass_at_8'])<1e-12
print('PASS: four matched suites / 7,896 records / 63,168 samples; exact scores and truncations; finite random/best histories; 3/9 targets.')
