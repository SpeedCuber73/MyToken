from rest_framework import serializers
from . import models


class AddressBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AddressBook
        fields = ('url', 'organization', 'city', 'house_num')
