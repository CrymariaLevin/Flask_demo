from resources.base import BaseDb

bd = BaseDb()

# sql = "select * from `flask_test_unit`"
sql = "select * from `flask_test_type`"
bd.dict_cur.execute(sql)
r_id = bd.dict_cur.fetchall()
print(r_id)

