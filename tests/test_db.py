from sqlalchemy import select

from fast_api_dunossauro.models import User


def test_create_user(session):
    user = User(
        username='dunossauro',
        email='dunomail@mail.com',
        password='123456',
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    session.scalar(select(User).where(User.email == 'dunomail@mail.com'))

    assert user.username == 'dunossauro'
    assert user.id == 1
