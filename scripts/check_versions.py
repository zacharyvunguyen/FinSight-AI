def check_versions():
    import sys
    print(f"Python version: {sys.version}")
    
    packages = {
        'fastapi': 'fastapi',
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'PyPDF2': 'PyPDF2',
        'pdfplumber': 'pdfplumber',
        'openai': 'openai',
        'langchain': 'langchain',
        'sentence_transformers': 'sentence_transformers',
        'pinecone': 'pinecone',
        'google.cloud.bigquery': 'google-cloud-bigquery',
        'google.cloud.storage': 'google-cloud-storage'
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