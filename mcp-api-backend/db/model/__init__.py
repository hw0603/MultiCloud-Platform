from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [
    basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')
]
from db.model import *


# 모든 모델을 import
# 참고) https://stackoverflow.com/questions/9088957/sqlalchemy-cannot-find-a-class-name
"""
From the SQLAlchemy documentation:
However, due to the behavior of SQLAlchemy's "declarative" configuration mode,
all modules which hold active SQLAlchemy models need to be imported before those models can successfully be used.
So, if you use model classes with a declarative base,
you need to figure out a way to get all your model modules imported to be able to use them in your application.
"""
