from rest_framework import serializers


class UserSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=20, min_length=2)
    password = serializers.CharField(max_length=40)

    def validate_username(self, value):

        for char in value:
            if not (char.isalpha() or char.isdigit() or char is '_'):
                raise serializers.ValidationError("there is invalid character in username")
        return value
