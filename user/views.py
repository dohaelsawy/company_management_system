from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, login
from rest_framework.permissions import AllowAny
from .serializers import EmailLoginSerializer
from rest_framework.parsers import JSONParser

User = get_user_model()


class EmailLoginView(APIView):

    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    
    def post(self, request):

        serializer = EmailLoginSerializer(data=request.data)
        
        if serializer.is_valid():

            email = serializer.validated_data['email']
            user, _ = User.objects.get_or_create(email=email, defaults={'username': email})

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
        
            return Response({"message": "Login successful", "email": email})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
