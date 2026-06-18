import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, DB_COLLECTION

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnimalShelter:
    """CRUD operations for the Animal collection in MongoDB."""

    def __init__(self):
        try:
            connection_string = f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            self.client = MongoClient(connection_string)
            self.database = self.client[DB_NAME]
            self.collection = self.database[DB_COLLECTION]
            self.create_indexes()
            logger.info("Connected to MongoDB database.")
        except ConnectionFailure as error:
            logger.error("MongoDB connection failed: %s", error)
            raise

    def create(self, data):
        if not isinstance(data, dict) or not data:
            raise ValueError("Data must be a non-empty dictionary.")

        self.validate_animal_document(data)

        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        except OperationFailure as error:
            logger.error("Insert failed: %s", error)
            return False

    def read(self, query=None):
        if query is None:
            query = {}

        if not isinstance(query, dict):
            raise ValueError("Query must be a dictionary.")

        try:
            return list(self.collection.find(query))
        except OperationFailure as error:
            logger.error("Query failed: %s", error)
            return []

    def update(self, query, new_values):
        if not isinstance(query, dict) or not isinstance(new_values, dict):
            raise ValueError("Query and new_values must be dictionaries.")

        try:
            result = self.collection.update_many(query, {"$set": new_values})
            return result.modified_count
        except OperationFailure as error:
            logger.error("Update failed: %s", error)
            return 0

    def delete(self, query):
        if not isinstance(query, dict):
            raise ValueError("Query must be a dictionary.")

        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except OperationFailure as error:
            logger.error("Delete failed: %s", error)
            return 0
        
    def create_indexes(self):
        """Create indexes for frequently queried fields."""

        self.collection.create_index("breed")
        self.collection.create_index("age_upon_outcome_in_weeks")
        self.collection.create_index("sex_upon_outcome")

        logger.info("Database indexes created.")

    
    def validate_animal_document(self, data):
        """Validate required fields before inserting a document."""

        required_fields = [
            "animal_id",
            "animal_type",
            "breed",
            "sex_upon_outcome",
            "age_upon_outcome_in_weeks"
        ]

        missing_fields = [
            field for field in required_fields
            if field not in data or data[field] in [None, ""]
        ]

        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")

        if not isinstance(data.get("age_upon_outcome_in_weeks"), (int, float)):
            raise ValueError("age_upon_outcome_in_weeks must be a number.")

        return True
    
    def get_breed_statistics(self, limit=10):
        """Use an aggregation pipeline to count animals by breed."""

        pipeline = [
            {
                "$group": {
                    "_id": "$breed",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"count": -1}
            },
            {
                "$limit": limit
            }
        ]

        try:
            results = list(self.collection.aggregate(pipeline))

            return [
                {
                    "breed": item["_id"],
                    "count": item["count"]
                }
                for item in results
            ]

        except OperationFailure as error:
            logger.error("Aggregation failed: %s", error)
            return []