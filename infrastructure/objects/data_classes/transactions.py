from dataclasses import dataclass

@dataclass
class Transactions:
    date_time: str
    amount: str
    transaction_type: str