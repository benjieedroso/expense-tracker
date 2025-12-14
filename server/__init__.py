import os
from dotenv import load_dotenv
from flask import Flask
from sqlalchemy.orm import DeclarativeBase


from .extensions import db
from .extensions import migrate
from .extensions import api

from .expense_ns import expense_ns
from .budget_ns import budget_ns
from .summary import summary_ns

load_dotenv()


class Base(DeclarativeBase):
    pass


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

    db.init_app(app)

    from . import models

    migrate.init_app(app, db)

    api.init_app(app)

    api.add_namespace(expense_ns)
    api.add_namespace(budget_ns)
    api.add_namespace(summary_ns)

    from .routes import register_routes
    register_routes(app)



    return app
    
    


