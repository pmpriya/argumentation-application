import pytest
from sqlalchemy_models import app, db
from sqlalchemy_models import register_table

@pytest.fixture(scope='module')
def newUser():
    user = register_table('user1', 'argupedia')
    return user

@pytest.fixture(scope='module')
def initDatabase():
    # Create the database and the database table
    user = newUser()
    db.create_all()

    # Insert user database
    user1 = register_table('user2', 'pwd2')
    user2 = register_table('user3', 'pwd3')
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield True # this is where the testing happens!

    #db.drop_all()


@pytest.fixture(scope='function')
def loginDefaultUser():
    query = register_table.query.filter(username = 'user1', password='argupedia')
    if (query):
        yield True