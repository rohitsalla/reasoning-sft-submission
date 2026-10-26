"""Generate report figures from the recorded training and evaluation results."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'report/figures';OUT.mkdir(exist_ok=True)
base=json.loads((ROOT/'results/base/metrics.json').read_text())
sft=json.loads((ROOT/'results/full-sft/metrics.json').read_text())
comp=json.loads((ROOT/'results/comparison.json').read_text())
keys=['aime','aime25','math','cn_math_2024','kaoyan','amc','minerva','olympiadbench','gpqa']
names=['AIME24','AIME25','MATH','CN Math','Kaoyan','AMC','Minerva','Olympiad','GPQA']
BLUE='#245b89';ORANGE='#c66c32';GRAY='#6b7280'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#273142','axes.edgecolor':'#a6acb5','xtick.color':'#3b4555','ytick.color':'#3b4555','legend.frameon':False,'savefig.bbox':'tight','pdf.fonttype':42})
def save(fig,name):
 fig.savefig(OUT/(name+'.pdf'));fig.savefig(OUT/(name+'.png'),dpi=190);plt.close(fig)
x=np.arange(len(keys));w=.36
fig,ax=plt.subplots(figsize=(9.0,3.5),layout='constrained')
a=ax.bar(x-w/2,[base[k]['pass_at_8']*100 for k in keys],w,color=BLUE,label='Base model')
b=ax.bar(x+w/2,[sft[k]['pass_at_8']*100 for k in keys],w,color=ORANGE,label='Fine-tuned model')
ax.set(xticks=x,xticklabels=names,ylabel='Solved questions (%)',ylim=(0,100));ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
ax.legend(ncol=2,loc='upper left');ax.bar_label(a,fmt='%.1f',fontsize=7,padding=3);ax.bar_label(b,fmt='%.1f',fontsize=7,padding=3)
save(fig,'benchmark_pass8')
fig,axes=plt.subplots(1,2,figsize=(9.0,3.5),sharey=True,layout='constrained')
for ax,metric,title,col in zip(axes,['pass_at_8','pass_at_1'],['Pass@8','Pass@1'],[ORANGE,BLUE]):
 vals=np.array([comp[k][metric]['delta']*100 for k in keys]);interval=np.array([comp[k][metric]['ci95'] for k in keys])*100
 ax.errorbar(vals,np.arange(len(keys)),xerr=[vals-interval[:,0],interval[:,1]-vals],fmt='o',color=col,ecolor=col,capsize=3,markersize=4)
 ax.axvline(0,color=GRAY,lw=1,ls='--');ax.set(title=title,xlabel='Fine-tuned minus base (percentage points)');ax.grid(axis='x',alpha=.15)
axes[0].set(yticks=np.arange(len(keys)),yticklabels=names);axes[0].invert_yaxis()
save(fig,'paired_intervals')
state=json.loads((ROOT/'provenance/training/trainer_state.json').read_text())
rows=[r for r in state['log_history'] if 'loss' in r and 'learning_rate' in r]
steps=np.array([r['step'] for r in rows]);loss=np.array([r['loss'] for r in rows]);lr=np.array([r['learning_rate'] for r in rows])
assert len(rows)==1875 and np.isfinite(loss).all()
fig,axes=plt.subplots(1,2,figsize=(9.0,3.0),layout='constrained')
axes[0].plot(steps,loss,color='#b6bfca',lw=.45,alpha=.65,label='Per-update loss')
window=50;avg=np.convolve(loss,np.ones(window)/window,mode='valid')
axes[0].plot(steps[window-1:],avg,color=BLUE,lw=1.7,label='50-update moving average')
axes[0].set(xlabel='Optimizer update',ylabel='Response cross-entropy');axes[0].legend(fontsize=8)
axes[1].plot(steps,lr*1e6,color=ORANGE,lw=1.6);axes[1].set(xlabel='Optimizer update',ylabel='Learning rate (x 10$^{-6}$)')
for ax in axes:ax.grid(alpha=.15);ax.set_xlim(1,1875)
save(fig,'training_dynamics')
fig,axes=plt.subplots(1,2,figsize=(9.0,3.2),layout='constrained',gridspec_kw={'width_ratios':[1.7,1]})
for shift,d,col,name in [(-w/2,base,BLUE,'Base'),(w/2,sft,ORANGE,'Fine-tuned')]:
 rate=[d[k]['truncated_samples']/(d[k]['problems']*8)*100 for k in keys]
 axes[0].bar(x+shift,rate,w,color=col,label=name)
axes[0].set(xticks=x,xticklabels=names,ylabel='Truncated samples (%)',ylim=(0,55));axes[0].tick_params(axis='x',labelrotation=40);axes[0].legend(ncol=2,fontsize=8)
macro=comp['matched_seven_benchmark_macro'];xx=np.arange(2)
for shift,model,col,name in [(-w/2,'baseline',BLUE,'Base'),(w/2,'candidate',ORANGE,'Fine-tuned')]:
 bars=axes[1].bar(xx+shift,[macro[k][model]*100 for k in ['pass_at_1','pass_at_8']],w,color=col,label=name)
 axes[1].bar_label(bars,fmt='%.2f',fontsize=8,padding=3)
axes[1].set(xticks=xx,xticklabels=['Pass@1','Pass@8'],ylabel='Seven-benchmark average (%)',ylim=(0,62))
for ax in axes:ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
save(fig,'generation_tradeoffs')
summary={'questions':sum(base[k]['problems'] for k in keys),'samples_per_model':sum(base[k]['problems']*8 for k in keys),'base_truncated':sum(base[k]['truncated_samples'] for k in keys),'sft_truncated':sum(sft[k]['truncated_samples'] for k in keys),'training_updates':len(rows),'final_logged_loss':float(loss[-1]),'reported_train_loss':state['log_history'][-1]['train_loss'],'train_runtime_seconds':state['log_history'][-1]['train_runtime']}
(OUT/'figure_data.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
