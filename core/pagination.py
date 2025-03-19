from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomPagination(LimitOffsetPagination):
    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "example": 123,
                },
                "next": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": f"http://api.example.org/accounts/?{self.offset_query_param}=400&{self.limit_query_param}=100",
                },
                "previous": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": f"http://api.example.org/accounts/?{self.offset_query_param}=200&{self.limit_query_param}=100",
                },
                "data": schema,
            },
        }

    def get_limit(self, request):
        if self.request.query_params.get("limit") == "all":
            return float("inf")
        return super().get_limit(request)

    def get_count(self, queryset):
        count = super().get_count(queryset)
        if self.limit == float("inf"):
            self.limit = count
        return count

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "data": data,
            }
        )
