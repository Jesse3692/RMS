from flask_bcrypt import Bcrypt

from models.users import User

bcrypt = Bcrypt()


def validate_user(username, password):
    """
    Validates a user by their username and password.

    :param username: The username of the user to validate.
    :param password: The password of the user to validate.
    :return: The validated user if the username and password are valid, otherwise None.
    """
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password.password_hash, password):
        return user
    return None
