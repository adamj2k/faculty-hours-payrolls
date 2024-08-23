from sqlalchemy import ForeignKey  # noqa
from sqlalchemy import TIMESTAMP, Column, Integer, Double, String, Table, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from payrolls.models.database import Base

Base = declarative_base()

