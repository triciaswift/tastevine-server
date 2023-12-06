from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from tastevineapi.models import Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    """JSON serializer for ingredient"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name',)


class IngredientView(ViewSet):
    """Ingredient view set"""

    def list(self, request):
        """Handle GET requests for all ingredients

        Returns:
            Response -- JSON serialized list of ingredients
        """
        try:
            ingredients = Ingredient.objects.all()
            serializer = IngredientSerializer(ingredients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)