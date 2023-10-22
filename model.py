from custom_base_model import CustomModel
from schematics.types import StringType, IntType
from schematics.types.compound import ListType
from entities import db


class Insert_T_VARCHAR(CustomModel):
    name = StringType()

    def save(self):
        session = self.session
        t_varchar = self.to_db_entity(db.T_VARCHAR)
        session.add(t_varchar)
        session.flush()
        return t_varchar.id

class Get_T_VARCHAR(CustomModel):
	id = IntType()
	ids = ListType(IntType)

	def get(self):
		session = self.session
		return session.query(db.T_VARCHAR.name).filter(db.T_VARCHAR.id == self.id).all()

	def get_all(self):
		session = self.session
		return session.query(db.T_VARCHAR.name).filter(db.T_VARCHAR.id.in_(self.ids)).all()
