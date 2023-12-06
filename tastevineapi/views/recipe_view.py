from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from tastevineapi.models import Recipe
from .category_view import CategorySerializer
from .ingredient_view import IngredientSerializer

class RecipeView(ViewSet):
    """Recipe view set"""

    def list(self, request):
        """Handle GET requests for all recipes

        Returns:
            Response -- JSON serialized array
        """
        try:
            recipes = Recipe.objects.all()
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class RecipeSerializer(serializers.ModelSerializer):
    """JSON serializer for recipe"""
    ingredients = IngredientSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'author', 'publication_date', 'image', 'instructions', 'ingredients', 'categories',)
