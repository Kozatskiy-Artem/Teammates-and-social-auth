import os
from urllib import parse
import requests

from .dto import OAuthDTO, OAuthResponseDTO
from .exceptions import OAuth2Exception
from .interfaces import GoogleProviderInterfaces


class GoogleOAuth2Provider(GoogleProviderInterfaces):
    """
    GoogleOAuth2Provider is a class that performs the necessary queries
    to the Google service to authenticate the user
    """

    CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
    CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
    REDIRECT_URI = os.environ["REDIRECT_URI"]
    GET_ACCESS_TOKEN_URL = "https://www.googleapis.com/oauth2/v3/token"
    GET_USER_EMAIL_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    def get_user_info(self, auth_dto: OAuthDTO) -> OAuthResponseDTO:
        """
        Method accepts get_access_token, makes a request to google and returns user_info

        Args:
            auth_dto: (OAuthDTO)
        Returns:
              OAuthResponseDTO: email and id(to create password) from Google
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.get_access_token(auth_dto)}",
        }

        response = requests.post(self.GET_USER_EMAIL_URL, headers=headers)

        if not response.ok:
            raise OAuth2Exception("Failed to get user info")

        response_data = response.json()

        return OAuthResponseDTO(
            email=response_data["email"],
            first_name=response_data["given_name"],
            last_name=response_data["family_name"]
        )

    def get_access_token(self, auth_dto: OAuthDTO) -> str:
        """
        Method accepts authorization code from Google,
        makes a request to google and returns access token
        Args:
            auth_dto(OAuthDTO): Google's authorization code.
        Returns:
              access_token
        """

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
