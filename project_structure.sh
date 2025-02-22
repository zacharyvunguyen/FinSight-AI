# Create main directories
mkdir -p {backend,frontend,scripts,config,tests,data}

# Create backend subdirectories
mkdir -p backend/{app,models,services,utils}

# Create frontend subdirectories
mkdir -p frontend/pages

# Create test subdirectories
mkdir -p tests/{unit,integration}

# Create data subdirectories
mkdir -p data/{raw,processed}

# Create empty .gitkeep files to preserve empty directories
touch data/raw/.gitkeep data/processed/.gitkeep 

# Run the test script
python scripts/test_imports.py 