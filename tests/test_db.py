from sqlalchemy import select

from fast_zero_madr.models import User


def test_create_user(session):
    new_user = User(username='alice', senha='secret', email='teste@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'
