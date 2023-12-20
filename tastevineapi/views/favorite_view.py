from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from tastevineapi.models import Favorite, Recipe
from .category_view import CategorySerializer
from .recipe_view import RecipeUserSerializer

class FavoriteView(ViewSet):
    """Favorite view set"""

    def list(self, request):
        """Handle GET requests for all favorites

        Returns:
            Response -- JSON serialized array
        """
        try:
            favorites = Favorite.objects.filter(user=request.auth.user)
            serializer = FavoriteSerializer(favorites, many=True, context= {"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        # Get an object instance of a recipe
        recipe = Recipe.objects.get(pk=request.data["recipeId"])

        # Create a favorite object and assign it property values
        favorite = Favorite()
        favorite.recipe = recipe
        favorite.user = request.auth.user

        try:
            favorite.save()
            serializer = FavoriteSerializer(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single favorite

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            favorite = Favorite.objects.get(pk=pk)
            favorite.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Favorite.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RecipeFavoriteSerializer(serializers.ModelSerializer):
    """JSON serializer for recipes"""
    categories = CategorySerializer(many=True)
    author = RecipeUserSerializer(many=False)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'author', 'image', 'categories',)

        
class FavoriteSerializer(serializers.ModelSerializer):
    """JSON serializer for favorites"""
    recipe = RecipeFavoriteSerializer(many=False)

    class Meta:
        model = Favorite
        fields = ('id', 'recipe')
