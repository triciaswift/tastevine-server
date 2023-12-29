from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from tastevineapi.models import GroceryCategory

class GroceryCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for grocery categories"""

    class Meta:
        model = GroceryCategory
        fields = ('id', 'category',)

class GroceryCategoryView(ViewSet):
    """Grocery Category view set"""

    def list(self, request):
        """Handle GET requests for all grocery categories

        Returns:
            Response -- JSON serialized list of grocery categories
        """
        try:
            categories = GroceryCategory.objects.all()
            serializer = GroceryCategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
