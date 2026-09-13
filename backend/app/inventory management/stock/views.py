from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from .models import Stock  # Adjust model name if different in your stock app
from .serializers import StockSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [AllowAny]