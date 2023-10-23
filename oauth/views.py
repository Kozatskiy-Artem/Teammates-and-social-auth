from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.containers import ServiceContainer
from core.serializers import ResponseWithErrorSerializer

from .dto import OAuthDTO
from .exceptions import OAuth2Exception
from .serializers import GoogleOAuth2ResponseSerializer, GoogleOAuth2Serializer


class GoogleAuthView(APIView):
    """
    The class defines API endpoints for authenticating a user through a Google service.
    """

    @extend_schema(
        summary="Google user authentication.Redirects the user to the google "
        "authentication page.The response is a url "
        "with the 'code' parameter.",
        request=None,
        responses={
            200: {"type": "object", "properties": {"redirect_url": {"type": "string"}}},
        },
        tags=["OAuth"],
    )
    def get(self, request):
        """GET method to get google authentication data on redirect_url"""

        oauth_service = ServiceContainer.oauth_service()
        redirect_url = oauth_service.get_redirect_url()

        return Response({"redirect_url": redirect_url})

    @extend_schema(
        summary="Google user authentication. makes google queries to collect user data."
        " Creates a user in the system if he/she has not been created before "
        "and gives authorization tokens",
        request=GoogleOAuth2Serializer,
        responses={
            200: GoogleOAuth2ResponseSerializer,
            400: ResponseWithErrorSerializer,
            504: {"type": "object", "properties": {"detail": {"type": "string"}}},
        },
        tags=["OAuth"],
    )
    def post(self, request):
        """
        POST method processes "code" from Google, gets google user data,
        get or create the user and gives authorization tokens
        """
        google_auth_serializer = GoogleOAuth2Serializer(data=request.data)
        if not google_auth_serializer.is_valid():
            return Response(google_auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        auth_dto = OAuthDTO(**google_auth_serializer.validated_data)

        oauth_service = ServiceContainer.oauth_service()
        try:
            user = oauth_service.get_or_create_oauth_user(auth_dto)
        except OAuth2Exception as exception:
            return Response({"error": exception.message}, status=status.HTTP_504_GATEWAY_TIMEOUT)

        tokens_serializer = GoogleOAuth2ResponseSerializer(user)

        return Response(tokens_serializer.data)
