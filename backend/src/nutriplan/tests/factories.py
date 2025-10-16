# type: ignore[reportIncompatibleVariableOverride]

from collections.abc import Iterable
from decimal import Decimal
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.utils.text import slugify
from factory import post_generation
from factory.declarations import LazyAttribute, LazyFunction, Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker as FactoryFaker
from faker import Faker

from nutriplan.models import (
    Category,
    CollectionItem,
    DietaryRestriction,
    Image,
    Ingredient,
    Recipe,
    RecipeCollection,
    RecipeIngredient,
    Review,
)

fake = Faker("es")
User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    id = LazyFunction(uuid4)
    email = LazyAttribute(lambda _: fake.unique.email().lower())
    first_name = LazyAttribute(lambda _: fake.first_name())
    last_name = LazyAttribute(lambda _: fake.last_name())
    is_active = True
    is_staff = False
    is_superuser = False


class DietaryRestrictionFactory(DjangoModelFactory):
    class Meta:
        model = DietaryRestriction

    id = LazyFunction(uuid4)
    name = LazyAttribute(lambda _: fake.unique.word())


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    id = LazyFunction(uuid4)
    name = LazyAttribute(lambda _: fake.unique.word().capitalize())
    friendly_name = LazyAttribute(lambda obj: obj.name)
    description = FactoryFaker("sentence")


class IngredientFactory(DjangoModelFactory):
    class Meta:
        model = Ingredient

    id = LazyFunction(uuid4)
    name = LazyAttribute(lambda _: fake.unique.word().capitalize())
    description = FactoryFaker("sentence")
    calories_per_100g = Decimal("100.00")
    protein_per_100g = Decimal("10.00")
    carbs_per_100g = Decimal("10.00")
    fat_per_100g = Decimal("5.00")
    sugar_per_100g = Decimal("5.00")


class ImageFactory(DjangoModelFactory):
    class Meta:
        model = Image

    id = LazyFunction(uuid4)
    url = LazyAttribute(lambda _: f"https://picsum.photos/seed/{uuid4()}/800/600")
    alt_text = FactoryFaker("sentence")


class RecipeFactory(DjangoModelFactory):
    class Meta:
        model = Recipe

    id = LazyFunction(uuid4)
    name = LazyAttribute(lambda _: fake.unique.sentence(nb_words=3).rstrip("."))
    slug = LazyAttribute(lambda obj: slugify(obj.name))
    description = FactoryFaker("paragraph")
    prep_time = 10
    cook_time = 20
    servings = 2
    calories_per_serving = Decimal("250.00")
    protein_per_serving = Decimal("15.00")
    carbs_per_serving = Decimal("20.00")
    fat_per_serving = Decimal("8.00")
    sugar_per_serving = Decimal("5.00")
    main_image_url = LazyAttribute(
        lambda _: f"https://picsum.photos/seed/{uuid4()}/400/300"
    )

    @post_generation
    def categories(
        self,
        create: bool,  # noqa: FBT001
        extracted: Iterable[Category] | None,
        **kwargs,  # noqa: ANN003, ARG002
    ) -> None:
        """
        Post-generation hook that populates categories relation.

        Args:
            create:    Indicates whether parent object was actually created.
            extracted: Optional iterable of Category instances to attach.
            **kwargs:  Ignored; present for Factory Boy API compatibility.

        """

        if not create:
            return

        if extracted:
            for c in extracted:
                self.categories.add(c)
        else:
            self.categories.add(CategoryFactory())


class RecipeIngredientFactory(DjangoModelFactory):
    class Meta:
        model = RecipeIngredient

    id = LazyFunction(uuid4)
    recipe = SubFactory(RecipeFactory)
    ingredient = SubFactory(IngredientFactory)
    amount = Decimal("100.00")
    unit = "g"


class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    id = LazyFunction(uuid4)
    user = SubFactory(UserFactory)
    recipe = SubFactory(RecipeFactory)
    rating = 4
    comment = FactoryFaker("sentence")


class RecipeCollectionFactory(DjangoModelFactory):
    class Meta:
        model = RecipeCollection

    id = LazyFunction(uuid4)
    owner = SubFactory(UserFactory)
    name = LazyAttribute(lambda _: f"Lista {fake.word().capitalize()}")
    slug = LazyAttribute(lambda obj: slugify(obj.name))
    description = FactoryFaker("sentence")
    is_public = False


class CollectionItemFactory(DjangoModelFactory):
    class Meta:
        model = CollectionItem

    id = LazyFunction(uuid4)
    collection = SubFactory(RecipeCollectionFactory)
    recipe = SubFactory(RecipeFactory)
    order = Sequence(lambda n: n)
