from model import (
    Insert_T_VARCHAR,
    Get_T_VARCHAR
)
from entities import create_session
from sqlalchemy import event
from sqlalchemy.engine.base import Engine
import pyodbc


@event.listens_for(Engine, "connect")
def do_configure_connection_encoding(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, pyodbc.Connection):
        pass
        # dbapi_connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        # dbapi_connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        # dbapi_connection.setencoding(encoding='utf-8')


ascii_chars = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
context = {'session': create_session()}

saved_ids = []
model = Insert_T_VARCHAR({'name': ascii_chars}, context=context)
new_id = model.save()
saved_ids.append(new_id)

model = Get_T_VARCHAR({'ids': saved_ids}, context=context)
print(model.get_all())
