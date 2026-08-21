from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field


class Transaction(BaseModel):
    transaction_id: str = Field(pattern=r"^TX\d{3}$")
    amount_cents: int = Field(gt=0)
    currency: Literal["USD"] = "USD"


TRANSACTIONS = [
    Transaction(transaction_id="TX001", amount_cents=1299),
    Transaction(transaction_id="TX002", amount_cents=2500),
    Transaction(transaction_id="TX003", amount_cents=875),
    Transaction(transaction_id="TX004", amount_cents=4200),
]

app = FastAPI(title="Data Platform Lab Source")


@app.get("/transactions", response_model=list[Transaction])
def list_transactions() -> list[Transaction]:
    return TRANSACTIONS


@app.post("/transactions/validate", response_model=Transaction)
def validate_transaction(transaction: Transaction) -> Transaction:
    return transaction
