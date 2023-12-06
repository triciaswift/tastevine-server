from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.db.models.functions import Lower
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
            ingredients = Ingredient.objects.all().order_by(Lower("name"))
            serializer = IngredientSerializer(ingredients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        ingredient = Ingredient()
        ingredient.name = request.data["name"]

        try:
            ingredient.save()
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)