#!/usr/bin/env python3
"""Query prompts.chat database."""
import csv
import sys
import json

PROMPTS_FILE = "/root/.pi/prompts-lib/prompts.csv"

def load_prompts():
    with open(PROMPTS_FILE, 'r') as f:
        return list(csv.DictReader(f))

def search(query, limit=10):
    prompts = load_prompts()
    q = query.lower()
    results = []
    for p in prompts:
        act = p.get('act', '').lower()
        prompt_text = p.get('prompt', '').lower()
        if q in act or q in prompt_text:
            results.append({
                'act': p['act'],
                'prompt': p['prompt'][:500],
                'for_devs': p.get('for_devs', ''),
                'type': p.get('type', ''),
                'contributor': p.get('contributor', '')
            })
            if len(results) >= limit:
                break
    return results

def list_categories(limit=50):
    prompts = load_prompts()
    acts = sorted(set(p['act'] for p in prompts if p.get('act')))
    return acts[:limit]

def get_prompt(act_name):
    prompts = load_prompts()
    for p in prompts:
        if p.get('act', '').lower() == act_name.lower():
            return {
                'act': p['act'],
                'prompt': p['prompt'],
                'for_devs': p.get('for_devs', ''),
                'type': p.get('type', '')
            }
    return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: query.py <search|list|get> [query]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == 'search' and len(sys.argv) > 2:
        results = search(' '.join(sys.argv[2:]))
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif cmd == 'list':
        cats = list_categories(int(sys.argv[2]) if len(sys.argv) > 2 else 50)
        for c in cats:
            print(c)
    elif cmd == 'get' and len(sys.argv) > 2:
        result = get_prompt(' '.join(sys.argv[2:]))
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Usage: query.py <search|list|get> [query]")
