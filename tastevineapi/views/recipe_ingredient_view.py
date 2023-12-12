from rest_framework import serializers
from tastevineapi.models import RecipeIngredient
from .ingredient_view import IngredientSerializer

class RecipeIngredientSerializer(serializers.ModelSerializer):
    """JSON serializer for ingredient"""
    measurement = serializers.SerializerMethodField()
    ingredient = IngredientSerializer(many=False)

    def get_measurement(self, obj):
        # obj.ingredient retrieves the related Ingredient object associated with the foreign key on RecipeIngredient
        ingredient = obj.ingredient
        return f'{obj.quantity} {obj.unit} {ingredient.name}'

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'ingredient', 'quantity', 'unit', 'measurement',)