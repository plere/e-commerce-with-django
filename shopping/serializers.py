from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from shopping.auth import storePayloadHandler
from shopping.models import Store, Item, Order

JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class StoreSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 128, write_only=True)
    item_set = serializers.StringRelatedField(many = True)

    class Meta:
        model = Store
        fields = ['store_name', 'password', 'description', 'item_set']


class StoreLoginSerializer(serializers.Serializer):
    store_name = serializers.CharField(max_length = 128)
    password = serializers.CharField(max_length = 128, write_only=True)
    description = serializers.CharField(read_only = True)
    token = serializers.CharField(max_length = 255, read_only = True)

    def validate(self, data):
        store_name = data.get('store_name')
        password = data.get('password', None)

        store = authenticate(store_name=store_name, password=password)

        if store is None:
            return {'store_name': 'None'}
        try:
            payload = storePayloadHandler(store)
            jwt_token = JWT_ENCODE_HANDLER(payload)

        except Store.DoesNotExist:
            raise serializers.ValidationError('Store with given storename and password does not exist')
        return {
            'store_name': store.store_name,
            'token': jwt_token
        }


class ItemSerializer(serializers.ModelSerializer):
    item_order_count = serializers.IntegerField(read_only = True)

    class Meta:
        model = Item
        fields = ['item_name', 'stock_count', 'item_order_count', 'item_price', 'item_description']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user_id', 'item_id', 'order_count', 'order_date', 'shipping_status']


