from flask import Blueprint

webapp = Blueprint("webapp", __name__)

from . import add_to_poem_handler
from . import new_poem_handler

__all__ = [
    "add_to_poem_handler"
    "new_poem_handler"
]
