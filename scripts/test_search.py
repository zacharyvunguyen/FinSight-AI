import asyncio
from dotenv import load_dotenv
from backend.app.services.search import SearchService

async def test_search():
    """Test search functionality."""
    load_dotenv()
    
    print("\n🔍 Testing Search Functionality")
    print("-" * 50)
    
    search_service = SearchService()
    
    try:
        # Test semantic search
        print("\n1. Testing Semantic Search")
        print("-" * 30)
        results = await search_service.semantic_search(
            query="What is the company's revenue growth?",
            top_k=3
        )
        print(f"Found {len(results)} matches")
        for i, result in enumerate(results, 1):
            print(f"\nMatch {i}:")
            print(f"File: {result['file_name']}")
            print(f"Score: {result['score']:.4f}")
            print(f"Preview: {result['content'][:200]}...")
        
        # Test metric search
        print("\n2. Testing Metric Search")
        print("-" * 30)
        metric_results = await search_service.search_by_metric(
            metric="Revenue",
            min_value=1000000
        )
        print(f"Found {len(metric_results)} documents with revenue > $1M")
        
        print("\n✅ Search tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Search test failed: {str(e)}")
        raise e

if __name__ == "__main__":
    asyncio.run(test_search()) 