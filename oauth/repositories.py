from annoying.functions import get_object_or_None
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils.crypto import get_random_string

from .dto import OAuthResponseDTO
from .interfaces import OAuthRepositoryInterfaces


class GoogleAuthRepository(OAuthRepositoryInterfaces):

    def get_or_create_oauth_user(self, user_dto: OAuthResponseDTO):
        """
        Get or create a user based on data from OAuth or returns
        the necessary data to authenticate an existing user.

        Args:
           user_dto(OAuthResponseDTO): OAuth user info.
        Returns:
            User - user object.
        """

        user = get_object_or_None(get_user_model(), email=user_dto.email)

        if user is None:
            with transaction.atomic():
                user = get_user_model().objects.create_user(
                    username=user_dto.email.split("@")[0],
                    email=user_dto.email,
                    is_active=True,
                    first_name=user_dto.first_name,
                    last_name=user_dto.last_name,
                )

        user.password = make_password(self.generate_password())
        user.save()

        return user

    @staticmethod
    def generate_password():
        """Generate random password for oauth user"""
        password = get_random_string(length=12)

        return password
