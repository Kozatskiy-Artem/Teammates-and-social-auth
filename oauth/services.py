from rest_framework_simplejwt.tokens import RefreshToken

from .dto import OAuthDTO, OAuthLoginResponseDTO
from .interfaces import GoogleProviderInterfaces, GoogleAuthRepositoryInterfaces


class GoogleAuthService:
    """
    The class GoogleAuthService is a service for managing interactions
    related to authentication through the Google service
    """

    def __init__(self, oauth_provider: GoogleProviderInterfaces, oauth_repository: GoogleAuthRepositoryInterfaces):
        self.oauth_provider = oauth_provider
        self.oauth_repository = oauth_repository

    def get_or_create_oauth_user(self, oauth_dto: OAuthDTO) -> OAuthLoginResponseDTO:
        """
        Get or create a user based on data from Google or returns
        the necessary data to authenticate an existing user.

        Args:
           oauth_dto(AuthDTO): Google's authorization code.

        Returns:
           OAuthLoginResponseDTO: A data transfer object containing user data for login.
        """

        user_info = self.oauth_provider.get_user_info(oauth_dto)
        user = self.oauth_repository.get_or_create_oauth_user(user_info)

        refresh = RefreshToken.for_user(user)

        return OAuthLoginResponseDTO(access_token=str(refresh.access_token), refresh_token=str(refresh))

    def get_redirect_url(self):
        """
        Get the redirect URL for the OAuth2 authentication flow.

        Returns:
            str - The redirect URL for the OAuth2 authentication.
        """

        return self.oauth_provider.get_redirect_url()
