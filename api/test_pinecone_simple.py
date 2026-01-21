"""Simple test to check Pinecone connection"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Checking environment variables...")
api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENVIRONMENT")
index_name = os.getenv("PINECONE_INDEX_NAME")

print(f"API Key: {api_key[:20]}..." if api_key else "API Key: NOT FOUND")
print(f"Environment: {environment}")
print(f"Index Name: {index_name}")

print("\nTrying to import Pinecone...")
try:
    from pinecone import Pinecone
    print("✅ Pinecone imported successfully!")
    
    print("\nTrying to connect...")
    pc = Pinecone(api_key=api_key)
    print("✅ Pinecone client created!")
    
    print("\nListing indexes...")
    indexes = pc.list_indexes()
    print(f"✅ Found indexes: {indexes}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
