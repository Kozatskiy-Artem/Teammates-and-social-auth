import os
from urllib import parse
import requests
from typing import Type

from .dto import OAuthDTO, OAuthResponseDTO
from .exceptions import OAuth2Exception
from .interfaces import ProviderInterface


class BaseOAuth2Provider(ProviderInterface):

    GET_ACCESS_TOKEN_URL = None
    GET_USER_EMAIL_URL = None
    CLIENT_ID = None
    CLIENT_SECRET = None
    REDIRECT_URI = os.environ.get("REDIRECT_URI")

    def __init__(self, auth_dto: OAuthDTO) -> None:
        self.access_token = self.get_access_token(auth_dto)

    def get_access_token(self, auth_dto: OAuthDTO) -> str:
        code = self._get_decode_code(auth_dto)

        headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
        params = {
            "code": code,
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "redirect_uri": self.REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(self.GET_ACCESS_TOKEN_URL, params=params, headers=headers)

        if not response.ok:
            raise OAuth2Exception("Invalid authorization code")

        response_data = response.json()
        access_token = response_data["access_token"]

        return access_token

    @staticmethod
    def _get_decode_code(auth_dto: OAuthDTO) -> str:
        """
        Get the decoded code from the provided OAuthDTO object.

        Args:
            auth_dto (OAuthDTO): An instance of the OAuthDTO object.

        Returns:
            str - The decoded code.

        Raises:
            OAuth2Exception: If an error occurs during the decoding operation.
        """

        if getattr(auth_dto, "code", False):
            code = parse.unquote(getattr(auth_dto, "code"))
            return code
        raise OAuth2Exception("Error in decoder operation")

    def get_user_info(self):
        pass

    @classmethod
    def get_redirect_url(cls):
        pass


class GoogleOAuth2Provider(BaseOAuth2Provider):
    """
    GoogleOAuth2Provider is a class that performs the necessary queries
    to the Google service to authenticate the user
    """

    CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
    CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
    GET_ACCESS_TOKEN_URL = "https://www.googleapis.com/oauth2/v3/token"
    GET_USER_EMAIL_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    def get_user_info(self) -> OAuthResponseDTO:
        """
        Method accepts get_access_token, makes a request to google and returns user_info

        Returns:
              OAuthResponseDTO: email and id(to create password) from Google
        """

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"}

        response = requests.post(self.GET_USER_EMAIL_URL, headers=headers)

        if not response.ok:
            raise OAuth2Exception("Failed to get user info")

        response_data = response.json()

        return OAuthResponseDTO(
            email=response_data["email"],
            first_name=response_data["given_name"],
            last_name=response_data["family_name"]
        )

    @classmethod
    def get_redirect_url(cls) -> str:
        """
        Get the redirect URL for the OAuth2 authentication flow.

        Returns:
            str - The redirect URL for the OAuth2 authentication.
        """

        return (
            f"https://accounts.google.com/o/oauth2/auth?client_id={cls.CLIENT_ID}"
            f"&response_type=code&scope=openid%20profile%20email&redirect_uri={cls.REDIRECT_URI}"
        )


class FacebookOAuth2Provider(BaseOAuth2Provider):
    """
    FacebookOAuth2Provider is a class that performs the necessary queries
    to the Facebook service to authenticate the user
    """

    CLIENT_ID = os.environ.get("FACEBOOK_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("FACEBOOK_CLIENT_SECRET")

    GET_ACCESS_TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
    GET_USER_DATA_URL = "https://graph.facebook.com/me?fields=email,picture,first_name,last_name"

    @classmethod
    def get_redirect_url(cls) -> str:
        """
        Get the redirect URL for the OAuth2 authentication flow.

        Returns:
            str - The redirect URL for the OAuth2 authentication.
        """

        return (
            f"https://www.facebook.com/v18.0/dialog/oauth?client_id={cls.CLIENT_ID}" f"&redirect_uri={cls.REDIRECT_URI}"
        )

    def get_user_info(self):
        """
        Method accepts get_access_token, makes a request to google and returns user_info

        Returns:
              OAuthResponseDTO: email and id(to create password) from Google
        """

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"}

        response = requests.get(self.GET_USER_DATA_URL, headers=headers)

        if not response.ok:
            raise OAuth2Exception("Facebook API error 2")

        response_data = response.json()

        try:
            email = response_data["email"]
        except KeyError:
            raise OAuth2Exception("Not email in Facebook response user data")

        return OAuthResponseDTO(
            email=email,
            first_name=response_data["first_name"],
            last_name=response_data["last_name"]
        )


class OAuth2ProviderFactory:

    @staticmethod
    def get_provider(provider: str) -> Type[ProviderInterface]:
        match provider:
            case "google":
                return GoogleOAuth2Provider
            case "facebook":
                return FacebookOAuth2Provider
            case _:
                raise OAuth2Exception("Unsupported oauth provider")
