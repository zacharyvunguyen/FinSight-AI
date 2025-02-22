# FinSight-AI

An intelligent system for analyzing, comparing, and extracting insights from financial closing books and reports using AI and machine learning.

## 🎯 Features

- **PDF Data Extraction**: Automatically extract structured financial data from PDF reports
- **Change Detection**: Identify material changes between different versions of financial reports
- **AI-Powered Search**: Natural language querying of financial data and insights
- **Data Warehousing**: Store structured financial data in BigQuery for SQL analysis
- **Vector Search**: Utilize Pinecone for semantic search and AI-powered retrieval

## 🏗️ Technical Architecture

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Data Storage**: 
  - BigQuery (structured data)
  - Pinecone (vector embeddings)
- **AI/ML**: 
  - OpenAI GPT-4 (text analysis)
  - LangChain (AI orchestration)
  - Sentence Transformers (embeddings)

## 📁 Project Structure

FinSight-AI/
├── backend/
│   ├── app/
│   ├── models/
│   ├── services/
│   └── utils/
├── frontend/
│   └── pages/
├── scripts/
│   ├── verify_env.py
│   └── test_imports.py
├── config/
├── tests/
│   ├── unit/
│   └── integration/
├── data/
│   ├── raw/
│   └── processed/
├── .env
├── .gitignore
├── environment.yml
└── README.md

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/zacharyvunguyen/FinSight-AI.git
   cd FinSight-AI
   ```

2. Set up the environment:
   ```bash
   # Create and activate conda environment
   conda env create -f environment.yml
   conda activate finsight-ai
   ```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your API keys and configurations:
     - OPENAI_API_KEY
     - PINECONE_API_KEY
     - GOOGLE_CLOUD_PROJECT
     - Other required variables

4. Verify setup:
   ```bash
   # Run environment verification
   python scripts/verify_env.py
   
   # Test package imports
   python scripts/test_imports.py
   ```

## 🛠️ Development

### Backend (FastAPI)
- API endpoints for PDF processing
- Financial data extraction and analysis
- Integration with AI services

### Frontend (Streamlit)
- Interactive dashboard
- File upload interface
- Query and visualization tools

### Data Processing
- PDF text extraction
- Financial data structuring
- Vector embedding generation

## 📊 Data Storage

### BigQuery
- Structured financial data
- Historical records
- Analysis results

### Pinecone
- Vector embeddings
- Semantic search capabilities
- AI-powered retrieval

## 🧪 Testing

```bash
# Run unit tests
pytest tests/unit

# Run integration tests
pytest tests/integration
```

## 📝 Documentation

- API documentation available at `/docs` when running the backend
- Frontend user guide in `/frontend/README.md`
- Development guidelines in `/docs`

## 🔐 Security

- Environment variables for sensitive data
- API authentication required
- Data encryption in transit and at rest

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.