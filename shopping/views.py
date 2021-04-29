# Create your views here.
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets

from shopping.models import Store
from shopping.serializers import StoreSerializer, StoreLoginSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_object(self, store_name):
        return self.get_queryset().get(store_name=store_name)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(request.user.store_name)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


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
