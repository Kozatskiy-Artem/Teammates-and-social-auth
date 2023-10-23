from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.containers import ServiceContainer
from core.serializers import ResponseWithErrorSerializer

from .dto import OAuthDTO
from .exceptions import OAuth2Exception
from .serializers import OAuth2ResponseSerializer, OAuth2Serializer


class OAuthView(APIView):
    """
    The class defines API endpoints for authenticating a user through a Google or Facebook service.
    """

    @extend_schema(
        summary="Get URL for redirect user to chosen auth provider for login process",
        description=(
                "## NOTE\n"
                "### Authentication via Facebook works in test mode,"
                "meaning it only works with the developer's account of this application.\n"
                "Alternatively, you can use the credentials of your own configured Facebook app for logging in."
        ),
        parameters=[
            OpenApiParameter(
                name="provider",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                enum=["google", "facebook"],
                description="Authentication provider (e.g., 'google' or 'facebook').",
            ),
        ],
        request=None,
        responses={
            200: {"type": "object", "properties": {"redirect_url": {"type": "string"}}},
            400: ResponseWithErrorSerializer,
        },
        tags=["OAuth"],
    )
    def get(self, request, provider: str):
        """GET method to get provider authentication data on redirect_url"""

        oauth_service = ServiceContainer.oauth_service()
        try:
            redirect_url = oauth_service.get_redirect_url(provider)
        except OAuth2Exception as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"redirect_url": redirect_url})

    @extend_schema(
        summary="OAuth user authentication",
        parameters=[
            OpenApiParameter(
                name="provider",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                enum=["google", "facebook"],
                description="Authentication provider (e.g., 'google' or 'facebook').",
            ),
        ],
        request=OAuth2Serializer,
        responses={
            200: OAuth2ResponseSerializer,
            400: ResponseWithErrorSerializer,
            504: {"type": "object", "properties": {"detail": {"type": "string"}}},
        },
        tags=["OAuth"],
    )
    def post(self, request, provider: str):
        """
        POST method processes "code" from provider, gets user data,
        get or create the user and gives authorization tokens
        """

        oauth_serializer = OAuth2Serializer(data=request.data)
        if not oauth_serializer.is_valid():
            return Response(oauth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        auth_dto = OAuthDTO(**oauth_serializer.validated_data)

        oauth_service = ServiceContainer.oauth_service()
        try:
            user = oauth_service.get_or_create_oauth_user(auth_dto, provider)
        except OAuth2Exception as exception:
            return Response({"error": exception.message}, status=status.HTTP_504_GATEWAY_TIMEOUT)

        tokens_serializer = OAuth2ResponseSerializer(user)

        return Response(tokens_serializer.data)
