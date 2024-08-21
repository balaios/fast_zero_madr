import factory.fuzzy

from fast_zero_madr.models import Livro, Romancista, User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    senha = factory.LazyAttribute(lambda obj: f'{obj.username}123')


class RomancistaFactory(factory.Factory):
    class Meta:
        model = Romancista

    nome = factory.Sequence(lambda n: f'test{n}')


class LivroFactory(factory.Factory):
    class Meta:
        model = Livro

    titulo = factory.Sequence(lambda n: f'test{n}')
    ano = factory.fuzzy.FuzzyInteger(1900, 2024)
    id_romancista = None
