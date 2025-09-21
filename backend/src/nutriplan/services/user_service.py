"""
User service for managing user creation and dietary restrictions.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from nutriplan.models import CustomUser as User, DietaryRestriction

CustomUser = get_user_model()


class UserService:
    """
    Service class with static methods to handle user management.
    """

    @staticmethod
    def create_user(user_data: dict[str, str]) -> AbstractUser:
        """
        Creates a new user with the provided user data.

        Args:
            user_data:          dictionary containing user information.
                - "username":   username for the new user.
                - "email":      email address for the new user.
                - "password":   password for the new user.
                - "first_name": first name of the user, defaults to empty string.
                - "last_name":  last name of the user, defaults to empty string.

        Returns:
            AbstractUser: created user instance.

        """

        return CustomUser.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", ""),
        )

    @staticmethod
    def add_dietary_restriction(user: User, restriction_name: str) -> User:
        """
        Adds a dietary restriction to the given user.

        If dietary restriction does not exist, it will be created.
        The restriction is then associated with the user's `dietary_restrictions`.

        Args:
            user:             user instance to modify.
            restriction_name: name of dietary restriction to add.

        Returns:
            User: updated user instance with new dietary restriction.

        """

        restriction, _ = DietaryRestriction.objects.get_or_create(name=restriction_name)
        user.dietary_restrictions.add(restriction)
        return user

    @staticmethod
    def get_user_with_restrictions(user_id: int) -> AbstractUser:
        """
        Retrieve a CustomUser instance along with its related dietary restrictions.

        Args:
            user_id: unique identifier of user to retrieve.

        Returns:
            AbstractUser: user instance with pre-fetched dietary restrictions.

        """

        return CustomUser.objects.prefetch_related("dietary_restrictions").get(
            id=user_id
        )
