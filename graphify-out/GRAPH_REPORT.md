# Graph Report - /home/work/gemma-agent  (2026-04-19)

## Corpus Check
- 1 files · ~1,217 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 12 nodes · 14 edges · 3 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]

## God Nodes (most connected - your core abstractions)
1. `run_chain()` - 4 edges
2. `is_bad_answer()` - 3 edges
3. `run_agent()` - 3 edges
4. `chat()` - 2 edges
5. `Return True if the answer looks like a failure.` - 1 edges
6. `Try each model in MODEL_CHAIN. Return first good answer, else signal Claude fall` - 1 edges

## Surprising Connections (you probably didn't know these)
- `run_chain()` --calls--> `run_agent()`  [EXTRACTED]
  /home/work/gemma-agent/agent.py → /home/work/gemma-agent/agent.py  _Bridges community 2 → community 1_

## Communities

### Community 0 - "Community 0"
Cohesion: 0.33
Nodes (0): 

### Community 1 - "Community 1"
Cohesion: 0.5
Nodes (4): is_bad_answer(), Return True if the answer looks like a failure., Try each model in MODEL_CHAIN. Return first good answer, else signal Claude fall, run_chain()

### Community 2 - "Community 2"
Cohesion: 1.0
Nodes (2): chat(), run_agent()

## Knowledge Gaps
- **2 isolated node(s):** `Return True if the answer looks like a failure.`, `Try each model in MODEL_CHAIN. Return first good answer, else signal Claude fall`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 2`** (2 nodes): `chat()`, `run_agent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_chain()` connect `Community 1` to `Community 0`, `Community 2`?**
  _High betweenness centrality (0.200) - this node is a cross-community bridge._
- **Why does `is_bad_answer()` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.182) - this node is a cross-community bridge._
- **Why does `run_agent()` connect `Community 2` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **What connects `Return True if the answer looks like a failure.`, `Try each model in MODEL_CHAIN. Return first good answer, else signal Claude fall` to the rest of the system?**
  _2 weakly-connected nodes found - possible documentation gaps or missing edges._