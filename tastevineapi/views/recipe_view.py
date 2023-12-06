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
            Response -- JSON serialized list of recipes
        """

        owner_only = self.request.query_params.get("owner", None)

        try:
            recipes = Recipe.objects.all()

            if owner_only is not None and owner_only == 'current':
                recipes = recipes.filter(author=request.auth.user)
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def retrieve(self, request, pk=None):
        """Handle GET requests for single recipe

        Returns:
            Response -- JSON serialized recipe record
        """
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class RecipeSerializer(serializers.ModelSerializer):
    """JSON serializer for recipe"""
    ingredients = IngredientSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'author', 'publication_date', 'image', 'instructions', 'ingredients', 'categories',)
