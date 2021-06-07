from database.MongoDBConnector import MongoConnector

class Recorddata:

    db = MongoConnector.connect()
    
    userDocuments = db.userdocuments
    projectStore = db.projectstore
    teamStore = db.teamstore
