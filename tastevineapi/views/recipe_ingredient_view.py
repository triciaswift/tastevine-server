from rest_framework import serializers
from tastevineapi.models import RecipeIngredient
from .ingredient_view import IngredientSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """JSON serializer for ingredient"""
    ingredient = IngredientSerializer(many=False)

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'quantity', 'unit',)