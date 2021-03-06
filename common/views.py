# Create your views here.
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from common.models import User
from common.permissions import IsUser
from common.serializers import CustomRegisterSerializer, UserSerializer, UserLoginSerializer


@permission_classes([AllowAny])
class Registration(generics.GenericAPIView):
    serializer_class = CustomRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'Request Body Error.'}, status = status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)
        return Response({
            'user': UserSerializer(user, context = self.get_serializer_context()).data
        }, status = status.HTTP_201_CREATED)


@permission_classes([AllowAny])
class Login(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'Request Body Error.'}, status = status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user['username'] == 'None':
            return Response({'message': 'fail'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': user['token']
        })


@permission_classes([IsAuthenticated, IsUser])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'



