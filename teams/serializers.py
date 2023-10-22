from rest_framework import serializers


class MemberSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)


class TeamCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)


class TeamSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    members = MemberSerializer(many=True)


class MemberIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
