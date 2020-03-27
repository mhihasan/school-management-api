EXCLUDED_PERMISSION_MODELS = [
    "logentry",
    "group",
    "contenttype",
    "session",
    "counter",
    "servicebillitem",
    "invoiceitem",
]

# Accounting related constant

# Debit Balance : 0, 1, 8, 9, 10, 11
# Credit Balance: 2, 3, 4, 5, 6, 7
ACCOUNT_GROUP_TYPE = (
    # Balance sheet type
    (0, "Current Assets"),
    (1, "Non-current Assets"),
    (2, "Current Liabilities"),
    (3, "Non-current Liabilities"),
    (4, "Equity"),
    # Income statement type
    (5, "Revenue"),
    (6, "Other Operating Income"),
    (7, "Non-operating Income"),
    (8, "Cost of Sales"),
    (9, "Indirect Overhead"),
    (10, "Non-operating Expenses"),
    (11, "Income Taxes"),
    # this will no affect income statement or balance sheet
    (12, "Gain/Losses"),
)

TYPE = (
    (0, "Cash & Cash Equivalents"),
    (1, "Account Receivable"),
    (2, "Inventory"),
    (3, "Other Current Assets"),
)

ACCOUNT_TYPE = ((0, "Balance Sheet"), (1, "Income Statement"), (2, "Retained Earnings"))

DOC_TYPE = ((0, "Invoice"), (1, "Billing"), (2, "Credit Note"), (3, "Debit Note"))

INVOICE_TYPE = ((0, "Code wise"), (1, "Item wise"))

INVOICE_STATUS = ((0, "Due"), (1, "Paid"), (2, "Refund"))

PAYMENT_TYPE = ((0, "Collection"), (1, "Payment"))

ENTRY_STATUS = ((0, "Pending"), (1, "Posted"), (2, "Deleted"))


PAYMENT_MODE = ((0, "Cash"), (1, "bKash"), (2, "CreditCard"), (3, "Cheque"))

DEBIT = 1
CREDIT = -1

BALANCE_SHEET = 0
INCOME_STATEMENT = 1

CASH_AND_CASH_EQUIVALENT = 1
ACCOUNT_RECEIVABLE = 2
ACCOUNT_PAYABLE = 8

# Code
SALES_RETURNS_CODE = 400999
