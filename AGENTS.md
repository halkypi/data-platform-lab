# AGENTS.md

## Purpose

This repository is a learning lab for understanding a modern data platform by building the smallest possible local, inspectable vertical slice.

The learner reviews every meaningful Git commit in Magit before continuing. Git history is part of the curriculum.

Read `docs/learning-governance.md` before planning or implementing learning work. It defines the human gate, metrics, critical-collaboration rules, documentation responsibilities, and learning constraints.

Before meaningful repository writes, summarize the proposed purpose, files affected, important decisions, and expected complexity. Ask when consequential requirements are ambiguous. Do not assume the learner's proposed approach is correct; challenge unsupported assumptions or unnecessary complexity. Wait for approval unless review is explicitly waived.

## Core Rule

Optimize for understanding per line of code and configuration.

Prefer one observable concept per commit. Keep each diff small enough to read comfortably before proceeding.

Default implementation diff target: no more than 100 meaningful added lines of executable code or hand-written configuration per learning commit.

The implementation diff budget does **not** apply to prompts, research findings, documentation/notes, data fixtures, lock files, generated files, exported NiFi definitions, or machine-generated metadata. These should still be kept purposeful and readable, and generated material must be reported separately rather than used to hide complexity.

If an implementation change needs substantially more than 100 meaningful lines, split it or explain why the extra complexity is necessary to teach the concept.

## Build Style

Build breadth before depth. Extend one tiny end-to-end path gradually rather than deeply implementing one technology in isolation.

Use a tiny stable dataset, preferably 3-10 records, with `TX001` as the canonical record to trace through the system.

At every stage, be able to answer:

- Where is `TX001`?
- What physical representation is it in?
- What component owns that representation?
- What metadata describes it?
- How can the learner inspect it directly?
- What operation moves or changes it?
- What happens when that operation fails?

## Grounding

Do not invent behavior for third-party technologies.

Use authoritative upstream documentation, specifications, or official reference implementations. Distinguish documented facts from local design choices.

Preferred authorities include Apache NiFi, Apache Iceberg, DuckDB, dbt, FastAPI, Pydantic, Lakekeeper, and the official implementation/specification of any sharing protocol introduced later. Use Snowflake documentation only when mapping Apache NiFi concepts to Openflow.

If an integration lacks authoritative support, stop and say so rather than fabricating a plausible implementation.

## Initial Technology Hypothesis

Treat this as a hypothesis to validate, not a mandate:

- source/serving API: FastAPI
- application contracts: Pydantic
- local data movement: Apache NiFi
- Openflow mapping: conceptual only
- file format: Parquet
- object storage: MinIO
- open table format: Apache Iceberg
- catalog: Iceberg REST Catalog, likely Lakekeeper
- local query engine: DuckDB
- transformation/testing: dbt + dbt-duckdb
- sharing: defer until the vertical slice is understood

Do not add Kafka, Airflow, Spark, Kubernetes, Terraform, cloud infrastructure, a frontend, or dedicated observability/data-quality platforms unless a later learning objective demonstrates why they are needed.

## Inspectability

Every stage must expose a short inspection path using ordinary tools where possible, such as:

- `curl`
- `jq`
- `cat`
- `find`
- `ls`
- `duckdb`
- `docker ps`
- `docker logs`
- `git diff`

Prefer real, inspectable artifacts such as HTTP payloads, NiFi FlowFiles and queues, provenance events, Parquet files, object keys, Iceberg metadata JSON, manifests, snapshots, catalog HTTP calls, DuckDB objects, compiled dbt SQL, and Pydantic validation errors.

## Implementation Discipline

Avoid unnecessary abstraction and production hardening. In particular, avoid factories, plugin frameworks, elaborate CLIs, speculative extensibility, and classes that do not directly teach the current concept.

Prefer 5 understandable lines over 50 reusable lines.

Pydantic belongs at application/data-contract boundaries, not as a generic data-processing layer.

Run Apache NiFi locally rather than emulating Openflow. When Openflow is discussed, map NiFi concepts using Snowflake's official documentation.

Do not fake Iceberg metadata. Use a real Iceberg implementation.

## Commit Discipline

Each meaningful learning increment should be its own commit with a specific message, for example:

- `lab: add minimal transaction HTTP source`
- `lab: ingest source response with nifi`
- `lab: persist valid records as parquet`
- `lab: query parquet with duckdb`
- `lab: add first dbt staging model`
- `lab: introduce iceberg catalog`

Avoid vague messages such as `setup infrastructure` or `implement data platform`.

Before each commit, report the intended concept and approximate meaningful LOC when practical.

After each implementation commit, stop and report only the stage, commit SHA/message, diff size, 1-3 commands to try, 1-3 things to inspect, the single most important thing to notice, and the proposed next increment. Do not continue until the learner explicitly approves.

## Branch and Review Workflow

Do not make learning changes directly on `main` unless the learner explicitly asks.

Use a focused branch. Keep commits unsquashed so the learner can review the teaching sequence in Magit. Do not merge or squash without explicit approval.

## Secrets and Data

Use synthetic data only. Do not commit credentials, tokens, personal data, work data, or secrets.
