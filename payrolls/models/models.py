from sqlalchemy import ForeignKey  # noqa
from sqlalchemy.ext.declarative import declarative_base

from payrolls.models.database import Base

Base = declarative_base()
