from users.models import User
from users import service

sample = User(id=4, email="robert@solar.com")


def test_create():
    resp = service.create(sample)
    assert resp == sample
    data = service.get_all()
    assert len(data) == 3


def test_get_exists():
    resp = service.get_one(4)
    assert resp == sample


def test_get_missing():
    resp = service.get_one(5)
    assert resp is None
