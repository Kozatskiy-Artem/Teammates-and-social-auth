from abc import ABCMeta, abstractmethod

from .dto import OAuthDTO, OAuthResponseDTO


class OAuthRepositoryInterfaces(metaclass=ABCMeta):
    @abstractmethod
    def get_or_create_oauth_user(self, user_dto: OAuthResponseDTO):
        """
        Get or create a user based on data from OAuth or returns
        the necessary data to authenticate an existing user.

        Args:
           user_dto(OAuthResponseDTO): OAuth user info.
        Returns:
            User - user object.
        """
        pass


class ProviderInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_user_info(self) -> OAuthResponseDTO:
        """
        Method accepts get_access_token, makes a request to google and returns user_info

        Returns:
              OAuthResponseDTO: email and id(to create password) from Google
        """
        pass

    @abstractmethod
    def get_access_token(self, auth_dto: OAuthDTO) -> str:
        """
        Method accepts authorization code from Google, makes a request to google and returns access token

        Args:
            auth_dto(OAuthDTO): Google's authorization code.
        Returns:
              access_token
        """
        pass

    @abstractmethod
    def get_redirect_url(self) -> str:
        """
        Get the redirect URL for the OAuth2 authentication flow.

        Returns:
            str - The redirect URL for the OAuth2 authentication.
        """
        pass
