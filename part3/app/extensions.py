#!/usr/bin/python3
"""
Application extensions.
"""

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()
cors = CORS()
