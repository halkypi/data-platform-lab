# Deep Research: Minimal Local Data Platform Learning Lab

## Objective

Research and validate the architecture for a **minimal, completely local, inspectable modern data-platform learning lab**.

This is research and technology selection, **not implementation**.

A later orchestrator will use these findings to construct the lab incrementally. Each Git commit will introduce approximately one architectural concept, and I will inspect every commit before proceeding.

The goal is to understand how modern data systems actually work **under the hood**, rather than learning vendor terminology or assembling a production-grade stack.

## Core Learning Question

What is the **smallest set of real technologies and reference implementations** that lets me follow a tiny dataset end-to-end and understand:

```text
produce
  ↓
serialize
  ↓
transport / ingest
  ↓
validate
  ↓
queue / retry / route
  ↓
physically store
  ↓
organize files into tables
  ↓
catalog / discover
  ↓
query / compute
  ↓
transform / test
  ↓
serve through an API
  ↓
share with another consumer
```

Everything should run locally where practical.

I want to be able to inspect the actual:

- HTTP requests and responses
- JSON
- queues
- processing/provenance events
- Parquet files
- object-storage keys
- Iceberg metadata
- snapshots
- manifests
- catalog REST calls
- SQL
- database objects
- dbt models/tests
- Python objects
- API contracts and responses

The lab should favor **transparent implementations over managed abstractions**.

## Current Hypothesis

The current candidate architecture is:

| Responsibility | Candidate |
|---|---|
| source application/API | FastAPI |
| application contracts | Pydantic |
| transport | HTTP/JSON |
| ingestion/data movement | Apache NiFi |
| managed-enterprise analogue | Snowflake Openflow |
| physical analytical format | Parquet |
| local object storage | MinIO |
| open table format | Apache Iceberg |
| catalog protocol | Iceberg REST Catalog |
| local catalog implementation | Lakekeeper |
| local analytical compute | DuckDB |
| transformation/testing | dbt + dbt-duckdb |
| serving layer | FastAPI + Pydantic |
| open data sharing | possibly Delta Sharing |

**Do not assume this architecture is correct.**

Challenge it.

Identify technologies that are unnecessary, overlap, obscure rather than illuminate the underlying concept, introduce disproportionate operational complexity, have better alternatives, or should be postponed.

Also identify important architectural concepts that this list misses.

## Real-World Motivation

One practical motivation is understanding how legacy Pentaho ingestion/transformation workloads can be decomposed into modern architectural responsibilities.

I want to understand distinctions such as:

```text
ingestion ≠ transformation
storage ≠ compute
files ≠ tables
table format ≠ catalog
schema validation ≠ data quality testing
API serving ≠ data sharing
orchestration ≠ data movement
```

The research should correct any of these distinctions if they are misleading.

Apache NiFi is being considered partly because Snowflake Openflow is based on NiFi. Determine whether learning local NiFi is genuinely a useful way to understand Openflow's underlying model.

Do not turn this into a Snowflake tutorial.

## Learning Philosophy

Optimize for **understanding per line of code/configuration** rather than **number of technologies demonstrated**.

The eventual repository should be extremely small.

A tiny dataset of perhaps 3–10 transaction records is sufficient.

One stable record such as `TX001` should be traceable through the entire ecosystem.

The learner should repeatedly be able to answer:

```text
Where is TX001?
What representation is it currently in?
Who owns that representation?
What metadata describes it?
How can I inspect it directly?
What causes it to move/change?
What happens if that operation fails?
```

## Git as the Teaching Mechanism

The eventual implementation will use Git commits as lessons.

The desired pattern is:

```text
commit 1 → introduce one observable concept
review in Magit
understand it
continue

commit 2 → introduce next concept
review
understand it
continue
```

Therefore favor technologies that can be introduced progressively without requiring a huge initial infrastructure commit.

Research whether the candidate technologies support this style of incremental construction.

Flag technologies whose minimum viable setup introduces excessive generated configuration or infrastructure.

## Research Questions

### 1. Validate the Conceptual Architecture

Identify the minimum architectural primitives necessary to demonstrate a modern analytical data flow locally.

Separate **concepts** from **products**.

Determine which concepts are fundamental and which are optional.

### 2. Evaluate Each Candidate Technology

For each candidate answer:

- What architectural concept does it teach?
- Is that concept important?
- Is this the smallest reasonable implementation?
- Can it run locally?
- Can its internal state be inspected?
- Does it have a strong official/reference implementation?
- How much setup complexity does it introduce?
- Is there a materially simpler alternative?
- Should it be **include**, **defer**, or **reject**?

