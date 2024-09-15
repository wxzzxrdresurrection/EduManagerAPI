from pymongo import MongoClient
import os

class MongoConnection:
    _instance = None  # Variable de clase para el patrón Singleton

    def __new__(cls):
        """Controla la creación de una única instancia (Singleton)."""
        if cls._instance is None:
            cls._instance = super(MongoConnection, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Se inicializa solo una vez."""
        if not self._initialized:
            self._initialized = True
            mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://devluiszapata:99zvOAejXk6cPnyc@edumanager.ac5ko.mongodb.net/?retryWrites=true&w=majority&appName=EduManager")  
            self.client = MongoClient(mongo_uri, tlsAllowInvalidCertificates=True)
            print("Mongo URI:", mongo_uri)
            self.db = self.client.get_database("EduManager")  
            self.test_connection()

    def test_connection(self):
        """Prueba si la conexión es exitosa."""
        try:
            self.client.server_info()  
            print("Connection to MongoDB successful")
            return True
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            return False

    def get_collection(self, collection_name):
        """Devuelve una colección MongoDB."""
        try:
            collection = self.db[collection_name]
            return collection.find()
        except Exception as e:
            print(f"Error fetching collection {collection_name}: {e}")
            return None
