from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import session
from app.c_models import *
from app.sd_models import *
from sqlalchemy.orm import aliased
import sqlalchemy as sa
from sqlalchemy_utils import (
    create_view,
)


db = SQLAlchemy()
