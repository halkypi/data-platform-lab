# Orchestrator Handoff — Minimal Local Data Platform

## Readiness

**READY FOR ORCHESTRATION**

The research and challenger artifacts are now preserved on `main`. The remaining early blocker was the NiFi 2.11.0 stock-binary Parquet question. A learner-run local verification closed that question as **FAIL** for the stock binary.

## Empirical closure: NiFi 2.11.0 stock binary

The local verification used the official archive:

- URL: `https://archive.apache.org/dist/nifi/2.11.0/nifi-2.11.0-bin.zip`
- file: `nifi-2.11.0-bin.zip`
- SHA-256: `e549acad7e320416b12cb3a902884d0d5458cecd602d1ffd3f26d79081d7f512`
- official SHA-512: matched locally

Inventory of the extracted standard binary established:

- `nifi-parquet-nar`: **absent**
- `nifi-hadoop-libraries-nar`: **absent**
- `nifi-record-serialization-services-nar`: present
- `nifi-standard-nar`: present
- custom/copied/separately downloaded NARs: none

Therefore the stock NiFi 2.11.0 binary cannot configure `ParquetRecordSetWriter` without additional packaging. Startup was unnecessary to decide this stock-binary gate because the required extension is absent before runtime.

This empirically agrees with the source-level evidence already recorded in `research/minimal-local-data-platform.md` that Parquet support is associated with the `include-hadoop` build profile.

## Architecture decision

Keep **Apache NiFi** in the early learning path because FlowFiles, connections/queues, provenance, routing and backpressure are explicit concepts worth observing.

Do **not** require NiFi to create Parquet in the first vertical slice. Additional Hadoop/Parquet NAR packaging adds setup cost without adding enough learning value at that point.

Use this initial path instead:

```text
FastAPI + Pydantic
  -> HTTP/JSON
  -> NiFi
  -> raw JSON on local filesystem
  -> DuckDB converts JSON to Parquet
  -> DuckDB queries/inspects Parquet
  -> dbt Core + dbt-duckdb
  -> FastAPI serving
```

This keeps the key distinctions visible:

- source/application contract vs transport;
- transport/queued flow vs persisted file;
- JSON representation vs Parquet representation;
- storage vs compute;
- plain SQL vs dbt-managed transformation/test;
- analytical result vs served API contract.

NiFi-to-Parquet can be revisited later only if learning the extension/NAR packaging boundary itself becomes worthwhile.

## Later path

After the first complete slice and comprehension checkpoint:

1. PyIceberg + SQLite + local `file://` warehouse for files vs table metadata.
2. DuckDB direct read of Iceberg metadata for table format vs catalog.
3. Remote Iceberg REST catalog only after a minimal authoritative implementation path is established; evaluate the Apache Iceberg REST test fixture before Lakekeeper.
4. Object storage, Lakekeeper and open sharing remain deferred until their concepts earn the infrastructure.

## Orchestrator constraints

Start with **Stage 1 only**. Do not generate or implement later stages yet.

Stage 1 should teach only: a tiny contracted transaction source using FastAPI + Pydantic + HTTP/JSON, with 3–5 synthetic records including `TX001`, directly inspectable with `curl` and a deliberate validation failure.

After the Stage 1 implementation commit, stop for learner inspection and explanation before proposing Stage 2.
