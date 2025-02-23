from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Optional
from ...services.search import SearchService
from pydantic import BaseModel

router = APIRouter()
search_service = SearchService()

class SearchResult(BaseModel):
    file_hash: str
    file_name: str
    score: float
    content: str
    section_type: str
    key_metrics: dict

@router.get("/search/semantic", response_model=List[SearchResult])
async def search_documents(
    query: str = Query(..., description="Search query"),
    top_k: int = Query(5, description="Number of results to return")
):
    """Search documents using semantic similarity."""
    try:
        results = await search_service.semantic_search(query, top_k)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis/financial")
async def analyze_financials(
    metric: str = Query(..., description="Financial metric to analyze"),
    min_value: Optional[float] = Query(None, description="Minimum value"),
    max_value: Optional[float] = Query(None, description="Maximum value")
):
    """Analyze financial metrics across documents."""
    try:
        results = await search_service.search_by_metric(metric, min_value, max_value)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis/sql")
async def run_sql_analysis(
    query: str = Query(..., description="SQL query for analysis")
):
    """Run SQL analysis on financial data."""
    try:
        results = await search_service.sql_analysis(query)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 