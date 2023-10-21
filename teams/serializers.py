from rest_framework import serializers


class TeamCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)


class TeamSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
