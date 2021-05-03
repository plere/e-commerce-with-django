# Create your views here.
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets

from shopping.models import Store, Item
from shopping.permissions import IsOwnerStore, IsStore
from shopping.serializers import StoreSerializer, StoreLoginSerializer, ItemSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    lookup_field = 'store_name'

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsStore]
        return [permission() for permission in permission_classes]


@permission_classes([AllowAny])
class Login(generics.GenericAPIView):
    serializer_class = StoreLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'Request Body Error.'}, status = status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        store = serializer.validated_data
        if store['store_name'] == 'None':
            return Response({'message': 'fail'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'store': StoreSerializer(store, context=self.get_serializer_context()).data,
            'token': store['token']
        })


@permission_classes([IsAuthenticated, IsStore, IsOwnerStore])
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        serializer.save(store=self.request.user)


