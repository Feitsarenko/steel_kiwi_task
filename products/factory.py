import factory
from factory.django import DjangoModelFactory
from .models import Product, Category, Like, Comment
from django.contrib.auth.models import User
import factory.fuzzy
import uuid
from faker import Faker
import datetime


class CategoryFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: 'category{}'.format(n))
    description = Faker().text()

    class Meta:
        model = Category


list_grade = [x[0] for x in Product.PRODUCT_GRADE]


class ProductFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: 'product{}'.format(n))
    description = Faker().text()
    grade = factory.fuzzy.FuzzyChoice(list_grade)
    price = factory.fuzzy.FuzzyDecimal(low=1, high=99999, precision=2)
    category = factory.SubFactory(CategoryFactory)
    image = factory.django.ImageField(color='blue')

    class Meta:
        model = Product


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: 'username_{}'.format(n))
    email = factory.Sequence(lambda n: 'email{}@email.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', uuid.uuid4().hex)
    first_name = factory.Sequence(lambda n: 'first {}'.format(n))
    last_name = factory.Sequence(lambda n: 'last {}'.format(n))

    class Meta:
        model = User


class LikeFactory(DjangoModelFactory):
    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Like


class CommentFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    text = Faker().text()

    class Meta:
        model = Comment
