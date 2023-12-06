from rest_framework import serializers
from tastevineapi.models import Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    """JSON serializer for ingredient"""

    class Meta:
        model = Ingredient
        fields = ('name',)
