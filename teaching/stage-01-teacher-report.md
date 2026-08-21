# Teacher Report — Stage 1: Minimal Transaction HTTP Source

## Scope

This report teaches only the implementation at:

- Repository: `halkypi/data-platform-lab`
- Branch under inspection: `lab/stage-01-transaction-source`
- Commit: `7cb67a8ad96fcf69a358e83f20e41d51f95de43c`
- Commit message: `lab: add minimal transaction HTTP source`
- Implementation: [`app.py`](https://github.com/halkypi/data-platform-lab/blob/7cb67a8ad96fcf69a358e83f20e41d51f95de43c/app.py) and [`pyproject.toml`](https://github.com/halkypi/data-platform-lab/blob/7cb67a8ad96fcf69a358e83f20e41d51f95de43c/pyproject.toml)

The governing Teaching Planner prompt is [`prompts/teaching-planner.md`](https://github.com/halkypi/data-platform-lab/blob/bfb063c9ffda7c4962df3bc50c810bd34f0e6da7/prompts/teaching-planner.md) at commit `bfb063c9ffda7c4962df3bc50c810bd34f0e6da7`.

The explanation below distinguishes documented FastAPI/Pydantic behavior from local design choices in `app.py`.

## 1. Concepts worth teaching

### `Transaction` is the application/data contract

Stage 1 defines:

```python
class Transaction(BaseModel):
    transaction_id: str = Field(pattern=r"^TX\d{3}$")
    amount_cents: int = Field(gt=0)
    currency: Literal["USD"] = "USD"
```

Documented Pydantic behavior: models inherit from `BaseModel`; input is parsed and validated into model instances whose fields conform to the declared model definition and constraints.

Local design choices: the field names, `TX###` identifier shape, positive-only amount rule, use of cents, and USD-only currency are decisions made by this lab. They are not FastAPI or Pydantic requirements.

Primary source: <https://docs.pydantic.dev/latest/concepts/models/>

### Python `Transaction` objects are different from JSON transported over HTTP

`TX001` is created in Python as:

```python
Transaction(transaction_id="TX001", amount_cents=1299)
```

Because `currency` has a default, the resulting model has `currency="USD"`.

The object is an in-process Python model instance. Across HTTP, a client sees a JSON representation such as:

```json
{
  "transaction_id": "TX001",
  "amount_cents": 1299,
  "currency": "USD"
}
```

Pydantic provides model validation and serialization capabilities; FastAPI handles the HTTP request/response boundary.

Primary sources:

- <https://docs.pydantic.dev/latest/concepts/models/>
- <https://fastapi.tiangolo.com/tutorial/body/>

### FastAPI request-body validation

This parameter:

```python
transaction: Transaction
```

causes FastAPI to treat the request body as data for a Pydantic model. FastAPI documents that it reads JSON request data, validates/converts it using the declared model, and supplies the resulting model object to the path operation function.

For Stage 1, this means invalid transaction data should be rejected before the function body can use it as a valid `Transaction`.

Primary source: <https://fastapi.tiangolo.com/tutorial/body/>

### `response_model` declares the HTTP response contract

Stage 1 declares:

```python
@app.get("/transactions", response_model=list[Transaction])
```

and:

```python
@app.post("/transactions/validate", response_model=Transaction)
```

FastAPI documents that `response_model` is used for response validation/serialization, generated OpenAPI schema, and output filtering to the declared shape.

Primary source: <https://fastapi.tiangolo.com/tutorial/response-model/>

### Field constraints belong to the contract; their particular values are local design

The model uses three relevant constraint mechanisms:

```python
transaction_id: str = Field(pattern=r"^TX\d{3}$")
amount_cents: int = Field(gt=0)
currency: Literal["USD"] = "USD"
```

- `pattern` constrains the string with a regular expression.
- `gt=0` requires a value greater than zero.
- `Literal["USD"]` restricts the accepted literal value to `"USD"`.
- `= "USD"` provides the field default.

The framework provides these mechanisms. The exact pattern, threshold, currency, and default are local choices.

Primary sources:

- <https://docs.pydantic.dev/latest/concepts/fields/>
- <https://docs.pydantic.dev/latest/api/fields/>
- <https://docs.pydantic.dev/latest/api/standard_library_types/>

### `GET /transactions` is the inspectable source endpoint

The route returns the fixed in-memory list:

```python
TRANSACTIONS = [
    Transaction(transaction_id="TX001", amount_cents=1299),
    Transaction(transaction_id="TX002", amount_cents=2500),
    Transaction(transaction_id="TX003", amount_cents=875),
    Transaction(transaction_id="TX004", amount_cents=4200),
]
```

and:

```python
def list_transactions() -> list[Transaction]:
    return TRANSACTIONS
```

This is a local design choice. Stage 1 does not read from a file, database, queue, or external system.

### `POST /transactions/validate` is a validation echo, not persistence

The route is intentionally minimal:

```python
def validate_transaction(transaction: Transaction) -> Transaction:
    return transaction
```

It exposes request validation and response serialization with almost no unrelated application logic.

It does **not** add the supplied transaction to `TRANSACTIONS`, write a file, or persist anything.

That echo behavior is a local teaching design, not a prescribed FastAPI architecture.

### FastAPI/Pydantic expose schema through OpenAPI

Pydantic can generate JSON Schema from models. FastAPI incorporates model schemas into the application's generated OpenAPI description. FastAPI serves its OpenAPI schema at `/openapi.json` by default.

This gives the learner two views of the same contract:

```text
runtime contract -> validation of transaction data
schema contract  -> machine-readable description in OpenAPI
```

Primary sources:

- <https://docs.pydantic.dev/latest/concepts/json_schema/>
- <https://fastapi.tiangolo.com/tutorial/first-steps/>

## 2. Compact teaching Markdown

### The contract

`Transaction` is the boundary between incoming data and the Python object the application is prepared to work with.

For `TX001`, distinguish these two representations:

```text
Python process:
Transaction(transaction_id="TX001", amount_cents=1299, currency="USD")

HTTP JSON:
{"transaction_id":"TX001","amount_cents":1299,"currency":"USD"}
```

The first is an in-process Python model instance. The second is data represented as JSON across HTTP.

Pydantic owns model parsing, validation, field constraints, serialization support, and JSON Schema generation. The particular transaction fields and rules are choices made in `app.py`.

### Incoming request

For:

```python
def validate_transaction(transaction: Transaction) -> Transaction:
```

FastAPI treats `transaction` as a Pydantic-model request body. Before the function runs with a valid model, FastAPI reads the JSON request and validates it against `Transaction`.

A useful mental path is:

```text
HTTP JSON
   ↓
FastAPI request handling
   ↓
Pydantic validation
   ↓
Transaction Python object
```

### Outgoing response

For:

```python
response_model=Transaction
```

or:

```python
response_model=list[Transaction]
```

FastAPI has an explicit declaration of what the HTTP response is supposed to look like. It uses that contract when validating/serializing output and documenting the endpoint through OpenAPI.

The reverse path is:

```text
Transaction Python object
   ↓
FastAPI response_model
   ↓
JSON response
   ↓
HTTP client
```

### Why `/transactions/validate` exists

The endpoint does almost nothing on purpose:

```python
return transaction
```

Its teaching value is the exposed boundary. A valid request reaches the function as a `Transaction`; invalid request data is rejected by the declared contract. The echo then makes the resulting representation directly inspectable.

### Schema

The same `Transaction` definition supports both runtime validation and machine-readable schema generation:

```text
Transaction model
   ├─ runtime validation
   └─ JSON Schema → FastAPI OpenAPI
```

The constraints are therefore not only hidden runtime code; the framework can expose contract metadata to clients and tooling.

## 3. Key distinctions the learner should be able to explain

- **Python object vs JSON:** `Transaction(...)` is an in-process Python model object; the HTTP client receives JSON.
- **Application contract vs transport:** Pydantic describes valid transaction data; HTTP/JSON moves a representation of that data.
- **Framework behavior vs local business rule:** Pydantic provides the validation mechanisms; `TX###`, positive amounts, and USD-only currency are local choices.
- **Request validation vs endpoint logic:** FastAPI/Pydantic validate the request; the function contains no manual validation code.
- **Validation vs persistence:** `/transactions/validate` proves that input satisfies the contract; it does not save it.
- **Return value vs response contract:** the Python function returns objects; `response_model` explicitly declares the HTTP response model FastAPI should use.
- **Data instance vs schema:** `TX001` is one transaction; the `Transaction` JSON Schema describes allowed transaction structure.
- **Default vs allowed value:** `"USD"` is both the only allowed literal and the default when the field is omitted. Those are separate concepts.

## 4. Prediction questions

Use these before observation where practical.

1. `TX001` was constructed without a `currency` argument. What value should its `currency` attribute have?
2. Before calling `GET /transactions`, will the response contain Python syntax such as `Transaction(...)`, or JSON objects?
3. What should happen if `POST /transactions/validate` receives `transaction_id: "TX01"`?
4. What should happen for `"amount_cents": 0`?
5. What should happen for `"amount_cents": -1`?
6. What should happen for `"currency": "EUR"`?
7. If `currency` is omitted from an otherwise valid POST, predict whether the request passes and what currency appears in the response.
8. Does a successful POST add the transaction to the result of a later GET?
9. Before inspecting `/openapi.json`, predict which constraints will appear as schema metadata: the transaction ID pattern, positive amount requirement, USD restriction, and USD default.
10. Where is `TX001` immediately before serialization for `GET /transactions`: in a file, database, JSON text, or as an object in Python memory?

## 5. Authoritative sources

### FastAPI — Request Body

<https://fastapi.tiangolo.com/tutorial/body/>

Supports: Pydantic models as request bodies; JSON reading; conversion and validation; model objects supplied to path operation functions; generated schema integration.

### FastAPI — Response Model

<https://fastapi.tiangolo.com/tutorial/response-model/>

Supports: response validation, serialization, output filtering, and response schema generation in OpenAPI.

### FastAPI — First Steps / OpenAPI

<https://fastapi.tiangolo.com/tutorial/first-steps/>

Supports: generated OpenAPI and the default `/openapi.json` inspection path.

### Pydantic — Models

<https://docs.pydantic.dev/latest/concepts/models/>

Supports: `BaseModel`, model instantiation/validation, Python model instances, serialization, and model schema concepts.

### Pydantic — Fields

<https://docs.pydantic.dev/latest/concepts/fields/>

Supports: field metadata, constraints, and defaults.

### Pydantic — Field API

<https://docs.pydantic.dev/latest/api/fields/>

Supports specifically: `pattern` regular-expression constraints and `gt` numeric constraints.

### Pydantic — Standard Library Types

<https://docs.pydantic.dev/latest/api/standard_library_types/>

Supports: `typing.Literal` constraining input to explicitly allowed literal values.

### Pydantic — JSON Schema

<https://docs.pydantic.dev/latest/concepts/json_schema/>

Supports: model JSON Schema generation and the distinction between a data instance and a schema describing the model.

### Uvicorn — Settings

<https://www.uvicorn.org/settings/>

Use only if the notebook needs to explain startup such as `uvicorn app:app`. Uvicorn documents the application import string as `<module>:<attribute>` and its host/port settings.

## 6. Claims or areas to avoid

- Do not call `TRANSACTIONS` a database, persisted dataset, durable store, or repository. It is an in-memory Python list.
- Do not imply `POST /transactions/validate` creates, inserts, or saves transactions. It returns the validated object unchanged.
- Do not say FastAPI requires transaction IDs to look like `TX001`; that is a local constraint.
- Do not say Pydantic requires positive monetary amounts or USD; both are local design choices.
- Do not generalize `amount_cents > 0` into a complete monetary model. Stage 1 says nothing about refunds, zero-value transactions, decimals, precision policy, or accounting semantics.
- Do not describe the return annotation `-> Transaction` alone as the HTTP response contract. The implementation deliberately also declares `response_model=Transaction`; keep Python typing and FastAPI's response-model behavior conceptually distinct.
- Do not claim the contract rejects unknown JSON properties. `Transaction` does not configure `extra="forbid"`; extra-field behavior is therefore not a custom rule in this implementation.
- Do not teach strict typing. This model does not enable strict mode.
- Do not introduce persistence, NiFi, Parquet, queues, ingestion, databases, or downstream architecture. Those belong to later stages.
- Do not claim exact HTTP validation error bodies from documentation alone. The TA should observe those against the actual installed dependency versions.

## 7. Version-sensitive behavior for TA verification

`pyproject.toml` specifies unpinned `fastapi` and `uvicorn` dependencies and this exact Stage 1 commit does not pin the installed FastAPI/Pydantic/Uvicorn versions. Exact generated output should therefore be verified empirically.

The TA should verify rather than assume:

1. the installed FastAPI, Pydantic, and Uvicorn versions;
2. the actual HTTP status and exact JSON error structure for each deliberate validation failure;
3. whether an omitted `currency` is returned as `"USD"` exactly as predicted;
4. the exact generated `Transaction` representation in `/openapi.json`, including how `pattern`, the positive numeric bound, `Literal["USD"]`, required fields, and the USD default are represented;
5. the exact GET and POST response JSON;
6. any coercion behavior used in exercises—for example whether a JSON string such as `"1299"` is accepted for an integer field—before putting that behavior into learner-facing material;
7. any test involving extra fields, because the model does not configure an explicit extra-field policy.

No broader research is required for the central Stage 1 teaching claims above.
