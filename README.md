You should implement ability to create new wallets and provide transactions between them. Transactions are available only for wallets with the same currnecy( from RUB to RUB - ok, from RUB to USD - wrong, show exception for user. When user sends money from his wallet to his another wallet - no commission, and when he sends to wallet, related to another user - commission=10%


Wallet entity:
- name - unique random 8 symbols of latin alphabet and digits. Example: MO72RTX3
- type - 2 possible choices: Visa or Mastercard
- currency - 3 possible choices: USD, EUR, RUB
- balance - balance rounding up to 2 decimal places. Example: 1.38 - ok,1.377 - wrong
- created_on - datetime, when wallet was created
- modified_on - datetime, when wallet was modified

User can't create more than 5 wallets.

How to create wallets: 
POST /wallets
{
 "type": "visa",
 "currency": "RUB"
}
When user creates new wallet he gets default bonus from bank: if wallet currency USD or EUR - balance=3.00, if RUB - balance=100.00

Get all user's wallets:
GET /wallets
Example:
{
[
"id": "1",
"name": "ER15096L",
"type": "Visa",
"currency": "USD",
"balance": "1.87",
"created_on": ...,
"modified_on": ...
],
[
"id": "2",
"name": "VB07N96L",
"type": "Visa",
"currency": "RUB",
"balance": "1000.50",
"created_on": ...,
"modified_on": ...
]
}

GET /wallets/<name> - get wallet where name=<name>. Example - /wallets/VB07N96L
DELETE /wallets/<name> - delete wallet

You can't modified wallet's data, PUT and PATCH are not available.

Transactions entity:
- sender - wallet id
- receiver - wallet id
- transfer_amount of money that "sender" send to "receiver". Example - 5.00
- commission - 0.00 if no commision else transfer_amount * 0.10
- status - PAID if no problems else FAILED
- timestamp - datetime when transaction was created

POST /wallets/transactions/ - create new transaction. Example:
{
"sender": "VB07N96L"
"receiver": "MJYR096L",
"transfer_amount": "100.00"
}

GET /wallets/transactions/ - get all transactions for currnet user. Example:
{
[
"id": 1,
"sender": "VB07N96L",
"receiver": "MJYR096L",
"transfer_amount": "100.00",
"commision": "0.00",
"status": "PAID",
"timestamp": ...
],
...
}

GET /wallets/transactions/<transaction_id> - get transaction
GET /wallets/transactions/<wallet_name> - get all transactions where wallet was sender or receiver

Stack: Python, Django, DRF, Django ORM, PostgreSQL
