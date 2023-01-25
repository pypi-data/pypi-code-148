from darmilibs.darmi.database import db_x

darmi = db_x["Zaid"]["rraid"]


async def rraid_user(chat):
    doc = {"_id": "Rraid", "users": [chat]}
    r = await darmi.find_one({"_id": "Rraid"})
    if r:
        await darmi.update_one({"_id": "Rraid"}, {"$push": {"users": chat}})
    else:
        await darmi.insert_one(doc)


async def get_rraid_users():
    results = await darmi.find_one({"_id": "Rraid"})
    if results:
        return results["users"]
    else:
        return []


async def unrraid_user(chat):
    await darmi.update_one({"_id": "Rraid"}, {"$pull": {"users": chat}})
