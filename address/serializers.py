from rest_framework import serializers
from . import models


class AddressBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AddressBook
        fields = ('url', 'user', 'organization', 'city', 'house_num')

    def update(self, instance, validated_data):
        """
        override for protection on user update
        """
        instance.organization = validated_data.get('organization', instance.organization)
        instance.city = validated_data.get('city', instance.city)
        instance.house_num = validated_data.get('house_num', instance.house_num)

        instance.save()
        return instance
