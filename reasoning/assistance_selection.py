"""Assistance-associated utility plus coverage selector from the completed best run.

CPU-only reference. Inputs must already have passed the original source/model/
prefix/provenance audit. This module does not generate demonstrations or launch
training. Full original targets are selected unchanged. Saved scoring records and
the exact assistance dataset are not included in the current public release.
"""
from collections import defaultdict
import hashlib
from .select import allocate, eligible
CUTOFF = 16384
SEED_TAG = 'assist-cover-42'

def text_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()


def utility(records):
    """Exactly two supported normally-finished requests per condition; else None."""
    if len(records) != 4:
        return None
    indexed = {(r.get('condition'), r.get('sample')): r for r in records}
    if set(indexed) != {(c, s) for c in ('normal', 'assisted') for s in range(2)}:
        return None
    if any(r.get('finish_reason') != 'stop' or r.get('supported') is not True
           or type(r.get('correct')) is not bool for r in records):
        return None
    normal = (sum(indexed['normal', s]['correct'] for s in range(2)) + 1) / 4
    assisted = (sum(indexed['assisted', s]['correct'] for s in range(2)) + 1) / 4
    return (1 - normal) * max(assisted - normal, 0)


def select(features, scores, size=15000):
    """Existing capped sqrt cluster/quartile allocations, at most half utility."""
    if len({f['id'] for f in features}) != len(features):
        raise ValueError('duplicate feature identity')
    groups = defaultdict(list)
    for f in features:
        if eligible(f, CUTOFF):
            groups[f['cluster']].append(f)
    # Feasibility before ranking; this inherits Candidate A's frozen allocation.
    quotas = allocate({k: len(v) for k, v in groups.items()}, size)
    result, receipts = [], []
    for cluster in sorted(groups):
        ordered = sorted(groups[cluster], key=lambda f: (f['response_tokens'], f['id']))
        cells = defaultdict(list)
        for i, f in enumerate(ordered):
            cells[min(3, 4 * i // len(ordered))].append(f)
        cq = allocate({k: len(v) for k, v in cells.items()}, quotas[cluster]) if quotas[cluster] else {k: 0 for k in cells}
        for quartile in sorted(cells):
            cell, q = cells[quartile], cq[quartile]
            ranked = sorted((f for f in cell if scores.get(f['id'], 0) > 0),
                            key=lambda f: (-scores[f['id']], f['id']))
            chosen = ranked[:q // 2]
            ids = {f['id'] for f in chosen}
            remaining = sorted((f for f in cell if f['id'] not in ids),
                               key=lambda f: (text_hash(SEED_TAG + ':' + f['id']), f['id']))
            selected = [(f, 'utility') for f in chosen] + [(f, 'coverage') for f in remaining[:q - len(chosen)]]
            result.extend({**f, 'length_quartile': quartile, 'selection_basis': basis,
                           'assistance_utility': scores.get(f['id'])} for f, basis in selected)
            receipts.append({'cluster': cluster, 'length_quartile': quartile, 'capacity': len(cell),
                             'quota': q, 'positive_scored_available': len(ranked),
                             'selected_by_utility': len(chosen), 'selected_by_coverage': q - len(chosen)})
    result.sort(key=lambda f: (text_hash(SEED_TAG + ':' + f['id']), f['id']))
    if len(result) != size or len({f['id'] for f in result}) != size:
        raise ValueError('selection size/uniqueness failure')
    return result, receipts
