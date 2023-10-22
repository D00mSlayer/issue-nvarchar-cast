from sqlalchemy import Column, String, Unicode, BigInteger
from sqlalchemy import create_engine
from z3c.sqlalchemy.mapper import MappedClassBase
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


class CustomMappedClassBase(MappedClassBase):
    @property
    def session(self):
        return object_session(self)

    def query(self, *args, **argd):
        return self.session.query(*args, **argd)


sqla_meta_data = MetaData()
DBEntity = declarative_base(name='DBEntity', metadata=sqla_meta_data, cls=CustomMappedClassBase)


class EntityGetter(object):
    def __getattr__(self, entity_name):
        entity = DBEntity._decl_class_registry.get(entity_name)
        if not entity:
            raise AttributeError(f'{entity_name} was not imported.')
        return entity


db = EntityGetter()


class T_VARCHAR(DBEntity):
    __tablename__ = 't_varchar'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))


def create_session():
    engine = create_engine('mssql+pyodbc://SA:Jiva@123@test_2022')
    DBEntity.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine))
