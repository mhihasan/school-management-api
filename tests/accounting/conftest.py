from src.accounting.models import Account, StudentFee


def account_object(org_id):
    return Account.objects.create(
        name="a",
        group_id=15,
        balance_type=1,
        account_type=1,
        gl_code="xlg",
        organization_id=org_id,
    )


def studentfee_object(name, amount=6700):
    return StudentFee.objects.create(
        name=name,
        amount=amount
    )
