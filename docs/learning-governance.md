# Learning Governance

## Objective

This repository is a learning system, not a race to build a data platform.

> Maximize demonstrated understanding per minute of learner time.

Agent output is cheap; learner attention is scarce. The repository must not grow faster than the learner can inspect, understand, and approve it.

## Git Is the Control Plane

Each implementation commit should introduce roughly one observable concept:

`propose → implement → commit → inspect in Magit → run/inspect → explain → measure → proceed/reinforce/simplify/reconsider`

The learner gates progress. Do not generate subsequent implementation stages until the learner approves proceeding.

For each stage the learner should normally:

1. inspect the diff;
2. touch the running system;
3. explain the important concept in their own words;
4. approve the next step.

Prefer behavioral checks over self-reported scores: trace `TX001`, distinguish adjacent concepts, predict a failure, or explain a small modification.

## Critical Collaboration

Do not assume the learner's proposed architecture, technology, metric, or workflow is correct. For material decisions, consider a credible alternative or failure mode, identify unnecessary complexity, and challenge unsupported assumptions. Do not manufacture objections merely to appear critical.

If consequential requirements are ambiguous, ask before acting.

Before meaningful repository writes, summarize the purpose, files affected, important decisions, and expected complexity. Show drafts for substantial policies, prompts, skills, or architecture documents when useful. Wait for approval unless review is explicitly waived.

## Metrics

Metrics are first-class project artifacts, but measurement must not become the project.

Initially care about:

- learner minutes invested;
- concepts introduced;
- meaningful implementation LOC;
- demonstrated comprehension (trace/explain/debug where applicable);
- later retention;
- bootstrap context required by a new agent.

A useful heuristic is `learning ROI = demonstrated concepts learned / learner minutes invested`. Treat it as directional evidence, not a scientific score.

Each stage ends with `PROCEED`, `REINFORCE`, `SIMPLIFY`, or `RECONSIDER`. Successful implementation alone does not imply `PROCEED`.

For decision quality, record challenges raised, challenges accepted, and unsupported agreements when useful. Do not set a target challenge rate.

## Documentation and Context

Documentation exists to explain the current system and reduce context cost. Prefer that a new agent become task-ready from no more than three canonical documents. Track the number of bootstrap documents and approximate lines required; if that grows continually, consolidate rather than adding summaries.

Keep responsibilities distinct:

- **Research** — what external evidence says.
- **Docs** — how this system works.
- **Glossary** — concepts the learner needs to understand.
- **Anki** — concepts the learner wants to retain.
- **Git** — how the system and understanding evolved.
- **Metrics** — evidence about the learning process.

## Glossary and Anki

Maintain a minimal progressive glossary. Add a term only when it is needed to explain something actually built or observed. Prefer a concise definition, a `Distinguish from` comparison, and the commit where the concept became relevant.

The glossary is the source for possible Anki cards. After learning a concept, an agent may propose 0–3 cards (normally 1). Zero is valid. Prefer durable mental models and distinctions over commands or implementation trivia. The learner approves cards before they are added or exported.

Do not duplicate Anki's review statistics in Git unless experience shows that doing so improves learning decisions.

## Complexity Must Earn Its Place

This applies to learning infrastructure too. Do not add skills, hooks, CI, metrics automation, Anki integration, or documentation frameworks merely because they might be useful. Observe the manual workflow first and automate only when repeated experience shows that automation reduces learner effort or improves learning.

> Build the smallest thing that exposes the next important concept.
