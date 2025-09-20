from rest_framework import generics, permissions

from nutriplan.models import Category
from nutriplan.serializers import CategorySerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
