# Stage 1 TA Verification Report

Repository: `halkypi/data-platform-lab`  
Stage commit: `7cb67a8ad96fcf69a358e83f20e41d51f95de43c`  
Commit message: `lab: add minimal transaction HTTP source`

This report verifies the Stage 1 learner exercises against the exact `app.py` and `pyproject.toml` blobs from the specified implementation commit. It does not modify the Stage 1 implementation or teach later stages.

## 1. Environment and versions

Verification environment:

| Item | Observed |
|---|---|
| OS | Debian GNU/Linux 13 (trixie) |
| Kernel | Linux 6.18.35 x86_64 |
| Python | 3.13.5 |
| FastAPI | 0.128.2 |
| Pydantic | 2.13.4 |
| Uvicorn | 0.48.0 |
| curl | 8.10.1 |

`pyproject.toml` requires Python `>=3.11` and declares unpinned `fastapi` and `uvicorn` dependencies.

Installation command actually used: none. The verification sandbox already contained the versions above.

Startup command actually executed:

```bash
python3 -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Observed startup:

```text
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Exact-source verification

The GitHub blobs at the teaching commit are:

```text
app.py          9069be8d83f2802fd94d3ca29cb073f45569c932
pyproject.toml  d8015570f097552799fc60358b3684beb56071ee
```

The files executed locally produced exactly those same Git blob hashes:

```text
app_blob=9069be8d83f2802fd94d3ca29cb073f45569c932
pyproject_blob=d8015570f097552799fc60358b3684beb56071ee
```

Therefore the executed Stage 1 source files were byte-for-byte identical to the specified commit.

A full GitHub clone was attempted but failed because the sandbox could not resolve `github.com`. Consequently, verification of the original repository checkout's HEAD and status is `UNVERIFIED`. Runtime verification used a temporary Git workspace reconstructed from the exact fetched blobs.

## 2. Exercise Markdown

### Exercise 1 — Start the transaction source

**Purpose:** Start the actual FastAPI application and establish the HTTP inspection point.

**Action:**

```bash
python3 -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Leave this terminal running.

**Inspect:** Look for successful application startup and the listening address.

**Learner question:** What Python object does `app:app` refer to in `app.py`?

**Observed result:**

```text
Application startup complete.
Uvicorn running on http://127.0.0.1:8000
```

**Expected learner-facing observation:** Uvicorn imports the `app` object defined by:

```python
app = FastAPI(title="Data Platform Lab Source")
```

**Result:** PASS.

### Exercise 2 — Retrieve the transactions and trace `TX001`

**Purpose:** Observe the synthetic data through its HTTP representation.

**Action, from another terminal:**

```bash
curl -sS -w '\nHTTP %{http_code}\n' \
  http://127.0.0.1:8000/transactions
```

**Prediction:** Before running it, predict how many transaction objects will be returned and what `TX001.amount_cents` will be.

**Observed result:**

```json
[{"transaction_id":"TX001","amount_cents":1299,"currency":"USD"},{"transaction_id":"TX002","amount_cents":2500,"currency":"USD"},{"transaction_id":"TX003","amount_cents":875,"currency":"USD"},{"transaction_id":"TX004","amount_cents":4200,"currency":"USD"}]
HTTP 200
```

Optional focused inspection without requiring `jq`:

```bash
curl -sS http://127.0.0.1:8000/transactions |
python3 -c 'import json,sys; xs=json.load(sys.stdin); print(next(x for x in xs if x["transaction_id"]=="TX001"))'
```

Observed:

```text
{'transaction_id': 'TX001', 'amount_cents': 1299, 'currency': 'USD'}
```

**Expected learner-facing observation:** `TX001` exists as a `Transaction` object in `TRANSACTIONS` and is serialized to JSON by the GET endpoint.

**Result:** PASS.

### Exercise 3 — Submit one valid transaction

**Purpose:** Observe Pydantic-backed request validation when the payload satisfies the contract.

**Action:**

```bash
curl -sS -w '\nHTTP %{http_code}\n' \
  -H 'Content-Type: application/json' \
  -d '{"transaction_id":"TX999","amount_cents":1234,"currency":"USD"}' \
  http://127.0.0.1:8000/transactions/validate
