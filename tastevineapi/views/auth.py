# Passwords...try last names all lowercase
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new user for authentication
    
    Method arguments:
        request -- The full HTTP request object
    '''
    email = request.data.get('email', None)
    password = request.data.get('password', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)

    if email is not None and first_name is not None and last_name is not None and password is not None:

        try:
            new_user = User.objects.create_user(
                username = request.data['email'],
                email = request.data['email'],
                password = request.data['password'],
                first_name = request.data['first_name'],
                last_name = request.data['last_name'],
            )
        except IntegrityError:
            return Response({'message': 'An account with that email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
        token = Token.objects.create(user=new_user)
        data = { 'token': token.key }
        return Response(data)
        
    return Response({'message': 'You must provide email, password, first_name, and last_name'}, status=status.HTTP_400_BAD_REQUEST)