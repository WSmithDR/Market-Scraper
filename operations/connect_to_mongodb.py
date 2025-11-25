import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient


def connect_to_mongodb():
    """
    Connect to MongoDB using credentials from .env file.
    
    Returns:
        dict: Dictionary containing 'client' and 'collection' if successful, None otherwise
    """
    try:
        # Get the project root directory (one level up from operations/)
        project_root = Path(__file__).parent.parent
        env_path = project_root / ".env"
        
        print(f"Looking for .env at: {env_path}")
        
        # Load environment variables
        if not load_dotenv(dotenv_path=env_path, override=True):
            print(" .env file not found in project root. Trying current directory...")
            if not load_dotenv(override=True):
                raise FileNotFoundError("Could not find .env file in project root or current directory")
        
        # Get credentials
        mongo_uri = os.getenv("MONGODB_URI")
        db_name = os.getenv("MONGODB_DB")
        collection_name = os.getenv("MONGODB_COLLECTION")
        
        if not all([mongo_uri, db_name, collection_name]):
            missing = []
            if not mongo_uri: missing.append("MONGODB_URI")
            if not db_name: missing.append("MONGODB_DB")
            if not collection_name: missing.append("MONGODB_COLLECTION")
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        # Create connection and test it
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # 5 second timeout
        client.admin.command('ping')  # Test the connection
        
        # Get database and collection
        db = client[db_name]
        collection = db[collection_name]
        
        # Create index if it doesn't exist
        collection.create_index([("job_url", 1)], unique=True)
        
        print("✅ Successfully connected to MongoDB")
        print(f"📊 Database: {db_name}")
        print(f"📂 Collection: {collection_name}")
        print(f"🔗 Total documents: {collection.estimated_document_count()}")
        
        return {
            'client': client,  # Keep the client to close it later
            'collection': collection
        }
        
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {str(e)}")
        return None