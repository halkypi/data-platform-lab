# Evidence-Backed Challenger Review — Minimal Local Data Platform

This document is the **evidence-backed challenger review** of the immutable Researcher brief. It is not the final architecture and does not reconcile the Researcher’s findings on the Researcher’s behalf.

## Challenger Verdict

**REVISE**

The Researcher’s central architecture is substantially sound and salvageable, but the committed brief is not yet strong enough for APPROVE. Independent upstream verification confirms the most important simplifications: local filesystem before object storage, Parquet before Iceberg, PyIceberg with SQLite/local filesystem as a real first Iceberg implementation, DuckDB as a strong inspectable bridge across Parquet and Iceberg, dbt Core + dbt-duckdb as a small inspectable transformation layer, Delta Sharing deferral, MinIO deferral, and a deliberately shallow NiFi→Openflow mapping. See [PyIceberg](https://py.iceberg.apache.org/), [DuckDB Iceberg](https://duckdb.org/docs/current/core_extensions/iceberg/overview), [dbt-duckdb](https://github.com/duckdb/dbt-duckdb), [Delta Sharing](https://github.com/delta-io/delta-sharing), [MinIO](https://github.com/minio/minio), and [Snowflake Openflow](https://docs.snowflake.com/en/user-guide/data-integration/openflow/about).

Three findings prevent approval.

First, the early **NiFi HTTP/JSON→Parquet stage remains evidence-incomplete**. Current Apache sources establish the necessary component capabilities, but no authoritative current assembled flow was found demonstrating the exact integration. This is the Researcher’s own largest early gap, and it sits on the first vertical slice. **No reliable authoritative example found.** Apache also warns that the standard binary does not contain every release NAR, so current-release packaging has to be pinned rather than inferred. See the [NiFi Administration Guide](https://nifi.apache.org/nifi-docs/administration-guide.html), [InvokeHTTP](https://nifi.apache.org/components/org.apache.nifi.processors.standard.InvokeHTTP/), [ConvertRecord](https://nifi.apache.org/components/org.apache.nifi.processors.standard.ConvertRecord/), [PutFile](https://nifi.apache.org/components/org.apache.nifi.processors.standard.PutFile/), and the [NiFi 2.11 Parquet bundle](https://github.com/apache/nifi/tree/rel/nifi-2.11.0/nifi-extension-bundles/nifi-parquet-bundle).

Second, the proposed later **Lakekeeper REST-catalog stage hides a required infrastructure transition**. Lakekeeper currently supports warehouse storage on S3, ADLS Gen2, OneLake, and GCS—not a local-filesystem warehouse—and its getting-started documentation says that creating a warehouse requires an external object store. Its official minimal deployment also introduces more infrastructure than the local PyIceberg lesson. Lakekeeper therefore cannot follow the local-filesystem Iceberg lesson exactly as the brief’s stage sequence suggests without first introducing an object-storage concept and implementation. See [Lakekeeper storage](https://docs.lakekeeper.io/docs/latest/storage/) and [Lakekeeper getting started](https://docs.lakekeeper.io/getting-started/).

Third, the Researcher missed a materially smaller official candidate for teaching the **REST-catalog concept**: Apache Iceberg itself ships a REST test fixture whose server defaults can use `JdbcCatalog` with SQLite and a temporary local filesystem warehouse. DuckDB’s Iceberg project explicitly tests against the Apache REST fixture, although assembled DuckDB fixtures may override those local defaults with object storage. The Apache fixture therefore deserves investigation before Lakekeeper, but the exact DuckDB + fixture + local-filesystem assembled path is not sufficiently established to substitute it blindly. See Apache Iceberg’s [`RESTCatalogServer`](https://github.com/apache/iceberg/blob/c07a081c8ab8687cd0531101db64922f6dbb2de6/open-api/src/testFixtures/java/org/apache/iceberg/rest/RESTCatalogServer.java) and the [DuckDB Iceberg project](https://github.com/duckdb/duckdb-iceberg).

The appropriate correction is therefore **not a wholesale architecture change**. Preserve the initial architecture, strengthen NiFi’s evidence gate and semantics, and change the late catalog sequence from “add Lakekeeper” to “introduce the REST-catalog concept only after an authoritative minimal implementation path has been closed; evaluate the Apache fixture first; retain Lakekeeper for a later realistic catalog-service lesson.”

## Input and Method

| Input | Value |
|---|---|
| Repository | `halkypi/data-platform-lab` |
| Researcher branch | `research/minimal-local-data-platform` |
| Researcher commit | `cffecf68252c08d34f2a0d6ed90f9477fb5f15b8` |
| Researcher path | `research/minimal-local-data-platform.md` |
| Researcher blob | `2846ec966d3a73a32291fc7deca622419c47d31c` |
| Research date | August 21, 2026 |

The immutable Researcher artifact reviewed was [`research/minimal-local-data-platform.md` at commit `cffecf682...`](https://github.com/halkypi/data-platform-lab/blob/cffecf68252c08d34f2a0d6ed90f9477fb5f15b8/research/minimal-local-data-platform.md), not a moving branch head.

The governing repository documents were treated as authoritative: [`AGENTS.md`](https://github.com/halkypi/data-platform-lab/blob/f821aabcd903ac69ef2589d00c13ecf710a49588/AGENTS.md), [`docs/learning-governance.md`](https://github.com/halkypi/data-platform-lab/blob/f821aabcd903ac69ef2589d00c13ecf710a49588/docs/learning-governance.md), and [`prompts/deep-research.md`](https://github.com/halkypi/data-platform-lab/blob/f821aabcd903ac69ef2589d00c13ecf710a49588/prompts/deep-research.md). Their constraints were applied throughout: authoritative upstream grounding, explicit refusal to invent unsupported integrations, complexity that must earn its place, and demonstrated understanding per learner minute.

The evidence hierarchy was:

1. specifications;
2. official documentation;
3. official project repositories;
4. official runnable examples and quickstarts;
5. project-maintainer material;
6. independent sources only when primary evidence was insufficient.

Only primary upstream sources were used for material technical findings: Apache NiFi documentation/source, Apache Iceberg/PyIceberg documentation/source, DuckDB documentation/source/tests, Lakekeeper documentation/repository, DuckDB Foundation’s `dbt-duckdb` repository plus dbt Labs documentation, the official Delta Sharing repository, the official MinIO repository, and Snowflake Openflow documentation.

Current-version sensitivity matters. Apache lists **NiFi 2.11.0, released August 3, 2026**, as the current NiFi 2 release in the [NiFi downloads page](https://nifi.apache.org/download/).

“Confirmed” below means upstream evidence materially supports the Researcher. “Qualified” means the basic conclusion survives but requires correction. “Overturned” means the evidence changes the decision or stage substantially. Absence of an assembled example is not treated as proof that an integration is technically impossible.

## Evidence Matrix

| Research stream / exact claim tested | Preferred or consulted primary sources | Evidence supporting the Researcher | Evidence overturning or materially qualifying the Researcher | Documented fact | Challenger interpretation | Challenger recommendation | Affected architecture decision | Closure status | Closure rationale |
|---|---|---|---|---|---|---|---|---|---|
| **1. NiFi deserves INCLUDE because queues, backpressure, routing and provenance are inspectable.** | [NiFi User Guide](https://nifi.apache.org/nifi-docs/user-guide.html), [NiFi Administration Guide](https://nifi.apache.org/nifi-docs/administration-guide.html), [NiFi downloads](https://nifi.apache.org/download/) | Connections expose FlowFile queues; backpressure thresholds affect scheduling; provenance is inspectable and supports replay. | NiFi 2.11 requires Java 21, multiple persistent repositories, generated flow/configuration state, local HTTPS/security setup and extension/NAR packaging awareness. | NiFi exposes the requested runtime state, but with a substantial bootstrap surface. | The learning value is real because the lab explicitly wants visible queue/backpressure/provenance state; primary evidence cannot objectively prove the highest possible learning ROI. | Keep NiFi INCLUDE but state bootstrap burden more strongly and separate its runtime concepts precisely. | Apache NiFi INCLUDE and early sequence. | **CLOSED for decision** | Evidence establishes both the unique observable state and the burden strongly enough to retain the decision as a curriculum judgment. |
| **1. Current NiFi can support HTTP/JSON→record→Parquet→filesystem without invention.** | [InvokeHTTP](https://nifi.apache.org/components/org.apache.nifi.processors.standard.InvokeHTTP/), [ConvertRecord](https://nifi.apache.org/components/org.apache.nifi.processors.standard.ConvertRecord/), [PutFile](https://nifi.apache.org/components/org.apache.nifi.processors.standard.PutFile/), [NiFi Parquet bundle](https://github.com/apache/nifi/tree/rel/nifi-2.11.0/nifi-extension-bundles/nifi-parquet-bundle), [Administration Guide](https://nifi.apache.org/nifi-docs/administration-guide.html) | The required supported primitives and Parquet extension exist upstream. | No current authoritative assembled tiny HTTP/JSON→Parquet flow was found; Apache warns that the standard binary does not contain every release NAR. | Component capability is established; assembled integration precedent is not. | Separate capabilities must not be treated as proof of a finished flow. | Retain the planned concept, but hard-gate implementation on exact NiFi 2.11 processor/controller-service/NAR verification. | NiFi→Parquet stage. | **PARTIALLY CLOSED** | Primitive support is closed; assembled integration and exact packaging remain open. **No reliable authoritative example found.** |
| **1. The proposed NiFi failure/retry/backpressure lesson is semantically accurate.** | [InvokeHTTP](https://nifi.apache.org/components/org.apache.nifi.processors.standard.InvokeHTTP/), [NiFi User Guide](https://nifi.apache.org/nifi-docs/user-guide.html) | `InvokeHTTP` exposes outcome relationships; NiFi exposes queues, backpressure and provenance replay. | `Retry` relationship routing, automatic relationship retry, processor yielding/penalty, queue backpressure and provenance replay are distinct mechanisms. | These mechanisms exist but are not synonyms. | The original “failure/retry/idempotency” lesson compresses several independently observable concepts. | Rewrite the lesson to distinguish HTTP outcome routing, configured retry, backpressure, and provenance replay. | Stages for failure, retry, idempotency, backpressure. | **CLOSED** | Current Apache documentation is sufficient to establish the distinctions. |
| **1. Local NiFi provides a useful mental model for Snowflake Openflow.** | [Snowflake Openflow](https://docs.snowflake.com/en/user-guide/data-integration/openflow/about), [NiFi User Guide](https://nifi.apache.org/nifi-docs/user-guide.html) | Snowflake explicitly says Openflow is built on/powered by Apache NiFi. | Openflow adds managed security, compliance, observability, maintainability and deployment semantics; one-to-one processor/security/governance/operating transfer is unsupported. | NiFi ancestry is documented; operational equivalence is not. | FlowFile/processor/dataflow concepts transfer safely at a narrow mental-model level. | Keep Openflow runtime REJECT and preserve only a shallow conceptual mapping. | Openflow REJECT; NiFi rationale. | **CLOSED** | Primary Snowflake evidence is sufficient for the narrow conclusion. |
| **2. PyIceberg + SQLite + local filesystem is the smallest authoritative first real Iceberg lesson.** | [PyIceberg](https://py.iceberg.apache.org/), [Apache Iceberg specification](https://iceberg.apache.org/spec/) | Official PyIceberg material demonstrates a SQL catalog backed by SQLite and a `file://` warehouse without another service, with real Iceberg table operations. | PyIceberg describes local filesystem use as a testing/demo topology rather than production-scale deployment. | SQLite + local filesystem is an upstream-supported demo/testing topology that creates genuine Iceberg state. | The production limitation is aligned with, not adverse to, this tiny local learning lab. | Keep PyIceberg + SQLite + filesystem INCLUDE after plain Parquet. | PyIceberg INCLUDE; Iceberg stage order. | **CLOSED** | Direct Apache documentation establishes the required topology and artifacts. |
| **3. DuckDB can read PyIceberg-produced local Iceberg output without the PyIceberg catalog.** | [DuckDB Iceberg overview](https://duckdb.org/docs/current/core_extensions/iceberg/overview), [DuckDB Iceberg project](https://github.com/duckdb/duckdb-iceberg), [PyIceberg](https://py.iceberg.apache.org/) | DuckDB documents catalog-free direct table access as read-only and exposes Iceberg metadata/snapshot inspection; DuckDB’s Iceberg project contains tests against PyIceberg-generated data. | The DuckDB Iceberg extension is still experimental; direct-path access is read-only and metadata/version behavior should be pinned to the implementation version. | Catalog-free read access is supported; catalog-mediated operations form a separate boundary. | This is unusually strong evidence for “table format ≠ catalog.” | Keep DuckDB central and retain the direct Iceberg read stage; pin the version/evidence when implemented. | DuckDB INCLUDE; Iceberg stages. | **CLOSED** | Direct DuckDB documentation plus upstream interoperability tests materially establish the intended path. |
| **4. Lakekeeper is the right first later REST-catalog implementation.** | [Iceberg REST Catalog specification](https://iceberg.apache.org/rest-catalog-spec/), [Lakekeeper storage](https://docs.lakekeeper.io/docs/latest/storage/), [Lakekeeper getting started](https://docs.lakekeeper.io/getting-started/), [Apache RESTCatalogServer](https://github.com/apache/iceberg/blob/c07a081c8ab8687cd0531101db64922f6dbb2de6/open-api/src/testFixtures/java/org/apache/iceberg/rest/RESTCatalogServer.java), [DuckDB Iceberg project](https://github.com/duckdb/duckdb-iceberg) | Lakekeeper is a real REST catalog implementation with DuckDB precedent and is appropriate for a realistic later catalog-service lesson. | Lakekeeper requires an external object store for a warehouse and typically introduces additional infrastructure; Apache Iceberg itself ships a smaller REST test fixture using SQLite/local filesystem defaults. | Lakekeeper’s supported storage is external-object-store based; Apache has a materially smaller fixture for the protocol boundary. | Lakekeeper teaches a realistic service plus storage/credential concerns, while the Apache fixture may isolate the catalog concept better. | Keep REST Catalog INCLUDE as a concept. Keep Lakekeeper DEFER; remove it as the automatic first REST implementation. Evaluate the Apache fixture first, but keep that concrete path evidence-gated. | Iceberg REST Catalog INCLUDE; Lakekeeper DEFER; remote-catalog stage order. | **PARTIALLY CLOSED** | Decision change is supported, but a complete DuckDB + Apache fixture + local-filesystem assembled path is not yet closed. **No reliable authoritative example found.** |
| **4. Lakekeeper + MinIO specifically lacks authoritative compatibility.** | [Lakekeeper storage](https://docs.lakekeeper.io/docs/latest/storage/) | The Researcher was correct that separate S3 compatibility claims should not be synthesized into a runnable example. | Lakekeeper’s current storage documentation explicitly says S3 support is tested with Minio, which is stronger compatibility evidence than the Researcher stated. | Minio compatibility is documented by Lakekeeper; a current minimal Lakekeeper-provided MinIO assembled example was not located. | Compatibility and a canonical minimal runnable example are different claims. | Correct the wording: compatibility exists, but the minimal assembled example remains unclosed. | Lakekeeper/object-storage evidence wording. | **CLOSED for compatibility; OPEN for minimal assembled example** | Current Lakekeeper documentation resolves compatibility. For the narrower runnable example: **No reliable authoritative example found.** |
| **5. dbt Core + dbt-duckdb earns INCLUDE after plain DuckDB SQL.** | [dbt-duckdb](https://github.com/duckdb/dbt-duckdb), [dbt data tests](https://docs.getdbt.com/docs/build/data-tests) | The adapter supports very small local configuration, persistent DuckDB and external Parquet; dbt exposes model compilation and test SQL as inspectable artifacts. | It introduces another abstraction layer, but the Researcher already places plain DuckDB SQL first. | dbt adds compiled SQL/materialization/test artifacts that plain SQL alone does not expose as a framework concept. | The marginal learning value is sufficient once the learner already understands raw DuckDB SQL. | Keep dbt Core + dbt-duckdb INCLUDE in the proposed relative order. | dbt INCLUDE and stage placement. | **CLOSED** | Upstream adapter/docs establish small setup and unique inspectable artifacts. |
| **6. No sufficiently small authoritative fully local Delta Sharing path exists for this lab.** | [Delta Sharing repository](https://github.com/delta-io/delta-sharing) | Official reference server/client exists; the documented architecture is cloud/object-storage oriented. | No official filesystem-only server binding equivalent to this lab’s initial local topology was found. | Reference implementation exists, but the needed fully local binding is not established. | Adding storage emulation solely to satisfy sharing would violate minimality unless sharing itself becomes the learning objective. | Keep Delta Sharing DEFER with a concrete future trigger: a verified authoritative local path or an explicit object-store-backed sharing lesson. | Delta Sharing DEFER; sharing stage. | **CLOSED for DEFER decision** | The absence of the required local path is sufficient to support deferral. **No reliable authoritative example found.** |
| **7. Object storage should be deferred from early Parquet/Iceberg lessons.** | [PyIceberg](https://py.iceberg.apache.org/), [Apache Parquet](https://parquet.apache.org/docs/file-format/), [DuckDB Parquet](https://duckdb.org/docs/current/data/parquet/overview) | Parquet and the first genuine Iceberg lesson work on local filesystem; object keys/S3 APIs/credentials are not necessary for those concepts. | Lakekeeper later introduces a real object-store requirement. | Early file/table concepts do not require object-store semantics; later realistic catalog service may. | Object storage should earn its own lesson rather than appear as ambient infrastructure. | Keep object storage DEFER initially and introduce it only before a technology that actually requires it. | Object storage DEFER; Lakekeeper sequence. | **CLOSED** | Primary docs establish the filesystem-first topology and Lakekeeper establishes the later trigger. |
| **7. MinIO’s current upstream status was characterized accurately.** | [MinIO repository](https://github.com/minio/minio), [Lakekeeper storage](https://docs.lakekeeper.io/docs/latest/storage/) | The official community repository states it is no longer maintained and that community distribution is source-only; historical precompiled binaries receive no updates. | MinIO can still be technically interoperable with later S3-compatible systems; Lakekeeper explicitly documents testing with Minio. | Maintenance/distribution status and interoperability are separate facts. | The repository status weakens MinIO as a new foundational lab dependency but does not prove incompatibility. | Keep MinIO DEFER and make a fresh object-store product choice only if/when the concept becomes necessary. | MinIO DEFER. | **CLOSED** | Current primary-source status is explicit and sufficient. |

## Verified Findings

### HIGH — The NiFi→Parquet stage is still not orchestrator-ready

**Exact Researcher claim or section:** the early stage “First analytical file” can use Apache NiFi to materialize the HTTP/JSON transaction batch as a real Parquet file on the ordinary local filesystem.

**Challenger conclusion:** **QUALIFIES** the claim. The factual capability argument is credible, but the assembled integration remains insufficiently grounded for implementation under this repository’s rules.

**Direct authoritative evidence:** `InvokeHTTP` is current Apache NiFi functionality; [`ConvertRecord`](https://nifi.apache.org/components/org.apache.nifi.processors.standard.ConvertRecord/) converts data through configured Record Reader/Writer services; [`PutFile`](https://nifi.apache.org/components/org.apache.nifi.processors.standard.PutFile/) persists to the filesystem; and the NiFi 2.11 source includes the [`nifi-parquet-bundle`](https://github.com/apache/nifi/tree/rel/nifi-2.11.0/nifi-extension-bundles/nifi-parquet-bundle). The [NiFi Administration Guide](https://nifi.apache.org/nifi-docs/administration-guide.html) also warns that the standard binary does not contain every release NAR.

**Documented fact:** the constituent processors/services and Parquet implementation exist.

**Challenger interpretation:** existence of the primitives is not an assembled integration precedent.

**Challenger recommendation:** keep NiFi and Parquet INCLUDE, but make this stage a hard evidence/empirical gate before implementation. Pin the exact NiFi release and exact reader/writer/NAR availability first.

**Effect on architecture or stage order:** no technology replacement yet, but the first vertical slice must stop at this gate if the exact path is not closed.

**Required correction:** explicitly mark the stage as hard-gated and avoid handing an orchestrator a configuration it would have to invent.

**Closure:** **PARTIALLY CLOSED**.

For the exact current tiny `InvokeHTTP → JSON records → Parquet → local filesystem` assembled flow: **No reliable authoritative example found.**

### HIGH — The proposed Lakekeeper stage omits a mandatory storage transition, and Lakekeeper is not the smallest first REST-catalog lesson

**Exact Researcher claim or section:** Lakekeeper is deferred until the remote catalog stage, where DuckDB can discover/query a Lakekeeper-managed table through the Iceberg REST Catalog.

**Challenger conclusion:** **MATERIALLY QUALIFIES** the proposed stage.

**Direct authoritative evidence:** [Lakekeeper storage documentation](https://docs.lakekeeper.io/docs/latest/storage/) lists object-storage-backed warehouse options and says S3 support is tested with AWS and Minio. [Lakekeeper getting started](https://docs.lakekeeper.io/getting-started/) states that an external object store is needed to create a warehouse. Apache Iceberg’s own [`RESTCatalogServer`](https://github.com/apache/iceberg/blob/c07a081c8ab8687cd0531101db64922f6dbb2de6/open-api/src/testFixtures/java/org/apache/iceberg/rest/RESTCatalogServer.java) provides a smaller protocol fixture with SQLite/local-filesystem-capable defaults.

The [DuckDB Iceberg project](https://github.com/duckdb/duckdb-iceberg) includes REST-catalog integration testing against upstream catalog implementations, including the Apache Iceberg fixture. This is evidence that the Apache fixture is a legitimate candidate, but not proof that the exact local-filesystem DuckDB assembled path is already closed.

**Documented fact:** Lakekeeper requires external object storage for a usable warehouse; Apache Iceberg maintains a smaller REST test fixture capable of a SQLite/local-filesystem topology.

**Challenger interpretation:** Lakekeeper teaches a realistic catalog service plus storage/credential concerns; the Apache fixture is better aligned with isolating “what does the REST catalog boundary add?”

**Challenger recommendation:** REST Catalog stays INCLUDE as a concept. Lakekeeper stays DEFER and should no longer be the automatic first REST implementation. Evaluate the Apache fixture first, but keep the concrete first-REST implementation evidence-gated until two-sided local interoperability is closed.

**Effect on architecture or stage order:** insert an explicit REST-catalog implementation evidence gate; if Lakekeeper is later used, object storage must precede it.

**Required correction:** remove the implied direct local-filesystem→Lakekeeper progression and make the object-store transition explicit.

**Closure:** **PARTIALLY CLOSED**.

For a canonical tiny assembled DuckDB + Apache REST fixture + local-filesystem write/read workflow: **No reliable authoritative example found.**

The Researcher’s stronger-sounding “Lakekeeper + MinIO unsupported” concern also needs wording correction. Lakekeeper now explicitly documents Minio as tested S3 storage. That is authoritative compatibility evidence, although a current Lakekeeper-provided *minimal assembled example* using MinIO was not located. For that narrower runnable-example claim: **No reliable authoritative example found.**

### HIGH — PyIceberg SQLite/local-filesystem Iceberg is directly confirmed

**Exact Researcher claim or section:** use PyIceberg’s documented local SQL catalog plus local filesystem for the first real Iceberg lesson.

**Challenger conclusion:** **CONFIRMS** the claim.

**Direct authoritative evidence:** [PyIceberg](https://py.iceberg.apache.org/) demonstrates a SQL catalog backed by SQLite and a `file://` warehouse, explicitly supporting local testing without another service. The [Apache Iceberg specification](https://iceberg.apache.org/spec/) defines the real metadata, snapshot, manifest and commit structures that such an implementation produces.

**Documented fact:** SQLite SQL catalog + local filesystem warehouse is an upstream-supported PyIceberg demo/testing topology.

**Challenger interpretation:** this topology is unusually well matched to “files ≠ table” because it introduces real Iceberg state without simultaneously introducing a network service, credentials, or object storage.

**Challenger recommendation:** retain **PyIceberg + SQLite + filesystem: INCLUDE**, in the proposed position after plain Parquet.

**Effect on architecture or stage order:** strengthens the Researcher’s ordering.

**Required correction:** only preserve the local-demo/testing qualifier; no architecture change.

**Closure:** **CLOSED; Researcher confirmed.**

### HIGH — DuckDB↔PyIceberg local interoperability is more strongly supported than the Researcher demonstrated

**Exact Researcher claim or section:** DuckDB can read an Iceberg table from metadata without the PyIceberg catalog, making “table format ≠ catalog” directly observable.

**Challenger conclusion:** **CONFIRMS and strengthens** the claim.

**Direct authoritative evidence:** [DuckDB Iceberg](https://duckdb.org/docs/current/core_extensions/iceberg/overview) documents direct, catalog-free Iceberg table access and states that this mode is read-only. It also exposes Iceberg metadata/snapshot inspection. The [DuckDB Iceberg upstream project](https://github.com/duckdb/duckdb-iceberg) contains cross-implementation test data and tests built from PyIceberg output rather than merely asserting independent compatibility.

**Documented fact:** DuckDB has upstream interoperability coverage against PyIceberg-generated Iceberg state, while direct-path access remains read-only.

**Challenger interpretation:** this is unusually strong evidence for the intended “table format ≠ catalog” lesson.

**Challenger recommendation:** keep DuckDB central and keep the catalog-free stage. Add a version pin/evidence check because the Iceberg extension is still evolving/experimental.

**Effect on architecture or stage order:** strengthens DuckDB’s position and the PyIceberg→DuckDB sequence.

**Required correction:** add version sensitivity and the read-only boundary explicitly.

**Closure:** **CLOSED; Researcher strongly confirmed.**

### MEDIUM — NiFi’s educational value survives challenge, but “retry” needs sharper language

**Exact Researcher claim or section:** NiFi earns its complexity because FlowFiles, queues, routing, backpressure, retry behavior and provenance are observable first-class state.

**Challenger conclusion:** **QUALIFIES** the claim but retains INCLUDE.

**Direct authoritative evidence:** [NiFi 2.11](https://nifi.apache.org/download/) runs as a Java 21 application and the [Administration Guide](https://nifi.apache.org/nifi-docs/administration-guide.html) documents its repositories and configuration surfaces. The [NiFi User Guide](https://nifi.apache.org/nifi-docs/user-guide.html) establishes Connection/FlowFile queue behavior, backpressure and provenance/replay. [`InvokeHTTP`](https://nifi.apache.org/components/org.apache.nifi.processors.standard.InvokeHTTP/) distinguishes server-error routing to `Retry`, client errors to `No Retry`, and communication/socket errors to `Failure`.

**Documented fact:** NiFi has first-class queues, routing, backpressure, provenance and replay at the cost of a Java runtime and multiple persistent repositories/configuration surfaces.

**Challenger interpretation:** primary evidence establishes the state NiFi exposes, but cannot objectively prove that it maximizes learning ROI. That remains a curriculum judgment.

**Challenger recommendation:** keep **NiFi: INCLUDE** because the requested curriculum explicitly prioritizes queue/backpressure/provenance inspection. Raise the bootstrap complexity warning and split the failure lesson into “HTTP outcome routing,” “configured retry,” “backpressure,” and “provenance replay.”

**Effect on architecture or stage order:** NiFi stays early; its lesson design becomes more precise.

**Required correction:** stop using “retry” as an umbrella term for multiple mechanisms.

**Closure:** **CLOSED for the INCLUDE decision**; the Parquet integration remains separately open.

### MEDIUM — dbt Core + dbt-duckdb earns its place after plain DuckDB SQL

**Exact Researcher claim or section:** dbt Core + dbt-duckdb should remain INCLUDE, but only after plain SQL is understood.

**Challenger conclusion:** **CONFIRMS** the claim.

**Direct authoritative evidence:** [`duckdb/dbt-duckdb`](https://github.com/duckdb/dbt-duckdb) documents a very small local profile, persistent DuckDB through a path, and external Parquet/other file operation. [dbt data tests](https://docs.getdbt.com/docs/build/data-tests) expose analytical assertions and compiled SQL artifacts distinct from application-boundary validation.

**Documented fact:** local persistent DuckDB, external Parquet, models and compiled test SQL all have current upstream precedent.

**Challenger interpretation:** dbt adds concepts—model compilation/materialization and analytical assertions—that plain SQL does not expose by itself.

**Challenger recommendation:** retain **dbt Core + dbt-duckdb: INCLUDE** and retain the Researcher’s rule that plain DuckDB SQL precedes it. There is insufficient evidence to require moving dbt behind API serving; that sequencing question is pedagogical rather than an integration failure.

**Effect on architecture or stage order:** unchanged relative order.

**Required correction:** none beyond version pinning at implementation time.

**Closure:** **CLOSED; Researcher confirmed.**

### MEDIUM — Delta Sharing deferral is supported

**Exact Researcher claim or section:** defer Delta Sharing because no authoritative fully local binding to the proposed filesystem/MinIO topology was found.

**Challenger conclusion:** **CONFIRMS** the DEFER decision.

**Direct authoritative evidence:** the official [Delta Sharing repository](https://github.com/delta-io/delta-sharing) provides the protocol and reference server/client and describes a storage-oriented sharing architecture centered on object/cloud storage backends. The reference server is suitable for testing connector implementations rather than proving the missing filesystem-only topology.

**Documented fact:** a reference server/client exists and the documented transfer architecture is object/cloud-storage oriented.

**Challenger interpretation:** adding storage emulation solely to satisfy the sharing box would violate the project’s minimality rule unless open-sharing itself becomes the next learning objective.

**Challenger recommendation:** keep **Delta Sharing: DEFER**. The future trigger should be a verified official/local reference path—or a later explicit decision to make object-store-backed sharing the concept under study.

**Effect on architecture or stage order:** sharing stays outside the initial complete slice.

**Required correction:** keep the evidence-failure wording and future trigger explicit.

**Closure:** **CLOSED for the DEFER decision**.

For a current authoritative reference-server example sharing this exact filesystem-only local lab: **No reliable authoritative example found.**

### MEDIUM — MinIO’s status was correctly characterized and is now clearer

**Exact Researcher claim or section:** MinIO should not be foundational because its current upstream maintenance/distribution status has changed materially compared with older lakehouse tutorials.

**Challenger conclusion:** **CONFIRMS and strengthens** the factual premise.

**Direct authoritative evidence:** the official [`minio/minio`](https://github.com/minio/minio) repository states that the repository is no longer maintained and that community distribution is source-only; historical precompiled binaries receive no updates. Lakekeeper’s current [storage documentation](https://docs.lakekeeper.io/docs/latest/storage/) separately documents testing of S3 storage with Minio.

**Documented fact:** the historical community repository/distribution changed materially and is no longer maintained, while Minio compatibility can still exist in downstream systems.

**Challenger interpretation:** “can interoperate” and “is the right new learning-lab dependency” are different questions.

**Challenger recommendation:** keep **object storage: DEFER** and **MinIO: DEFER**. Do not select a replacement object store yet; make that technology decision when object storage becomes necessary.

**Effect on architecture or stage order:** unchanged initial architecture; future object-store selection remains open.

**Required correction:** avoid wording that implies technical incompatibility.

**Closure:** **CLOSED; Researcher confirmed.**

### LOW — The NiFi→Openflow mapping is defensible only at the mental-model level

**Exact Researcher claim or section:** local NiFi is useful for understanding Openflow’s underlying model, while Openflow runtime should not be introduced.

**Challenger conclusion:** **CONFIRMS** the narrow claim.

**Direct authoritative evidence:** [Snowflake Openflow documentation](https://docs.snowflake.com/en/user-guide/data-integration/openflow/about) explicitly says Openflow is built on/powered by Apache NiFi while also describing added managed security, compliance, observability and maintainability capabilities.

**Documented fact:** Openflow is built on NiFi and adds managed-product capabilities.

**Challenger interpretation:** processor/FlowFile/dataflow concepts transfer safely; operational equivalence does not.

**Challenger recommendation:** retain **Openflow runtime: REJECT**, with only a narrow conceptual mapping after NiFi is understood.

**Effect on architecture or stage order:** unchanged.

**Required correction:** keep the mapping intentionally shallow.

**Closure:** **CLOSED; Researcher confirmed.**

## Architecture Decision Effects

Most decisions remain intact. The material revision is concentrated at the two integration gates rather than in the central technology stack.

| Concept / technology | Researcher decision | Challenger decision | Sequence effect |
|---|---:|---:|---|
| FastAPI + Pydantic | INCLUDE | **INCLUDE — unchanged** | None from this challenge. |
| HTTP/JSON | INCLUDE | **INCLUDE — unchanged** | None. |
| Apache NiFi | INCLUDE | **INCLUDE — unchanged, stronger complexity warning** | Bootstrap remains early because its queue/provenance concepts are intentional. |
| NiFi→Parquet stage | Planned early | **Retain, but HARD-GATE** | Do not implement until exact NiFi 2.11 packaging and flow are verified; no invented configuration. |
| Parquet + filesystem | INCLUDE | **INCLUDE — unchanged** | Remains before Iceberg/object storage. |
| DuckDB | INCLUDE | **INCLUDE — strengthened** | Direct PyIceberg interoperability has upstream test evidence. |
| dbt Core + dbt-duckdb | INCLUDE | **INCLUDE — unchanged** | Keep after plain DuckDB SQL. |
| PyIceberg + SQLite + filesystem | INCLUDE | **INCLUDE — strengthened** | Remains first real Iceberg implementation. |
| Iceberg REST Catalog concept | INCLUDE | **INCLUDE — unchanged** | Still comes after local Iceberg metadata. |
| Lakekeeper | DEFER until catalog stage | **DEFER further** | Do not make it the automatic first REST-catalog stage; it introduces object storage and additional service infrastructure. |
| Apache Iceberg REST fixture | Not considered | **DEFER pending one focused verification; preferred first candidate** | Investigate before Lakekeeper because its upstream server can use SQLite + local filesystem defaults. |
| Object storage | DEFER | **DEFER — unchanged initially** | Must precede Lakekeeper if Lakekeeper is eventually introduced. |
| MinIO | DEFER | **DEFER — strengthened** | Do not make the unmaintained community server the default by inertia. |
| Delta Sharing | DEFER | **DEFER — unchanged** | Sharing remains an explicit unresolved endpoint. |
| Openflow runtime | REJECT | **REJECT — unchanged** | Conceptual NiFi mapping only. |

The evidence-supported minimal architecture is therefore still predominantly the Researcher’s architecture, with the remote-catalog boundary made explicit as an evidence gate:

```mermaid
flowchart LR
    A["FastAPI + Pydantic"] -->|"HTTP / JSON"| B["Apache NiFi"]
    B -->|"evidence-gated write"| C["Parquet<br/>local filesystem"]
    C --> D["DuckDB"]
    D --> E["dbt Core<br/>dbt-duckdb"]
    E --> F["FastAPI + Pydantic"]

    C -. "later" .-> G["Apache Iceberg<br/>PyIceberg + SQLite + file://"]
    G -->|"direct read-only metadata path"| D

    G -. "later still" .-> R["Iceberg REST Catalog concept"]
    R --> D

    R -. "first candidate;<br/>verification still required" .-> X["Apache Iceberg<br/>REST test fixture"]
    R -. "realistic later service" .-> L["Lakekeeper"]
    O["Object storage<br/>implementation deferred"] --> L

    F -. "deferred" .-> S["Open data sharing"]
```

The principal sequence correction is narrow:

```mermaid
flowchart TD
    A["FastAPI/Pydantic source"] --> B["NiFi HTTP ingest"]
    B --> C["Queue + backpressure"]
    C --> D["HTTP routing / configured retry / provenance"]
    D --> G{"NiFi→Parquet<br/>evidence gate"}
    G -->|"closed"| E["Parquet on local filesystem"]
    G -->|"not closed"| STOP["STOP: do not invent integration"]

    E --> F["DuckDB direct Parquet SQL"]
    F --> H["dbt model"]
    H --> I["dbt data test"]
    I --> J["FastAPI serving"]
    J --> K["Comprehension checkpoint"]

    K --> L["PyIceberg + SQLite + file://"]
    L --> M["DuckDB direct Iceberg read"]
    M --> N["Snapshot / schema evolution"]
    N --> O{"REST-catalog implementation<br/>evidence gate"}

    O -.-> P["Evaluate Apache REST fixture first"]
    O -.-> Q["Lakekeeper later only after<br/>object-store lesson"]
    O -.-> R["Sharing remains deferred"]
```

This preserves the Researcher’s most important pedagogical ordering:

`physical Parquet file → real Iceberg table metadata → remote catalog boundary`

The revision is about **which evidence closes the boundaries**, not about replacing that progression.

## Findings That Withstood Challenge

| Conclusion that survived | Challenger assessment |
|---|---|
| **Filesystem before object storage** | Strongly supported. PyIceberg provides a `file://` learning topology; no early lesson requires S3 semantics. See [PyIceberg](https://py.iceberg.apache.org/). |
| **Parquet before Iceberg; Iceberg before catalog** | Remains the clearest separation of file, table state, and catalog-mediated management. DuckDB’s direct read-only Iceberg mode makes the latter distinction empirical. See [DuckDB Iceberg](https://duckdb.org/docs/current/core_extensions/iceberg/overview). |
| **PyIceberg is the missing simplifier** | Directly confirmed by Apache documentation. See [PyIceberg](https://py.iceberg.apache.org/). |
| **DuckDB is unusually valuable for inspectability/interoperability** | Strengthened by DuckDB upstream interoperability coverage against PyIceberg-generated local tables. See [DuckDB Iceberg project](https://github.com/duckdb/duckdb-iceberg). |
| **NiFi should not own analytical transformation merely because it can transform** | Remains a sound responsibility-boundary recommendation; NiFi’s unique curriculum value is its visible dataflow state. See [NiFi User Guide](https://nifi.apache.org/nifi-docs/user-guide.html). |
| **Plain DuckDB SQL before dbt** | Supported by dbt-duckdb’s small incremental configuration and inspectable compiled/test SQL. See [dbt-duckdb](https://github.com/duckdb/dbt-duckdb) and [dbt data tests](https://docs.getdbt.com/docs/build/data-tests). |
| **Delta Sharing should not be forced into the first slice** | Supported by the reference implementation’s storage-oriented architecture and absence of the required local binding. See [Delta Sharing](https://github.com/delta-io/delta-sharing). |
| **MinIO should not be foundational** | Strengthened by the repository’s current unmaintained/source-only state. See [MinIO](https://github.com/minio/minio). |
| **Openflow mapping must be shallow** | Confirmed by Snowflake’s simultaneous NiFi ancestry and managed-service differentiation. See [Snowflake Openflow](https://docs.snowflake.com/en/user-guide/data-integration/openflow/about). |

## Remaining Evidence Gaps

| Open question | Status | Smallest further research or empirical verification needed |
|---|---|---|
| Exact NiFi 2.11.0 `InvokeHTTP → JSON record reader → Parquet writer → PutFile` flow and NAR availability | **OPEN / HIGH** | One authoritative current Apache example, or a narrow empirical verification against the exact upstream release documenting every required processor/controller service/NAR. Until then: **No reliable authoritative example found.** |
| Exact DuckDB + Apache Iceberg REST fixture + local-filesystem catalog-managed read/write path | **OPEN / MEDIUM** | A direct upstream test/example, or narrow empirical verification using the fixture’s documented local defaults and a pinned DuckDB Iceberg extension. Do not infer from separate support claims. **No reliable authoritative example found.** |
| Which object-store implementation should accompany Lakekeeper if that lesson is later authorized | **OPEN / LOW now** | No research needed until object-storage semantics become the actual lesson. Lakekeeper’s supported storage interface is established; technology selection can remain deferred. See [Lakekeeper storage](https://docs.lakekeeper.io/docs/latest/storage/). |
| Exact fully local Delta Sharing binding for this lab | **OPEN / LOW now** | Official reference-server support/example for an acceptable local backend. Until then: **No reliable authoritative example found.** See [Delta Sharing](https://github.com/delta-io/delta-sharing). |
| DuckDB Iceberg extension stability over the eventual implementation period | **PARTIALLY CLOSED / ongoing MEDIUM** | Pin the version used by the lab and recheck current extension documentation/repository status at implementation time. See [DuckDB Iceberg project](https://github.com/duckdb/duckdb-iceberg). |

## Quality Audit

The immutable Researcher brief scores **86 / 100**.

| Dimension | Score | Challenger assessment |
|---|---:|---|
| **Scope coverage** | **24 / 25** | Nearly every requested concept, technology, deferral and integration boundary is covered. The principal omission is the smaller Apache REST fixture as a candidate for the remote-catalog lesson. |
| **Evidence integrity and claim-source fit** | **24 / 30** | Primary-source discipline is generally strong and unsupported integrations are usually called out correctly. Deductions are required for the still-unclosed critical NiFi→Parquet path, incomplete Lakekeeper storage dependency, overly broad wording around Lakekeeper+MinIO support, and insufficient direct evidence originally supplied for PyIceberg→DuckDB interoperability despite that evidence existing upstream. |
| **Decision relevance** | **19 / 20** | The brief makes concrete, useful INCLUDE/DEFER/REJECT decisions and materially simplifies the original hypothesis. Most survive challenge. |
| **Critical challenge and minimality** | **11 / 15** | Strong on removing early MinIO and separating PyIceberg from REST catalog infrastructure. Weaker on challenging Lakekeeper against Apache’s own smaller REST fixture and on fully closing NiFi’s bootstrap/integration cost before defending it. |
| **Learning and orchestrator utility** | **8 / 10** | The staged `TX001` trace and comprehension checkpoints are strong. Two stages still cannot safely be handed to an orchestrator as written: NiFi→Parquet lacks assembled precedent, and Lakekeeper requires a previously unstated object-storage transition. |
| **Total** | **86 / 100** | Below the 90-point APPROVE threshold; central design remains sound. |

### Deductions

- **Scope coverage: −1** because the Researcher did not consider Apache Iceberg’s own smaller REST test fixture as a candidate for the remote-catalog concept. Evidence: [`RESTCatalogServer`](https://github.com/apache/iceberg/blob/c07a081c8ab8687cd0531101db64922f6dbb2de6/open-api/src/testFixtures/java/org/apache/iceberg/rest/RESTCatalogServer.java).
- **Evidence integrity and claim-source fit: −6** because the NiFi→Parquet assembled path remains unclosed; Lakekeeper’s object-storage dependency was omitted from the stage sequence; Lakekeeper+MinIO compatibility was understated; and stronger direct DuckDB↔PyIceberg interoperability evidence existed upstream but was not used. Evidence: [NiFi Administration Guide](https://nifi.apache.org/nifi-docs/administration-guide.html), [Lakekeeper storage](https://docs.lakekeeper.io/docs/latest/storage/), [Lakekeeper getting started](https://docs.lakekeeper.io/getting-started/), and [DuckDB Iceberg project](https://github.com/duckdb/duckdb-iceberg).
- **Decision relevance: −1** because the central decisions are actionable and mostly survive challenge, but the first concrete REST-catalog implementation decision needs revision. Evidence: [Lakekeeper getting started](https://docs.lakekeeper.io/getting-started/) and Apache [`RESTCatalogServer`](https://github.com/apache/iceberg/blob/c07a081c8ab8687cd0531101db64922f6dbb2de6/open-api/src/testFixtures/java/org/apache/iceberg/rest/RESTCatalogServer.java).
- **Critical challenge and minimality: −4** because the brief did not sufficiently challenge Lakekeeper against the smaller Apache fixture and defended the NiFi early path before closing the most consequential assembled integration. Evidence: [NiFi Parquet bundle](https://github.com/apache/nifi/tree/rel/nifi-2.11.0/nifi-extension-bundles/nifi-parquet-bundle), [NiFi Administration Guide](https://nifi.apache.org/nifi-docs/administration-guide.html), and Apache [`RESTCatalogServer`](https://github.com/apache/iceberg/blob/c07a081c8ab8687cd0531101db64922f6dbb2de6/open-api/src/testFixtures/java/org/apache/iceberg/rest/RESTCatalogServer.java).
- **Learning and orchestrator utility: −2** because two planned stages still require evidence closure before they can be handed safely to an orchestrator: the early NiFi→Parquet stage and the later REST-catalog implementation. Evidence: [NiFi Administration Guide](https://nifi.apache.org/nifi-docs/administration-guide.html), [Lakekeeper storage](https://docs.lakekeeper.io/docs/latest/storage/), and Apache [`RESTCatalogServer`](https://github.com/apache/iceberg/blob/c07a081c8ab8687cd0531101db64922f6dbb2de6/open-api/src/testFixtures/java/org/apache/iceberg/rest/RESTCatalogServer.java).

### Hard-Gate Audit

| Hard gate | Result | Evidence-backed assessment |
|---|---|---|
| Every requested research stream is addressed | **PASS** | All seven Challenger research streams are represented in the evidence matrix and findings. |
| Every material Challenger finding has direct authoritative support | **PASS** | HIGH/MEDIUM findings cite Apache, DuckDB, Lakekeeper, dbt, Delta Sharing, MinIO or Snowflake primary sources directly. |
| No integration or runnable example is invented | **PASS** | Unclosed NiFi→Parquet, Apache REST-fixture local DuckDB path, and filesystem-only Delta Sharing paths are explicitly reported as unsupported rather than filled with recipes. |
| Facts, interpretations and recommendations are distinguishable | **PASS** | Each material evidence record separates documented fact, Challenger interpretation and Challenger recommendation. |
| Unsupported combinations are explicitly identified | **PASS** | The review uses **No reliable authoritative example found.** for the material unsupported assembled paths. |
| No named decision is silently omitted | **PASS** | Every Researcher decision that could materially change is preserved or explicitly changed in Architecture Decision Effects. |
| No unresolved HIGH finding remains | **FAIL** | The NiFi→Parquet assembled integration is still OPEN/HIGH and lies on the initial vertical slice. |
| Quality score reaches APPROVE threshold | **FAIL** | Independent score is **86/100**, below the required 90/100. |

The hard-gate result is therefore mixed rather than catastrophic. All named architecture decisions are present; unsupported combinations are identified rather than fabricated; facts, interpretations and recommendations are distinguished; and the core PyIceberg/DuckDB path has strong authoritative support. However, one **HIGH** unresolved finding remains on the initial vertical slice—NiFi→Parquet—and the later Lakekeeper stage cannot be implemented as described without introducing an omitted object-storage dependency.

Accordingly, **REVISE** is the evidence-backed verdict: preserve the central architecture, tighten NiFi semantics and its Parquet evidence gate, preserve the strongly verified PyIceberg→DuckDB progression, remove Lakekeeper as the assumed first REST-catalog implementation, explicitly account for Lakekeeper’s object-store boundary, and keep sharing and object-store product selection deferred until their concepts earn a learning stage.