```

**Prediction:** Will the endpoint return the supplied transaction or add it to the four stored transactions?

**Observed result:**

```json
{"transaction_id":"TX999","amount_cents":1234,"currency":"USD"}
HTTP 200
```

**Expected learner-facing observation:** The endpoint validates and returns the supplied transaction. It does not append it to `TRANSACTIONS`; the implementation simply returns its `transaction` argument.

**Result:** PASS.

### Exercise 4 — Break the contract deliberately

**Purpose:** Observe one existing Pydantic constraint failing.

The implementation declares:

```python
amount_cents: int = Field(gt=0)
```

**Prediction before running:** What HTTP status do you expect when `amount_cents` is exactly `0`?

**Action:**

```bash
curl -sS -w '\nHTTP %{http_code}\n' \
  -H 'Content-Type: application/json' \
  -d '{"transaction_id":"TX999","amount_cents":0,"currency":"USD"}' \
  http://127.0.0.1:8000/transactions/validate
```

**Observed result:**

```json
{"detail":[{"type":"greater_than","loc":["body","amount_cents"],"msg":"Input should be greater than 0","input":0,"ctx":{"gt":0}}]}
HTTP 422
```

**Expected learner-facing observation:** The request does not reach the endpoint as a valid `Transaction`; request validation rejects `amount_cents=0`.

The exact error-body wording is version-sensitive. Teach the observed `422` and connection to `gt=0`; do not require learners on different Pydantic/FastAPI versions to reproduce this JSON byte-for-byte.

**Result:** PASS.

### Exercise 5 — Connect code constraints to OpenAPI metadata

**Purpose:** See that the model contract also describes the HTTP API.

**Action:**

```bash
curl -sS http://127.0.0.1:8000/openapi.json |
python3 -c 'import json,sys; d=json.load(sys.stdin); print(json.dumps(d["components"]["schemas"]["Transaction"], indent=2, sort_keys=True))'
```

**Inspect:** Compare these three declarations in `app.py` with their OpenAPI representation:

```python
transaction_id: str = Field(pattern=r"^TX\d{3}$")
amount_cents: int = Field(gt=0)
currency: Literal["USD"] = "USD"
```

**Observed schema:**

```json
{
  "properties": {
    "amount_cents": {
      "exclusiveMinimum": 0.0,
      "title": "Amount Cents",
      "type": "integer"
    },
    "currency": {
      "const": "USD",
      "default": "USD",
      "title": "Currency",
      "type": "string"
    },
    "transaction_id": {
      "pattern": "^TX\\d{3}$",
      "title": "Transaction Id",
      "type": "string"
    }
  },
  "required": [
    "transaction_id",
    "amount_cents"
  ],
  "title": "Transaction",
  "type": "object"
}
```

**Learner questions:**

- Where did `exclusiveMinimum: 0.0` originate?
- Where did the transaction-ID regex originate?
- Why is `currency` absent from `required`?

**Expected learner-facing observation:** The same Pydantic model controls validation and contributes schema metadata. In this tested version, `gt=0` becomes `exclusiveMinimum`, the regex becomes `pattern`, and the defaulted USD field is not required.

Also inspect the implementation directly:

```bash
sed -n '1,30p' app.py
```

Then connect:

```python
@app.get("/transactions", response_model=list[Transaction])
```

to the array of `Transaction` objects returned by GET, and:

```python
def validate_transaction(transaction: Transaction) -> Transaction:
    return transaction
