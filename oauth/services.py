from rest_framework_simplejwt.tokens import RefreshToken

from .dto import OAuthDTO, OAuthLoginResponseDTO
from .interfaces import OAuthRepositoryInterfaces


class GoogleAuthService:
    """
    The class GoogleAuthService is a service for managing interactions
    related to authentication through the Google service
    """

    def __init__(self, oauth_provider_factory, oauth_repository: OAuthRepositoryInterfaces):
        self.oauth_provider_factory = oauth_provider_factory
        self.oauth_repository = oauth_repository

    def get_or_create_oauth_user(self, oauth_dto: OAuthDTO, provider: str) -> OAuthLoginResponseDTO:
        """
        Get or create a user based on data from Google or returns
        the necessary data to authenticate an existing user.

        Args:
           oauth_dto(AuthDTO): Google's authorization code.

        Returns:
           OAuthLoginResponseDTO: A data transfer object containing user data for login.
        """

        provider_class = self.oauth_provider_factory.get_provider(provider)
        oauth_provider = provider_class(oauth_dto)
        user_info = oauth_provider.get_user_info()
        user = self.oauth_repository.get_or_create_oauth_user(user_info)

        refresh = RefreshToken.for_user(user)

        return OAuthLoginResponseDTO(access_token=str(refresh.access_token), refresh_token=str(refresh))

    def get_redirect_url(self, provider: str) -> str:
        """
        Get the redirect URL for the OAuth2 authentication flow.

        Returns:
            str - The redirect URL for the OAuth2 authentication.
        """

        oauth_provider = self.oauth_provider_factory.get_provider(provider)

        return oauth_provider.get_redirect_url()
