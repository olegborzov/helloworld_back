import pytest


@pytest.fixture(scope='session')
def reg(request):
    from core.registry import create_registry
    registry = create_registry(env='test', env_type='web')
    registry.db.drop_all()
    registry.db.create_all()
    load_test_objects(registry.db)
    return registry


@pytest.fixture(scope='session')
def db(reg):
    yield reg.db


@pytest.fixture(autouse=True)
def app_context(reg):
    """Creates a flask app context"""
    with reg.app.app_context():
        yield reg.app


@pytest.fixture
def client(app_context):
    with app_context.test_client(use_cookies=True) as test_client:
        yield test_client


@pytest.fixture
def auth_admin(client):
    client.post('/api/auth/login', json={'email': 'admin@test.ru', 'password': 'admin'})


@pytest.fixture
def auth_user(client):
    client.post('/api/auth/login', json={'email': 'user@test.ru', 'password': 'user'})


def load_test_objects(db):
    import models

    clear_tables(db)

    admin_user = models.User(email='admin@test.ru', is_admin=True)
    admin_user.password = 'admin'

    user = models.User(email='user@test.ru', is_admin=False)
    user.password = 'user'

    db.session.add_all([admin_user, user])
    db.session.commit()


def clear_tables(db):
    meta = db.metadata
    setval_query = "SELECT setval('{sequence}'::regclass, tmp.maxval+1, false) " \
                   "FROM (SELECT coalesce(max(id), 0) as maxval from \"{table_name}\") as tmp;"
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
        if 'id' in table.columns:
            db.session.execute(setval_query.format(
                sequence='{}_id_seq'.format(table.name),
                table_name=table.name
            ))
        print(f'Clear table {table}')
    db.session.commit()