```

to the successful POST and validation failure.

**Result:** PASS.

### Exercise 6 — Make one tiny reversible change

**Purpose:** Demonstrate that the learner can predict a code-to-HTTP behavior change without altering the validation contract.

First stop the running Uvicorn process.

Change only:

```python
Transaction(transaction_id="TX001", amount_cents=1299),
```

to:

```python
Transaction(transaction_id="TX001", amount_cents=1300),
```

One exact shell method used during verification was:

```bash
python3 - <<'PY'
from pathlib import Path
p = Path("app.py")
s = p.read_text()
old = 'Transaction(transaction_id="TX001", amount_cents=1299)'
new = 'Transaction(transaction_id="TX001", amount_cents=1300)'
assert s.count(old) == 1
p.write_text(s.replace(old, new))
PY
```

Inspect:

```bash
git diff -- app.py
```

Observed diff:

```diff
-    Transaction(transaction_id="TX001", amount_cents=1299),
+    Transaction(transaction_id="TX001", amount_cents=1300),
```

**Prediction before restarting:** What should the `TX001` object returned by `GET /transactions` contain now? Should any other transaction change?

Restart:

```bash
python3 -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Then:

```bash
curl -sS -w '\nHTTP %{http_code}\n' \
  http://127.0.0.1:8000/transactions
```

**Observed result:**

```json
[{"transaction_id":"TX001","amount_cents":1300,"currency":"USD"},{"transaction_id":"TX002","amount_cents":2500,"currency":"USD"},{"transaction_id":"TX003","amount_cents":875,"currency":"USD"},{"transaction_id":"TX004","amount_cents":4200,"currency":"USD"}]
HTTP 200
```

Revert:

```bash
git restore -- app.py
```

Verify:

```bash
git diff -- app.py
git status --short
```

Then restart and inspect `TX001` again.

Observed after revert:

```text
{'transaction_id': 'TX001', 'amount_cents': 1299, 'currency': 'USD'}
```

Exact file proof:

```text
app.py after revert:
9069be8d83f2802fd94d3ca29cb073f45569c932
```

That equals the GitHub blob at commit `7cb67a8ad96fcf69a358e83f20e41d51f95de43c`.

**Result:** PASS for the reversible source modification and restoration.

## 3. Verification log

| Check | Exact primary action | Observed | Result |
|---|---|---|---|
| Startup | `python3 -m uvicorn app:app --host 127.0.0.1 --port 8000` | Application startup complete | PASS |
| GET transactions | `curl ... /transactions` | HTTP 200, four records | PASS |
| Locate `TX001` | inspect GET result | `TX001`, `1299`, `USD` | PASS |
| Valid POST | POST `TX999`, 1234, USD | HTTP 200; payload returned | PASS |
| Invalid POST | POST `amount_cents: 0` | HTTP 422 | PASS |
| OpenAPI | `curl ... /openapi.json` | pattern, exclusive minimum, USD constraint visible | PASS |
| Code connection | `sed -n '1,30p' app.py` | model/routes correspond to runtime behavior | PASS |
| Reversible change | change only 1299→1300 | GET shows 1300 | PASS |
| Revert | `git restore -- app.py` | GET returns 1299; blob SHA restored | PASS |
| Original GitHub checkout status | full clone/check status | sandbox DNS prevented clone | `UNVERIFIED` |

## 4. Deliberate failure result

Failure selected:

```json
{
  "transaction_id": "TX999",
  "amount_cents": 0,
  "currency": "USD"
}
```

Relevant implementation constraint:

```python
amount_cents: int = Field(gt=0)
```

Observed:

```text
HTTP 422
```

Observed evidence:

```json
{
  "type": "greater_than",
  "loc": ["body", "amount_cents"],
  "msg": "Input should be greater than 0",
  "input": 0,
  "ctx": {"gt": 0}
}
```

This is a good failure exercise because it exposes exactly one existing contract rule without expanding into exhaustive validation testing.

## 5. Reversible-change result and proof of revert

Only this synthetic value was changed:

```diff
-Transaction(transaction_id="TX001", amount_cents=1299)
+Transaction(transaction_id="TX001", amount_cents=1300)
```

Predicted HTTP effect: only `TX001.amount_cents` changes from `1299` to `1300`.

Observed HTTP effect:

```json
{"transaction_id":"TX001","amount_cents":1300,"currency":"USD"}
```

After `git restore -- app.py`, the runtime response returned to:

