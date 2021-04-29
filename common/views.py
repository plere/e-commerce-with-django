# Create your views here.
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response

from common.models import User
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


@permission_classes([IsAuthenticated])
class Info(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data
        }, status = status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class Modify(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get_object(self, username):
        return User.objects.get(username=username)

    def patch(self, request):
        user = self.get_object(request.user.username)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "user": UserSerializer(user, context = self.get_serializer_context()).data
            }, status = status.HTTP_202_ACCEPTED)
        return Response({"message": "fail"}, status=status.HTTP_409_CONFLICT)


@permission_classes([IsAuthenticated])
class Delete(generics.GenericAPIView):
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, username = request.user.username)
        if user:
            user.delete()
            return Response({
                "message": "user remove ok"
            }, status = status.HTTP_200_OK)
        return Response({
            "message": "fail"
        }, status = status.HTTP_400_BAD_REQUEST)

