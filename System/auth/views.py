from rest_framework.response import Response
from serializers import status
from rest_framework.exceptions import AuthenticationFailed
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
class CustomTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            return Response({
                'status': False,
                'message': "Incorrect username or password"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
@api_view('POST')
def register(request):
    pass