# from deta import Deta
# from ...settings import get_settings

# settings = get_settings()

# conn = Deta(settings.DATABASE_URL)

# def get_user_db() -> Deta.Base:
#     yield conn.Base("users")

# def get_one_by_key(db, k: str):
#     return db.get(k)


# def insert_one(db, obj: dict, uid: str):
#     # https://docs.deta.sh/docs/base/sdk#insert
#     item = db.insert(obj, uid)
#     return item

# def delete_all(db):
#     fetch_res = db.fetch()
#     for item in fetch_res.items:
#         db.delete(item["key"])

# def delete_one_by_key(db, k: str):
#     item = db.delete(k)
#     return item


# def fetch_all(db):
#     fetch_res = db.fetch()
#     lst = []
#     for item in fetch_res.items:
#         lst.append(item)
#     return lst

# # def fetch_all(db):
# #     res = db.fetch()
# #     all_items = res.items
# #     # fetch until last is 'None'
# #     while res.last:
# #       res = db.fetch(last=res.last)
# #       all_items += res.items
# #     return all_items