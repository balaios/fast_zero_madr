import factory.fuzzy

from fast_zero_madr.models import Book, Novelist, User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


class NovelistFactory(factory.Factory):
    class Meta:
        model = Novelist

    name = factory.Sequence(lambda n: f'test{n}')


class BookFactory(factory.Factory):
    class Meta:
        model = Book

    title = factory.Sequence(lambda n: f'test{n}')
    year = factory.fuzzy.FuzzyInteger(1900, 2024)
    novelist_id = None
