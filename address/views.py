from rest_framework.permissions import IsAuthenticated
from .models import AddressBook
from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_403_FORBIDDEN, \
    HTTP_400_BAD_REQUEST
from rest_framework.authentication import BasicAuthentication,\
    SessionAuthentication
from .info_loader import city_info


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class AddressBookList(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        address_books = AddressBook.objects.filter(user=request.user)
        data = serializers.AddressBookSerializer(address_books, context={'request': request}, many=True).data
        return Response(data)

    def post(self, request):
        address_book = request.data
        address_book['user'] = request.user.id

        serializer = serializers.AddressBookSerializer(data=address_book)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "address created successfully"})
        return Response({"status": serializer.errors}, HTTP_400_BAD_REQUEST)


class AddressBookDetail(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, pk):
        address = get_object_or_404(AddressBook, pk=pk)
        if address.user != request.user:
            return Response({
                "credentials": "access denied"
            }, HTTP_403_FORBIDDEN)
        data = serializers.AddressBookSerializer(address, context={'request': request}).data
        print("city is ", address.city)
        data["coordinate"] = city_info(address.city)
        return Response(data)

    def put(self, request, pk):
        address = get_object_or_404(AddressBook, pk=pk)
        data = request.data
        serializer = serializers.AddressBookSerializer(instance=address, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "successfully updated"})
        return Response({
            "status": serializer.errors
        }, HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = get_object_or_404(AddressBook, pk=pk)
        address.delete()
        return Response({
            "status": "successfully deleted"
        })
