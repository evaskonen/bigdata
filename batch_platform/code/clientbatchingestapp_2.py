from mysimbdp import insert_files

# PROGRAM FOR CUSTOMER B

# open database connection with MongoDB and PyMongo
#client = MongoClient(['localhost:27017', 'localhost:27018', 'localhost:27019'], replicaset='replicaset0')
def ingest(files):
    # create database
    database_name = 'CUSTOMER_B'

    insert_files(database_name, files)
    print("Data inserted into database.")
