"""Direct test without .env file - no emojis"""
import os

# Set environment variables directly
os.environ["PINECONE_API_KEY"] = "pcsk_39HByP_HmgWyvvErTPshchujfMB6saU9jKYjge9P3G7C5xoSbHZK2WPvYRNcETys5pgjDo"
os.environ["PINECONE_ENVIRONMENT"] = "us-east-1"
os.environ["PINECONE_INDEX_NAME"] = "code-reviewer"
os.environ["GOOGLE_AI_API_KEY"] = "AIzaSyDdlC-VQ4BJLrJSSgag_EbXO4Blrqr55g"

print("=" * 60)
print("Testing Pinecone Connection (Direct)")
print("=" * 60)

try:
    print("\n[1] Importing Pinecone...")
    from pinecone import Pinecone
    print("[OK] Pinecone imported!")
    
    print("\n[2] Creating Pinecone client...")
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    print("[OK] Client created!")
    
    print("\n[3] Listing indexes...")
    indexes = pc.list_indexes()
    print(f"[OK] Found indexes: {indexes.names()}")
    
    print("\n[4] Connecting to index...")
    index = pc.Index("code-reviewer")
    print("[OK] Connected to index!")
    
    print("\n[5] Getting index stats...")
    stats = index.describe_index_stats()
    print(f"[OK] Index stats: {stats}")
    
    print("\n" + "=" * 60)
    print("SUCCESS! Pinecone connection successful!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
