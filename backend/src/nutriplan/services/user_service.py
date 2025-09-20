from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from nutriplan.models import DietaryRestriction

CustomUser = get_user_model()


class UserService:
    @staticmethod
    def create_user(user_data) -> AbstractUser:
        return CustomUser.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", ""),
        )

    @staticmethod
    def add_dietary_restriction(user, restriction_name):
        restriction, _ = DietaryRestriction.objects.get_or_create(name=restriction_name)
        user.dietary_restrictions.add(restriction)
        return user

    @staticmethod
    def get_user_with_restrictions(user_id) -> AbstractUser:
        return CustomUser.objects.prefetch_related("dietary_restrictions").get(
            id=user_id
        )
