from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from tastevineapi.models import GroceryListItem, GroceryList, Ingredient
from .ingredient_view import IngredientSerializer

class GroceryListItemSerializer(serializers.ModelSerializer):
    """JSON serializer for grocery list items"""
    ingredient = IngredientSerializer(many=False)

    class Meta:
        model = GroceryListItem
        fields = ( 'id', 'ingredient', 'checked', )

class GroceryListItemView(ViewSet):
    """Grocery List Item view set"""

    def create(self, request):
        """Handle POST operations
        
        Returns:
            Response -- JSON serialized instance"""

        # Get current user from request
        user = request.auth.user
        # Get ingredients from request
        ingredient_ids = request.data.get('ingredients', [])
        # Check if a grocery list exists
        try:
            # Get the grocery list
            grocery_list = GroceryList.objects.get(user=user)
        except GroceryList.DoesNotExist:
            # Create a grocery list instance
            grocery_list = GroceryList.objects.create(user=user)

        added_items = []

        # Iterate through the ingredients
        for ingredient_id in ingredient_ids:
            # Get ingredient
            ingredient = Ingredient.objects.get(pk=ingredient_id)
            # Check if ingredient is in the grocery list
            if not GroceryListItem.objects.filter(grocery_list=grocery_list, ingredient=ingredient).exists():
                # Create a grocery list item
                grocery_list_item = GroceryListItem.objects.create(grocery_list=grocery_list, ingredient=ingredient)
                # Add grocery list item to added_items array
                added_items.append(grocery_list_item)

        # Serialize the grocery list items
        serializer = GroceryListItemSerializer(added_items, many=True)
        # Return an array of all the grocery list item objects
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single grocery item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            grocery_item = GroceryListItem.objects.get(pk=pk)
            grocery_item.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except GroceryListItem.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for grocery items

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            grocery_item = GroceryListItem.objects.get(pk=pk)
            grocery_item.checked = request.data["checked"]
            grocery_item.save()
        except GroceryListItem.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

        return Response(None, status=status.HTTP_204_NO_CONTENT)
