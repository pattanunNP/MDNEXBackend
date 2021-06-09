from database.MongoDBConnector import MongoConnector


class Recorddata:

    db = MongoConnector.connect()

    userDB = db.usersdata
    userDocuments = db.userdocuments
    projectStore = db.projectstore
    teamStore = db.teamstore
