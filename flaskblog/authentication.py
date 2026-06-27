# authentication.py — password hashing helpers
# bcrypt is initialized in __init__.py; this module imports it from there
# so there's no circular dependency and no need to pass `app` in here.
from . import bcrypt

def hash_password(password):
    # Returns a UTF-8 decoded hash string safe to store in the database
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(hashed, plain):
    # Returns True if `plain` matches the stored `hashed` value
    return bcrypt.check_password_hash(hashed, plain)
