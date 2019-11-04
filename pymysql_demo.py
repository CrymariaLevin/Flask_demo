from resources.base import BaseDb

bd = BaseDb()

sql = "select * from `hcb_factory_price_key` where `factory` = '昌邑石化（江阴油库）'"
bd.dict_cur.execute(sql)
r_id = bd.dict_cur.fetchone()
print(r_id)

