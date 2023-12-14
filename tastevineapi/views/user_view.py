from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

    
class UserViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], url_path='register')
    def register_account(self, request):
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
            data = { 'token': token.key, 'userId': token.user.id }
            return Response(data, status=status.HTTP_201_CREATED)
            
        return Response({'message': 'You must provide email, password, first_name, and last_name'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='login')
    def user_login(self, request):
        '''Handles the authentication of a user
        
        Method arguments:
        request -- The full HTTP request object'''

        email = request.data['email']
        password = request.data['password']

        authenticated_user = authenticate(username=email, password=password)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)

            data = {'token': token.key, 'userId': token.user.id}
            return Response(data, status=status.HTTP_200_OK)
        else: 
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
            
        
    def retrieve(self, request, pk=None):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user record
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
