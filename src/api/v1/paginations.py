from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class LedgerPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("opening_balance", self.opening_balance),
                    ("closing_balance", self.closing_balance),
                    ("results", data),
                ]
            )
        )


class LimitOffsetUnlimitedDefaultPagination(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        try:
            limit = request.query_params[self.limit_query_param]
            return super().paginate_queryset(queryset, request, view)
        except KeyError:
            self.limit = 1000000000
            self.count = self.get_count(queryset)
            self.request = request
            self.offset = 0
            return list(queryset)
