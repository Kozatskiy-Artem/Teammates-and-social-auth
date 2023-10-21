from rest_framework import serializers


class ResponseWithErrorSerializer(serializers.Serializer):
    """
    Serializer for creating an error response.
    Used to create a response that contains error information.
    Fields:
    - error (str): A string containing the error description.
    """

    error = serializers.CharField()


class ValidationErrorResponseSerializer(serializers.Serializer):
    """
    Serializer for creating a validation error response.
    Used to create a response that contains information about fields that failed validation.
    Fields:
    - field_name (list): The name of the field that failed validation along with a list of errors.
    """

    field_name = serializers.ListField()
