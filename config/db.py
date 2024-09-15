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
        
    def get_item_from_collection_by_id(self, collection_name, item_id):
        """Devuelve un item de una colección MongoDB por su id."""
        try:
            collection = self.db[collection_name]
            item = collection.find_one({"_id": item_id})
            if item:
                item['id'] = str(item.pop('_id'))
                return item
            else:
                print(f"Item {item_id} not found in collection {collection_name}")

            return item 
        except Exception as e:
            print(f"Error fetching item {item_id} from collection {collection_name}: {e}")
            return None
        
    def insert_item_into_collection(self, collection_name, item):
        """Inserta un item en una colección MongoDB."""
        try:
            collection = self.db[collection_name]
            return collection.insert_one(item)
        except Exception as e:
            print(f"Error inserting item into collection {collection_name}: {e}")
            return None
