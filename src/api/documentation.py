from drf_yasg import openapi


jwt_header = openapi.Parameter(
    "Authorization",
    openapi.IN_HEADER,
    description="jwt token for authentication",
    format="jwt <token>",
    type=openapi.TYPE_STRING,
    required=True,
)

from_date_param = openapi.Parameter(
    "from_date",
    openapi.IN_QUERY,
    format="%d-%m-%Y",
    description="return summary from this date",
    type=openapi.TYPE_STRING,
    required=True,
)
end_date_param = openapi.Parameter(
    "end_date",
    openapi.IN_QUERY,
    format="%d-%m-%Y",
    description="return summary till this date",
    type=openapi.TYPE_STRING,
    required=True,
)
date_param = openapi.Parameter(
    "date",
    openapi.IN_QUERY,
    format="%d-%m-%Y",
    description="return alarms on this date",
    type=openapi.TYPE_STRING,
    required=True,
)
