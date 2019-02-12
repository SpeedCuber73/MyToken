from rest_framework.permissions import IsAuthenticated
from .models import AddressBook
from . import serializers
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class AddressBookViewSet(viewsets.ModelViewSet):

    queryset = AddressBook.objects.all()
    serializer_class = serializers.AddressBookSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        user = self.request.user
        return AddressBook.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
