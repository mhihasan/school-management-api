from src.accounting.models import Account


def account_object(org_id):
    return Account.objects.create(
        name="a",
        group_id=15,
        balance_type=1,
        account_type=1,
        gl_code="xlg",
        organization_id=org_id,
    )
