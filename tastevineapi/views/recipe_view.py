from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from tastevineapi.models import Recipe, RecipeIngredient
from .category_view import CategorySerializer
from .recipe_ingredient_view import RecipeIngredientSerializer

class RecipeView(ViewSet):
    """Recipe view set"""

    def list(self, request):
        """Handle GET requests for all recipes

        Returns:
            Response -- JSON serialized list of recipes
        """

        owner_only = self.request.query_params.get("owner", None)

        try:
            recipes = Recipe.objects.all().order_by("-publication_date")

            if owner_only is not None and owner_only == 'current':
                recipes = recipes.filter(author=request.auth.user)
            
            for recipe in recipes:
                recipe.publication_date = recipe.publication_date.strftime("%m-%d-%Y")
            
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
            recipe.publication_date = recipe.publication_date.strftime("%m-%d-%Y")
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def create(self, request):
        """Handle POST requests for recipes

        Returns:
            Response -- JSON serialized representation of newly created recipe
        """
        recipe = Recipe()
        recipe.title = request.data["title"]
        recipe.instructions = request.data["instructions"]
        recipe.image = request.data["image"]
        recipe.author = request.auth.user

        try:
            # Save the new recipe
            recipe.save()

            #? Ingredients:
            # retrieve ingredients from payload
            ingredient_data = request.data.get("ingredients", [])
            # Loop through the array and grab each ingredient id
            ingredient_ids = [ingredient.get('ingredient') for ingredient in ingredient_data]
            # Through the many to many field set the ingredient ids
            recipe.ingredients.set(ingredient_ids)
            # Loop through each ingredient again from the request
            for ingredient in ingredient_data:
                # retrieve the join table with the correct recipe id & ingredient id
                recipe_ingredient = RecipeIngredient.objects.get(recipe__id=recipe.id, ingredient__id=ingredient['ingredient'])
                # Retrieve the new information from the ingredient
                quantity = ingredient['quantity']
                unit = ingredient['unit']
                #  Save the new info in the join table
                recipe_ingredient.quantity = quantity
                recipe_ingredient.unit = unit
                recipe_ingredient.save()

            #? Categories:
            category_ids = request.data.get("categories", [])
            recipe.categories.set(category_ids)

            recipe.publication_date = recipe.publication_date.strftime("%m-%d-%Y")
            serializer = RecipeSerializer(recipe, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None):
        """Handle PUT requests for recipes

        Returns:
            Response -- JSON serialized representation of updated recipe
        """
        try:
            recipe = Recipe.objects.get(pk=pk)

            if recipe.author.id == request.user.id:
                recipe.title = request.data["title"]
                recipe.instructions = request.data["instructions"]
                recipe.image = request.data["image"]
                recipe.author = request.auth.user
                recipe.save()

                #? Ingredients:
                ingredient_data = request.data.get("ingredients", [])
                ingredient_ids = [ingredient.get('ingredient') for ingredient in ingredient_data]
                recipe.ingredients.set(ingredient_ids)
                for ingredient in ingredient_data:
                    recipe_ingredient = RecipeIngredient.objects.get(recipe__id=recipe.id, ingredient__id=ingredient['ingredient'])
                    quantity = ingredient['quantity']
                    unit = ingredient['unit']
                    recipe_ingredient.quantity = quantity
                    recipe_ingredient.unit = unit
                    recipe_ingredient.save()

                #? Categories:
                category_ids = request.data.get("categories", [])
                recipe.categories.set(category_ids)

                serializer = RecipeSerializer(recipe, many=False)
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

            return Response({"message": "You are not the author of this recipe."}, status=status.HTTP_403_FORBIDDEN)
        
        except Recipe.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            recipe = Recipe.objects.get(pk=pk)
            if recipe.author.id == request.user.id:
                recipe.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            return Response({"message": "You are not the author of this recipe."}, status=status.HTTP_403_FORBIDDEN)

        except Recipe.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for user"""
    class Meta:
        model = User
        fields = ('first_name',)

class RecipeSerializer(serializers.ModelSerializer):
    """JSON serializer for recipe"""
    author = UserSerializer(many=False)
    recipe_ingredient = RecipeIngredientSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'author', 'publication_date', 'image', 'instructions', 'recipe_ingredient', 'categories',)
