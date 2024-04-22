from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer,UserLoginSerializer,ProfileSerializer,UpdateSerializer
from .models import CustomUser
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.utils import timezone
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                # Manually update the last_login field
                user.last_login = timezone.now()
                user.save()  
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'detail': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileRetrieveAPIView(APIView):
    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = ProfileSerializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ProfileUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [AllowAny]

    queryset = CustomUser.objects.all()
    serializer_class = UpdateSerializer

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        else:
            return response

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        else:
            return response
        
class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "No users found"}, status=status.HTTP_404_NOT_FOUND)
        

class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    lookup_url_kwarg = 'pk'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "All users deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class UserDeleteAllAPIView(APIView):
    def delete(self, request):
        try:
            CustomUser.objects.all().delete()
            return Response({"message": "All users deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": "Failed to delete users", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserBulkDeleteAPIView(APIView):
    def post(self, request):
        try:
            user_ids = request.data.get('user_ids', [])
            if not isinstance(user_ids, list):
                return Response({"message": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)
            
            users_to_delete = CustomUser.objects.filter(id__in=user_ids)
            users_to_delete.delete()
            return Response({"message": f"{len(user_ids)} users deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": "Failed to delete users", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
