def test_imports():
    packages = {
        'Basic Data Science': ['pandas', 'numpy'],
        'Web Framework': ['fastapi', 'uvicorn', 'pydantic'],
        'UI': ['streamlit'],
        'PDF Processing': ['PyPDF2', 'pdfplumber'],
        'AI/ML': [
            'openai',
            'langchain',
            'sentence_transformers',
            'pinecone',
            'llama_index'
        ],
        'Cloud Services': ['google.cloud.bigquery', 'google.cloud.storage'],
        'Document Processing': ['llama_parse'],
        'Development Tools': ['pytest', 'black', 'isort'],
        'Utilities': ['requests', 'dotenv']
    }
    
    failed_imports = []
    
    print("Testing package imports...")
    for category, package_list in packages.items():
        print(f"\n{category}:")
        for package in package_list:
            try:
                exec(f"import {package}")
                print(f"✅ {package}")
            except ImportError as e:
                failed_imports.append((package, str(e)))
                print(f"❌ {package}")
    
    if failed_imports:
        print("\n❌ Some packages failed to import:")
        for package, error in failed_imports:
            print(f"  - {package}: {error}")
    else:
        print("\n✅ All packages imported successfully!")

if __name__ == "__main__":
    test_imports() 