from drf_yasg import openapi

account_group = openapi.Parameter(
    "account_group",
    openapi.IN_QUERY,
    description="revenue, expense etc",
    format="revenue",
    type=openapi.TYPE_STRING,
)
