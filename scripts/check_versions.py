def check_versions():
    import sys
    print(f"Python version: {sys.version}")
    
    packages = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'streamlit': 'streamlit',
        'pydantic': 'pydantic',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'PyPDF2': 'PyPDF2',
        'pdfplumber': 'pdfplumber',
        'openai': 'openai',
        'langchain': 'langchain',
        'sentence_transformers': 'sentence-transformers',
        'pinecone': 'pinecone',
        'llama_index': 'llama-index',
        'llama_parse': 'llama-parse',
        'google.cloud.bigquery': 'google-cloud-bigquery',
        'google.cloud.storage': 'google-cloud-storage',
        'requests': 'requests',
        'black': 'black',
        'isort': 'isort',
        'pytest': 'pytest'
    }
    
    print("\nPackage Versions:")
    print("-" * 40)
    
    for import_name, package_name in packages.items():
        try:
            module = __import__(import_name.split('.')[0])
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {package_name}: {version}")
        except ImportError as e:
            print(f"❌ {package_name}: Not installed - {str(e)}")

if __name__ == "__main__":
    check_versions() 