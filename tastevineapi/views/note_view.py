from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from tastevineapi.models import Note, Recipe
from .recipe_view import RecipeUserSerializer

class NoteSerializer(serializers.ModelSerializer):
    """JSON serializer for notes"""
    author = RecipeUserSerializer()

    class Meta:
        model = Note
        fields = ('id', 'author', 'content', 'posted_on',)

class NoteView(ViewSet):
    """Note view set"""


    def list(self, request):
        """Handle GET requests for all notes

        Returns:
            Response -- JSON serialized array
        """
        recipe_id = request.query_params.get('recipe', None)
        
        try:
            if recipe_id is not None:
                notes = Note.objects.filter(recipe=recipe_id).order_by('-posted_on')
            else:
                notes = Note.objects.all()
            
            for note in notes:
                note.posted_on = note.posted_on.strftime("%m-%d-%Y")
                
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def update(self, request, pk=None):
        """Handle PUT requests for notes

        Returns:
            Response -- Empty body with 204 status code
        """
        # Get an object instance of a recipe
        recipe = Recipe.objects.get(pk=request.data["recipeId"])

        # Get an object instance of note
        note = Note.objects.get(pk=pk)
        # Assign the note object property values
        note.content = request.data["content"]
        note.author = request.auth.user
        note.recipe = recipe

        try:
            note.save()
        except Note.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single note

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            note = Note.objects.get(pk=pk)
            note.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Note.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        recipe = Recipe.objects.get(pk=request.data["recipeId"])

        note = Note()
        note.content = request.data["content"]
        note.author = request.auth.user
        note.recipe = recipe

        try:
            note.save()
            serializer = NoteSerializer(note)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)