```json
{"transaction_id":"TX001","amount_cents":1299,"currency":"USD"}
```

Final local verification:

```text
git status --porcelain=v1
<no output>

app.py:
9069be8d83f2802fd94d3ca29cb073f45569c932

pyproject.toml:
d8015570f097552799fc60358b3684beb56071ee
```

Both hashes exactly match the files fetched from the specified GitHub commit.

Running Python generated `__pycache__/` in the reconstructed workspace. It was removed before the final local status check. This temporary workspace did not contain the complete original repository's ignore configuration.

## 6. Prerequisites

Learner needs:

- the repository checked out at commit `7cb67a8ad96fcf69a358e83f20e41d51f95de43c`;
- Python 3.11 or later;
- FastAPI;
- Uvicorn;
- `curl`;
- two terminals, or equivalent ability to leave Uvicorn running while issuing requests.

`jq` is unnecessary.

For JSON-focused inspection, Python's standard library is already available because Python itself is a project prerequisite.

## 7. Broken, ambiguous, or version-sensitive steps

### Dependency installation

`UNVERIFIED`. The sandbox could not access GitHub or external package indexes. No fresh install from `pyproject.toml` was executed.

Do not claim a specific fresh-install command was tested here.

### Original repository status

`UNVERIFIED`. A real clone failed with:

```text
fatal: unable to access 'https://github.com/halkypi/data-platform-lab.git/':
Could not resolve host: github.com
```

The source files themselves were verified against their exact GitHub blob SHAs and executed successfully, but this is not equivalent to running `git status` in a genuine checkout of the original repository.

### Validation-body formatting

Version-sensitive. On FastAPI 0.128.2 / Pydantic 2.13.4, `amount_cents=0` produced:

```text
type="greater_than"
msg="Input should be greater than 0"
```

Do not make that exact body a learner success criterion across arbitrary dependency versions.

### OpenAPI representation

Version-sensitive. This environment emitted:

```json
"exclusiveMinimum": 0.0
```

and:

```json
"const": "USD"
```

Other supported dependency versions may serialize equivalent schema constraints differently.

## 8. Recommended corrections or simplifications

1. Keep the failure to `amount_cents=0`. It directly maps `Field(gt=0)` to one observed 422 and avoids needless validation coverage.
2. Do not require `jq`. Show the raw `curl` response first. Use the Python standard library only when focused schema/TX001 extraction materially improves readability.
3. Use Uvicorn without `--reload`. For the modification exercise, explicitly stop and restart the server after changing `app.py`. This avoids introducing reload mechanics as an incidental new concept.
4. Teach OpenAPI semantically, not byte-for-byte. Ask learners to find the transaction-ID pattern, positive-amount constraint, and USD restriction. Do not require exact generated schema syntax across unpinned versions.
5. Keep valid POST separate from persistence. A useful question is whether posting `TX999` adds it to `TRANSACTIONS`. The answer follows directly from the endpoint implementation and helps distinguish validation from storage without teaching later architecture.
6. For the real learner walkthrough, end the modification exercise with both `git diff` and `git status --short`. The final teaching walkthrough should verify this in an actual repository checkout.

No Stage 1 implementation defect was found.

## 9. UNVERIFIED items

- `UNVERIFIED` — fresh dependency installation: external network/package access was unavailable.
- `UNVERIFIED` — original checkout HEAD/status after exercise: the sandbox could not clone the GitHub repository. Exact source restoration was instead proven by matching the GitHub blob hashes for both Stage 1 implementation files.

Everything else required by the TA assignment—startup, GET, `TX001`, valid POST, deliberate invalid POST, HTTP status, OpenAPI inspection, code/runtime connection, reversible `TX001.amount_cents` change, observation, and source-file revert—was executed and verified.

## TA recommendation to Teaching Planner

The exercise set is technically viable. Preserve the `UNVERIFIED` checkout/install qualifications, avoid exact error-body/schema-format assertions, and send the eventual draft through the combined learner walkthrough in a real repository checkout before finalizing the notebook.
