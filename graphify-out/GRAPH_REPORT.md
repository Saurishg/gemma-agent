# Graph Report - /home/work/gemma-agent  (2026-04-24)

## Corpus Check
- 2 files · ~4,397 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 20 nodes · 17 edges · 10 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]

## God Nodes (most connected - your core abstractions)
1. `run_chain()` - 5 edges
2. `is_bad_answer()` - 3 edges
3. `run_agent()` - 3 edges
4. `route_task()` - 3 edges
5. `chat()` - 2 edges
6. `Return True if the answer looks like a failure.` - 1 edges
7. `Use phi4 to classify the task, return the best model name.` - 1 edges
8. `Smart route: classify task first, send to best model. Fall back linearly if need` - 1 edges
9. `Return True if the answer looks like a failure.` - 0 edges
10. `Use phi4 to classify the task, return the best model name.` - 0 edges

## Surprising Connections (you probably didn't know these)
- `run_chain()` --calls--> `run_agent()`  [EXTRACTED]
  /home/work/gemma-agent/agent.py → /home/work/gemma-agent/agent.py  _Bridges community 3 → community 1_
- `run_chain()` --calls--> `route_task()`  [EXTRACTED]
  /home/work/gemma-agent/agent.py → /home/work/gemma-agent/agent.py  _Bridges community 2 → community 1_

## Communities

### Community 0 - "Community 0"
Cohesion: 0.33
Nodes (0): 

### Community 1 - "Community 1"
Cohesion: 0.5
Nodes (4): is_bad_answer(), Return True if the answer looks like a failure., Smart route: classify task first, send to best model. Fall back linearly if need, run_chain()

### Community 2 - "Community 2"
Cohesion: 1.0
Nodes (2): Use phi4 to classify the task, return the best model name., route_task()

### Community 3 - "Community 3"
Cohesion: 1.0
Nodes (2): chat(), run_agent()

### Community 4 - "Community 4"
Cohesion: 1.0
Nodes (0): 

### Community 5 - "Community 5"
Cohesion: 1.0
Nodes (1): Return True if the answer looks like a failure.

### Community 6 - "Community 6"
Cohesion: 1.0
Nodes (1): Use phi4 to classify the task, return the best model name.

### Community 7 - "Community 7"
Cohesion: 1.0
Nodes (1): Smart route: classify task first, send to best model. Fall back linearly if need

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (1): Return True if the answer looks like a failure.

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (1): Try each model in MODEL_CHAIN. Return first good answer, else signal Claude fall

## Knowledge Gaps
- **8 isolated node(s):** `Return True if the answer looks like a failure.`, `Use phi4 to classify the task, return the best model name.`, `Smart route: classify task first, send to best model. Fall back linearly if need`, `Return True if the answer looks like a failure.`, `Use phi4 to classify the task, return the best model name.` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 2`** (2 nodes): `Use phi4 to classify the task, return the best model name.`, `route_task()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 3`** (2 nodes): `chat()`, `run_agent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 4`** (1 nodes): `chat.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 5`** (1 nodes): `Return True if the answer looks like a failure.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 6`** (1 nodes): `Use phi4 to classify the task, return the best model name.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 7`** (1 nodes): `Smart route: classify task first, send to best model. Fall back linearly if need`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (1 nodes): `Return True if the answer looks like a failure.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 9`** (1 nodes): `Try each model in MODEL_CHAIN. Return first good answer, else signal Claude fall`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_chain()` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `is_bad_answer()` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `route_task()` connect `Community 2` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **What connects `Return True if the answer looks like a failure.`, `Use phi4 to classify the task, return the best model name.`, `Smart route: classify task first, send to best model. Fall back linearly if need` to the rest of the system?**
  _8 weakly-connected nodes found - possible documentation gaps or missing edges._