Give particular scrutiny to Apache NiFi, Snowflake Openflow as conceptual mapping only, FastAPI, Pydantic, DuckDB, dbt-duckdb, Parquet, MinIO, Apache Iceberg, Iceberg REST Catalog, Lakekeeper, and Delta Sharing.

### 3. Identify Missing Concepts

Look specifically for missing fundamentals such as orchestration, incremental ingestion, CDC, idempotency, schema evolution, transactions, partitioning, lineage, provenance, observability, retries, backpressure, data contracts, data quality, authentication/authorization, secrets, interoperability, and ownership/governance.

Do **not** automatically recommend another product for each concept.

Determine which concepts can be demonstrated using capabilities already present in the proposed stack.

Classify each as **teach immediately / demonstrate later / acknowledge only**.

### 4. Find Canonical Runnable Examples

Find the strongest **official or upstream runnable examples** for each included technology.

Prefer, in order:

1. specifications
2. official documentation
3. official project repositories
4. official quickstarts/examples
5. project-maintainer material
6. high-quality independent material only when necessary

Look particularly for existing local examples involving combinations such as NiFi + HTTP, NiFi + Parquet, DuckDB + Parquet, DuckDB + Iceberg, Iceberg REST Catalog, Lakekeeper + DuckDB, MinIO + Iceberg, dbt + DuckDB, FastAPI + Pydantic, and an open data-sharing reference server/client.

Do not invent integrations merely because they appear technically possible.

Explicitly identify which combinations have authoritative runnable precedent and which would require us to design the integration ourselves.

### 5. Inspectability

Evaluate technologies partly by how well they let a learner see underneath the abstraction.

For each included technology identify the most educational artifacts/interfaces to inspect, such as curl responses, FlowFiles, NiFi queues, provenance events, Parquet metadata, MinIO objects, Iceberg metadata JSON, manifest lists, manifest files, snapshots, REST catalog calls, DuckDB objects, dbt compiled SQL, and Pydantic validation errors.

### 6. Progressive Build Order

Recommend a **breadth-first sequence**.

Each increment should add approximately one new architectural idea while keeping the existing system working.

Do not accept any proposed sequence blindly. Recommend a better sequence if the evidence supports one.

Avoid going deeply into any single technology before the learner has seen the complete vertical architecture.

### 7. Complexity Budget

Estimate the relative implementation/configuration burden of each proposed stage using rough categories: **tiny / small / medium / large**.

Flag anything likely to require hundreds of handwritten lines, large generated configuration, numerous containers, substantial JVM/application configuration, complex networking, or infrastructure unrelated to the concept being taught.

Look specifically for opportunities to eliminate components while preserving the lesson.

### 8. What NOT to Learn Yet

Explicitly evaluate whether the initial lab needs Kafka, Airflow, Spark, Kubernetes, Terraform, cloud infrastructure, distributed compute, dedicated observability platforms, dedicated data-quality platforms, or schema registries.

Do not include them merely because they are common in modern data architectures.

State the concrete future problem that would justify introducing each deferred technology.

## Evidence Standard

Prioritize primary and authoritative sources.

For Apache projects, prefer Apache specifications, documentation and repositories. For DuckDB, prefer DuckDB documentation/repositories. For dbt, prefer dbt documentation. For Pydantic and FastAPI, prefer their official documentation. For Lakekeeper, use its official documentation/repository. For Snowflake Openflow, use Snowflake documentation only to understand the relationship to NiFi and relevant architectural concepts. For sharing protocols, prioritize the actual protocol specification and reference implementation.

Cite factual claims directly.

Clearly distinguish **documented fact** from **research recommendation** from **proposed lab design**.

If authoritative evidence for an integration cannot be found, say: **No reliable authoritative example found.**

Do not fill the gap by inventing an implementation.

## Deliverable

Produce a compact **architecture decision brief**, not a tutorial.

Start with `## Recommended Minimal Architecture` and show the smallest recommended technology stack and a simple architecture diagram.

Then `## Decisions` with a table:

| Concept | Technology | Decision | Why | Authoritative foundation |
|---|---|---|---|---|

Decision must be **INCLUDE / DEFER / REJECT**.

Then provide:

- `## Missing Concepts`
- `## Canonical Examples`
- `## Progressive Learning Sequence`
- `## Deferred Technology`
- `## Risks / Weak Evidence`
- `## Orchestrator Handoff`

For each proposed Git-sized stage in the learning sequence include:

```text
Stage:
New concept:
Technology:
Observable result:
What to inspect:
Authoritative example:
Complexity:
```

Keep stages extremely small.

Do **not** write implementation code.
Do **not** create the repository.
Do **not** generate Docker Compose.
Do **not** create a production architecture.

The research succeeds if a later orchestrator can use it to construct the **smallest possible inspectable local ecosystem without having to invent how the underlying technologies work**.
