# import pymongo
# from app.config import Config
# from datetime import datetime
#
#
# class PyMongoDB(object):
#     def __init__(self):
#         self.client = pymongo.MongoClient(Config.MONGO_DATABASE_URI)
#         self.mydb = self.client[Config.MONGO_DATABASE_NAME]
#
#     def generateMongoCollection(self, companyId):
#         today = datetime.utcnow().date()
#         month = today.month
#         year = today.year
#         collection_name = "{}/{}/{}".format(str(companyId), str(month), str(year))
#         return collection_name, True
#
#     def insertOne(self, collection_name, filtered_data_id, record_id, smartpixl_data):
#         collection = self.mydb[collection_name]
#         entry = {'_id': filtered_data_id, "record_id": record_id, "data": smartpixl_data}
#         mongo_insertion = collection.insert_one(entry)
#         return mongo_insertion.inserted_id, True
#         #
#         # except Exception as e:
#         #     return "bulkInsertError: %s" % str(e), False
