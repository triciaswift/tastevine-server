from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from tastevineapi.models import Note
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