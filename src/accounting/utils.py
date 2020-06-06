from datetime import datetime

from django.db.models import Sum, F

from src.accounting.models import Transaction, Journal, Account

OTHER_CURRENT_LIABILITIES = 10
OTHER_CURRENT_ASSETS = 4


class Balance:
    """
    This course will calculate the balance of a given category or group.
    """

    def __init__(self, organization_id, category=None, group=None):
        if category and group:
            raise Exception("You must enter either category or group")
        if category is None and group is None:
            raise Exception("You must enter either category or group")

        self.organization_id = organization_id
        self.category = category
        self.group = group

    def balance(self, start_date=None, end_date=None):
        d = {
            "journal__organization_id": self.organization_id,
            "journal__is_posted": True,
        }

        if self.group:
            d.update({"account__group_id": self.group})
        else:
            d.update({"account__group__category": self.category})

        if start_date and end_date:
            trans = Transaction.objects.filter(
                journal__posted_date__gte=start_date,
                journal__posted_date__lte=end_date,
                **d
            )
        else:
            start_date = datetime.now()
            trans = Transaction.objects.filter(
                journal__posted_date__lte=start_date, **d
            )

        trans = trans.values(
            "account__code", "account__name", "account__balance_type"
        ).annotate(bal=Sum(F("debit") - F("credit")))

        balance = 0
        for i in trans:
            print(
                "a",
                i["account__code"],
                i["account__name"],
                i["bal"] * i["account__balance_type"],
            )
            balance += i["bal"] * i["account__balance_type"]
        return balance


class Validation:
    def __init__(self):
        self.validate_accounts()
        self.validate_transactions()
        self.validate_journals()

    def _invalidated_debit(self, account):
        return (
            account.group.category in [0, 1, 8, 9, 10, 11]
            and account.balance_type == -1
        )

    def _invalidated_credit(self, account):
        return (
            account.group.category in [2, 3, 4, 5, 6, 7] and account.balance_type == 1
        )

    def validate_accounts(self):
        accounts = Account.objects.all()
        valid = True
        for account in accounts:
            if account.code == 400999 or account.code == 400998:
                continue
            if self._invalidated_debit(account):
                raise ValueError(
                    "This ({}) should be debit type balance".format(account.id)
                )
            elif self._invalidated_credit(account):
                raise ValueError(
                    "This ({})should be credit type balance".format(account.id)
                )
        if valid:
            print("All Accounts are validated")

    def validate_journals(self):
        journals = Journal.objects.all()
        valid = True
        for j in journals:
            if not j.validate():
                valid = False
                # j.delete()
                print("Journal id {} is not validated".format(j.id))
        if valid:
            print("All Journals are validated")

    def validate_transactions(self):
        transactions = Transaction.objects.all()
        valid = True
        for t in transactions:
            if not t.account.is_active:
                # t.delete()
                valid = False
                print(
                    "Transaction id {} of Journal id {} is not valid".format(
                        t.id, t.journal.id
                    )
                )

        if valid:
            print("All Transactions are validated")


def create_initial_accounts(organization_id):
    c = {"organization_id": organization_id}
    Account.objects.get_or_create(
        code=111200,
        name="VAT on Sale",
        group_id=OTHER_CURRENT_LIABILITIES,
        balance_type=-1,
        account_type=0,
        **c
    )
    Account.objects.get_or_create(
        code=101300,
        name="VAT on Purchase",
        group_id=OTHER_CURRENT_ASSETS,
        balance_type=1,
        account_type=0,
        **c
    )
    Account.objects.get_or_create(
        code=100100,
        name="Sales Tax",
        group_id=OTHER_CURRENT_LIABILITIES,
        balance_type=-1,
        account_type=0,
        **c
    )
    Account.objects.get_or_create(
        code=200100,
        name="Purchase Tax",
        group_id=OTHER_CURRENT_ASSETS,
        balance_type=1,
        account_type=0,
        **c
    )
    Account.objects.get_or_create(
        code=400999,
        name="Sales Returns and Allowance",
        group_id=15,
        balance_type=1,
        account_type=1,
        **c
    )
    Account.objects.get_or_create(
        code=400998,
        name="Sales Discount",
        group_id=15,
        balance_type=1,
        account_type=1,
        **c
    )


def validate_accounting_equation(transactions):
    if not transactions:
        return False

    debit = credit = 0
    for t in transactions:
        debit += t["debit"]
        credit += t["credit"]

    if debit <= 0 or credit <= 0:
        return False

    if debit != credit:
        return False

    return True


def validate_debit_credit(transactions):
    if not transactions:
        return False

    debit = credit = 0
    for t in transactions:
        debit += t.debit
        credit += t.credit

    if debit <= 0 or credit <= 0:
        return False

    if debit != credit:
        return False

    return True
