
import datetime

from sqlalchemy.orm import sessionmaker

from app.models import User


def test_signup(client):
    with client:
        response = client.get('/')
        assert response.status_code == 200  # successfully reached the test


# def test_merchant_register(db, client):
#     username = "Test1"
#     email = "test@mail.com"
#     password = "Pass-1"
#     password = "Pass-1"
#     with client:
#         response = client.post('/signup',
#                                data={'username': username, 'email': email, 'password': password, 'submit': True})
#         assert response.status_code == 302  # 302 successful redirect to home page
#         # check to see if the user is in the database

#         response = client.get('/login')
#         assert response.status_code == 200  # successfully reached the test

#         users = User.query.filter(User.roles.any(id=2)).filter_by(username=username)
#         assert users.count() == 1  # should only have 1 matching user

#         # check props of user to make sure they are inserted correctly
#         user = users.first()
#         assert user.username == username
#         assert user.email == email
#         assert user.check_password(password)

#     # clean up any changes
#     User.query.delete()
#     db.session.query(UserRole).delete()
#     db.session.commit()
#     db.session.flush()
