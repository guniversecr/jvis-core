"""Core views."""

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Item
from core.serializers import ItemSerializer


@api_view(["GET"])
def health_check(request: Request) -> Response:
    """Health check endpoint: GET /api/health/."""
    return Response({"status": "healthy", "service": "api"})


class ItemViewSet(ModelViewSet):
    """CRUD ViewSet for Item model."""

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
