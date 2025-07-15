from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

    def paginate_queryset(self, queryset, request, view=None):
        if not queryset.exists():
            return None
        return super().paginate_queryset(queryset, request, view)
