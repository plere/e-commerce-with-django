import jwt
from django.utils.encoding import smart_text
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework_jwt.settings import api_settings
from django.utils.translation import ugettext as _
from rest_framework import exceptions

from shopping.models import Store

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class JSONWebTokenAuthentication(BaseAuthentication):
    www_authenticate_realm = 'api'

    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth:
            if api_settings.JWT_AUTH_COOKIE:
                return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
            return None

        if smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)

        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        store = self.authenticate_credentials(payload)

        return (store, jwt_value)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        storename = payload.get('store_name')

        if not storename:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            store = Store.objects.get(store_name=storename)

        except store.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        return store


class StoreBackend(object):
    def authenticate(self, request, store_name=None, password=None):
        try:
            store = Store.objects.get(store_name=store_name)
            if store.password == password:
                return store
        except Store.DoesNotExist:
            return None
        return None





def storePayloadHandler(store):
    return {
        "store_name": store.store_name
    }
