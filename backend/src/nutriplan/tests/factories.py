from decimal import Decimal
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.utils.text import slugify
from factory.declarations import (
    LazyAttribute,
    LazyFunction,
    PostGenerationMethodCall,
    Sequence,
    SubFactory,
)
from factory.django import DjangoModelFactory
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

fake = Faker("es_NI")
User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta(DjangoModelFactory.Meta):
        model = User

    id = LazyFunction(uuid4)
    email = LazyAttribute(lambda _: fake.unique.email().lower())
    first_name = LazyAttribute(lambda _: fake.first_name())
    last_name = LazyAttribute(lambda _: fake.last_name())
    is_active = True
    is_staff = False
    is_superuser = False
    password = PostGenerationMethodCall("set_password", "secret1234")


class DietaryRestrictionFactory(DjangoModelFactory):
    class Meta(DjangoModelFactory.Meta):
        model = DietaryRestriction

    id = LazyFunction(uuid4)
    name = LazyAttribute(lambda _: fake.unique.word())


class CategoryFactory(DjangoModelFactory):
    class Meta(DjangoModelFactory.Meta):
        model = Category

    id = LazyFunction(uuid4)
    name = LazyAttribute(lambda _: fake.unique.word().capitalize())
    friendly_name = LazyAttribute(lambda obj: obj.name)
    description = Faker("sentence")


class IngredientFactory(DjangoModelFactory):
    class Meta(DjangoModelFactory.Meta):
        model = Ingredient

    id = LazyFunction(uuid4)
    name = LazyAttribute(lambda _: fake.unique.word().capitalize())
    description = Faker("sentence")
    calories_per_100g = Decimal("100.00")
    protein_per_100g = Decimal("10.00")
    carbs_per_100g = Decimal("10.00")
    fat_per_100g = Decimal("5.00")
    sugar_per_100g = Decimal("5.00")


class ImageFactory(DjangoModelFactory):
    class Meta(DjangoModelFactory.Meta):
        model = Image

    id = LazyFunction(uuid4)
    url = LazyAttribute(
        lambda _: f"https://picsum.photos/seed/{uuid4()}/800/600"
    )
    alt_text = Faker("sentence")


class RecipeFactory(DjangoModelFactory):
    class Meta(DjangoModelFactory.Meta):
        model = Recipe

    id = LazyFunction(uuid4)
    name = LazyAttribute(lambda _: fake.unique.sentence(nb_words=3).rstrip("."))
    slug = LazyAttribute(lambda obj: slugify(obj.name))
    description = Faker("paragraph")
    category = SubFactory(CategoryFactory)
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


class RecipeIngredientFactory(DjangoModelFactory):
    class Meta(DjangoModelFactory.Meta):
        model = RecipeIngredient

    id = LazyFunction(uuid4)
    recipe = SubFactory(RecipeFactory)
    ingredient = SubFactory(IngredientFactory)
    amount = Decimal("100.00")
    unit = "g"


class ReviewFactory(DjangoModelFactory):
    class Meta(DjangoModelFactory.Meta):
        model = Review

    id = LazyFunction(uuid4)
    user = SubFactory(UserFactory)
    recipe = SubFactory(RecipeFactory)
    rating = 4
    comment = Faker("sentence")


class RecipeCollectionFactory(DjangoModelFactory):
    class Meta(DjangoModelFactory.Meta):
        model = RecipeCollection

    id = LazyFunction(uuid4)
    owner = SubFactory(UserFactory)
    name = LazyAttribute(lambda _: f"Lista {fake.word().capitalize()}")
    slug = LazyAttribute(lambda obj: slugify(obj.name))
    description = Faker("sentence")
    is_public = False


class CollectionItemFactory(DjangoModelFactory):
    class Meta(DjangoModelFactory.Meta):
        model = CollectionItem

    id = LazyFunction(uuid4)
    collection = SubFactory(RecipeCollectionFactory)
    recipe = SubFactory(RecipeFactory)
    order = Sequence(lambda n: n)
