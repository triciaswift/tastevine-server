from rest_framework import serializers
from tastevineapi.models import Category

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for ingredient"""

    class Meta:
        model = Category
        fields = ('label',)
