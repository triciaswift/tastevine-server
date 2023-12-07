from rest_framework import serializers
from tastevineapi.models import RecipeIngredient
from .ingredient_view import IngredientSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """JSON serializer for ingredient"""
    measurement = serializers.SerializerMethodField()

    def get_measurement(self, obj):
        ingredient = obj.ingredient
        return f'{obj.quantity} {obj.unit} {ingredient.name}'

    class Meta:
        model = RecipeIngredient
        fields = ('measurement',)