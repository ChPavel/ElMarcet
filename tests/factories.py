import factory
from django.utils import timezone
from pytest_factoryboy import register
from network.models import User, Contacts, Product, Provider


@register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._get_manager(model_class).create_user(*args, **kwargs)


@register
class ContactsFactory(factory.django.DjangoModelFactory):
    email = factory.Faker('email')
    country = factory.Faker('country')
    city = factory.Faker('city')
    street = factory.Faker('street_name')
    house_number = factory.Faker('random_digit_not_null')
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Contacts


@register
class ProductFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence')
    slug = factory.Faker('slug')
    model = factory.Faker('sentence')
    release = factory.Faker('date_this_month')
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Product


class DatesFactoryMixin(factory.django.DjangoModelFactory):
    time_create = factory.LazyFunction(timezone.now)
    time_update = factory.LazyFunction(timezone.now)

    class Meta:
        abstract = True


@register
class ProviderFactory(DatesFactoryMixin):
    title = factory.Faker('sentence')
    slug = factory.Faker('slug')
    type_provider = factory.Faker('random_element', elements=[x[0] for x in Provider.TYPE_P])
    contacts = factory.SubFactory(ContactsFactory)
    products = factory.SubFactory(ProductFactory)
    credit = factory.Faker('random_digit_not_null')
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Provider
