# Create your views here.
from django.db import transaction
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets

from common.models import User
from common.permissions import IsUser
from shopping.models import Store, Item, Order
from shopping.permissions import IsOwnerStore, IsStore
from shopping.serializers import StoreSerializer, StoreLoginSerializer, ItemSerializer, OrderSerializer


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


@permission_classes([IsAuthenticated, IsUser])
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, username = request.user)
        item = get_object_or_404(Item, pk = kwargs['pk'])

        if int(request.data.get('order_count')) > item.stock_count - item.item_order_count or int(request.data.get('order_count')) <= 0:
            return Response({"message": 'check order count'}, status = status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(user=user, item=item)

        item.item_order_count += int(request.data.get('order_count'))
        item.save()

        return Response(serializer.data)

