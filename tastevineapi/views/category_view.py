from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from tastevineapi.models import Category

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for ingredient"""

    class Meta:
        model = Category
        fields = ('label',)

class CategoryView(ViewSet):
    """Category view set"""

    def list(self, request):
        """Handle GET requests for all categories

        Returns:
            Response -- JSON serialized list of categories
        """
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)