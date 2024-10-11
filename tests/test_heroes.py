import pytest
from app import create_app, db
from app.models import Hero, Power

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_add_hero(client):
    response = client.post('/heroes', json={
        'name': 'Superman',
        'superpower': 'Flying'
    })
    assert response.status_code == 201
    assert b'Superman' in response.data

def test_get_heroes(client):
    client.post('/heroes', json={
        'name': 'Superman',
        'superpower': 'Flying'
    })
    response = client.get('/heroes')
    assert response.status_code == 200
    assert b'Superman' in response.data

def test_add_power(client):
    response = client.post('/powers', json={
        'name': 'Invisibility'
    })
    assert response.status_code == 201
    assert b'Invisibility' in response.data

def test_assign_power(client):
    # Create hero and power
    client.post('/heroes', json={'name': 'Superman', 'superpower': 'Flying'})
    client.post('/powers', json={'name': 'Strength'})

    # Assign power to hero
    response = client.post('/heroes/1/powers/1')
    assert response.status_code == 201
    assert b'hero_id' in response.data
