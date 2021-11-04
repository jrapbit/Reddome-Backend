from flask import Blueprint

api = Blueprint('api', __name__)

from .user import *
from .group import *
from .post import *
from .comment import *
