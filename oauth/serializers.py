from rest_framework import serializers


class OAuth2Serializer(serializers.Serializer):
    code = serializers.CharField()


class OAuth2ResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
