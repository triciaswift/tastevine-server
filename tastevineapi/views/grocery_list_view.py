from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from tastevineapi.models import GroceryList
from .grocery_list_item_view import GroceryListItemSerializer


class GroceryListSerializer(serializers.ModelSerializer):
    """JSON serializer for Grocery List"""
    groceries = GroceryListItemSerializer(many=True)


    class Meta:
        model = GroceryList
        fields = ( 'id', 'user', 'created_on', 'groceries', )


class GroceryListView(ViewSet):
    """Grocery List view set"""

    def list(self, request):
        """Handle GET requests for all grocery lists

        Returns:
            Response -- JSON serialized array
        """
        try:
            grocery_list = GroceryList.objects.get(user=request.auth.user)
            serializer = GroceryListSerializer(grocery_list, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single grocery list

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            grocery_list = GroceryList.objects.get(pk=pk)
            grocery_list.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except GroceryList.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
