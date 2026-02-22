from pymongo import MongoClient

db = MongoClient("mongodb+srv://sriram65raja:1324sriram@cluster0.dejys.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db_Intilize = db['codebase']
PROBLMES = db_Intilize['PROBLMES_LIST']


