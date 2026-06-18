from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from bson.objectid import ObjectId


class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB"""

    def __init__(self, username='aacuser', password='SNHU1234'):
        """
        Initialize MongoDB client with aacuser credentials.
        Update the password below as needed for your environment.
        """
        USER = 'aacuser'
        PASS = 'SNHU1234' 
        HOST = 'localhost'
        PORT = 27017
        DB = 'aac'
        COL = 'animals'

        try:
            # Establish the MongoDB connection
            self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}/{DB}')   
            self.database = self.client[DB]
            self.collection = self.database[COL]
        except ConnectionFailure as e:
            print(f"Connection failed: {e}")
            raise

    def create(self, data):
        """
        Inserts a single document into the collection.
        :param data: dict - the document to insert.
        :return: True if successful, False otherwise.
        """
        if data is not None and isinstance(data, dict):
            try:
                result = self.collection.insert_one(data)
                return result.acknowledged
            except OperationFailure as e:
                print(f"Insert failed: {e}")
                return False
        else:
            raise Exception("Nothing to save. The data parameter is empty or not a dictionary.")

    def read(self, query):
        """
        Queries documents from the collection based on the filter.
        :param query: dict - the filter to apply.
        :return: list of matching documents, or empty list.
        """
        if query is not None and isinstance(query, dict):
            try:
                result = self.collection.find(query)
                return list(result)
            except OperationFailure as e:
                print(f"Query failed: {e}")
                return []
        else:
            raise Exception("Invalid query. The query parameter must be a dictionary.")
            
    
    def update(self, query, new_values):
        """
        Updates document(s) based on the provided query.
        :param query: dict - the filter to select documents.
        :param new_values: dict - the fields and values to update.
        :return: int - number of documents modified.
        """
        if isinstance(query, dict) and isinstance(new_values, dict):
            try:
                result = self.collection.update_many(query, {'$set': new_values})
                return result.modified_count
            except OperationFailure as e:
                print(f"Update failed: {e}")
                return 0
        else:
            raise Exception("Both query and new_values must be dictionaries.")
            
    def delete(self, query):
        """
        Deletes document(s) from the collection based on the query.
        :param query: dict - the filter to select documents to delete.
        :return: int - number of documents deleted.
        """
        if isinstance(query, dict):
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except OperationFailure as e:
                print(f"Delete failed: {e}")
                return 0
        else:
            raise Exception("Query must be a dictionary.")