#!/usr/bin/env python3
"""Recount the frozen audited Coder390 corpus without inference (standard library)."""
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = ('Claude', 'GPT/OpenAI', 'Grok', 'DeepSeek', 'Kimi', 'Qwen', 'other')


def wilson(k, n):
    """Two-sided 95% Wilson score interval; no interval for an empty denominator."""
    if n == 0:
        return None
    if not 0 <= k <= n:
        raise ValueError('Invalid binomial counts')
    z = 1.959963984540054
    p = k / n
    centre = (p + z*z/(2*n)) / (1 + z*z/n)
    half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return [max(0.0, centre-half), min(1.0, centre+half)]


def classify(row, channel, family):
    labels = list(row['channels'].values()) if channel == 'union' else [row['channels'][channel]]
    if any(c['family'] == family for label in labels for c in label.get('claims', [])):
        return 'positive'
    if any(label.get('uncertain', False) for label in labels):
        return 'uncertain'
    if any(label['status'] == 'unavailable' for label in labels):
        return 'unavailable'
    if all(label['status'] == 'empty' for label in labels):
        return 'empty'
    return 'negative'


def summarise(rows, channel, family):
    counts = Counter(classify(row, channel, family) for row in rows)
    n = len(rows)
    k = counts['positive']
    scored = k + counts['negative']
    unknown = counts['uncertain'] + counts['unavailable']
    return {'n_registered_in_subset': n,
            **{s: counts[s] for s in ('positive', 'negative', 'empty', 'unavailable', 'uncertain')},
            'scored_denominator': scored,
            'confirmed_per_registered_wilson95': None if counts['empty'] == n else wilson(k, n),
            'positive_per_scored_wilson95': wilson(k, scored),
            'missing_outcome_bounds': [k/n, (k+unknown)/n] if n else None,
            'positive_ids': [r['source']['id'] for r in rows if classify(r, channel, family) == 'positive']}


def statistics(rows):
    tables = []
    subsets = {'full': lambda s: True, 'cuda88': lambda s: s['order'] >= 12,
               'retry_missing': lambda s: not s['retry'],
               'cuda_retry_missing': lambda s: s['order'] >= 12 and not s['retry'],
               'paired_retry_missing': lambda s: s['id'] != 'portrait-0015',
               'cuda_paired_retry_missing': lambda s: s['order'] >= 12 and s['id'] != 'portrait-0015'}
    for subset, select in subsets.items():
        for model in ('base-matched', 'coder390'):
            for condition in ('identity', 'portrait'):
                selected = [r for r in rows if r['source']['model'] == model and r['source']['condition'] == condition and select(r['source'])]
                for channel in (('reasoning', 'answer', 'union') if condition == 'identity' else ('reasoning', 'answer', 'svg_source', 'pixels', 'union')):
                    for family in FAMILIES:
                        tables.append({'subset': subset, 'model': model, 'condition': condition, 'channel': channel, 'family': family, **summarise(selected, channel, family)})
    paired = []
    for subset in ('full', 'cuda88'):
        for family in FAMILIES:
            for channel in ('reasoning', 'svg_source', 'pixels', 'union'):
                by_model = {m: {r['source']['order']: r for r in rows if r['source']['model'] == m and r['source']['condition'] == 'portrait' and subsets[subset](r['source'])} for m in ('base-matched', 'coder390')}
                c = Counter()
                for order, base in by_model['base-matched'].items():
                    a, b = classify(base, channel, family), classify(by_model['coder390'][order], channel, family)
                    if a in ('unavailable', 'uncertain') or b in ('unavailable', 'uncertain'):
                        c['unknown_pair'] += 1
                    else:
                        c['both' if a == b == 'positive' else 'base_only' if a == 'positive' else 'coder_only' if b == 'positive' else 'neither'] += 1
                paired.append({'subset': subset, 'family': family, 'channel': channel, **{k:c[k] for k in ('both','base_only','coder_only','neither','unknown_pair')}})
    return {'interval_method':'95% Wilson score; pointwise, not multiplicity adjusted. Registered-denominator intervals concern confirmed recorded claims, not imputed missing outcomes. Scored-denominator intervals exclude empty/unavailable/uncertain channels. Missing-outcome bounds are identification bounds, not confidence intervals.', 'tables':tables, 'paired_portraits':paired}


def main():
    out = ROOT / 'evidence/coder390/manual-audit'
    rows = json.loads((out / 'labels.json').read_text())
    assert len(rows) == 400
    result = statistics(rows)
    (out / 'statistics.json').write_text(json.dumps(result, indent=2)+'\n')
    lines = ['# Complete audited frequency tables', '', result['interval_method'], '',
             'Empty means no prose/channel content, not a scored negative. Union is across available channels; a negative with an unavailable channel is unavailable. Truncated SVG source is scored only on its captured fragment. Direct-answer SVG/pixels are inapplicable and omitted.', '',
             '| Subset | Model | Prompt | Channel | Family | Confirmed / registered | Negative | Empty | Unavailable | Uncertain | Scored n | Wilson 95%, registered | Wilson 95%, scored |',
             '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |']
    def interval(v):
        return '—' if v is None else f'{100*v[0]:.1f}–{100*v[1]:.1f}%'
    for t in result['tables']:
        lines.append('| '+ ' | '.join([t['subset'],t['model'],t['condition'],t['channel'],t['family'],f"{t['positive']}/{t['n_registered_in_subset']}",str(t['negative']),str(t['empty']),str(t['unavailable']),str(t['uncertain']),str(t['scored_denominator']),interval(t['confirmed_per_registered_wilson95']),interval(t['positive_per_scored_wilson95'])])+' |')
    (out/'frequency-tables.md').write_text('\n'.join(lines)+'\n')


if __name__ == '__main__':
    main()
