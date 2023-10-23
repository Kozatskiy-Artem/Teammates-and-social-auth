from rest_framework import serializers


class GoogleOAuth2Serializer(serializers.Serializer):
    code = serializers.CharField()


class GoogleOAuth2ResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
