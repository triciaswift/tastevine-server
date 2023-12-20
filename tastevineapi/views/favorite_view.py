from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from tastevineapi.models import Favorite, Recipe
from .category_view import CategorySerializer

class FavoriteView(ViewSet):
    """Favorite view set"""

    def list(self, request):
        """Handle GET requests for all favorites

        Returns:
            Response -- JSON serialized array
        """
        try:
            favorites = Favorite.objects.filter(user=request.auth.user)
            serializer = FavoriteSerializer(favorites, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
class RecipeFavoriteSerializer(serializers.ModelSerializer):
    """JSON serializer for recipes"""
    categories = CategorySerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'author', 'image', 'categories',)

        
class FavoriteSerializer(serializers.ModelSerializer):
    """JSON serializer for favorites"""
    recipe = RecipeFavoriteSerializer(many=False)

    class Meta:
        model = Favorite
        fields = ('id', 'recipe')
