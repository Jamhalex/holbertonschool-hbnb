#!/usr/bin/python3
from flask import Flask

from app.api import init_api
from app.persistence.repository import InMemoryRepository
from app.services.facade import HBnBFacade


def create_app():
    app = Flask(__name__)

    # In-memory repo + facade singletons for Part 2
    repo = InMemoryRepository()
    facade = HBnBFacade(repo)

    # Attach to app for access in namespaces
    app.config["FACADE"] = facade

    init_api(app)
    return app
