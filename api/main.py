"""
FastAPI service for DataScouteR
This service wraps the R DataScouteR package and exposes it via REST API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
import pandas as pd

app = FastAPI(
    title="DataScouteR API",
    description="Python API wrapper for the R DataScouteR package",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import R package
try:
    datascouteR = importr('DataScouteR')
    base = importr('base')
except Exception as e:
    print(f"Warning: Could not import DataScouteR package: {e}")
    datascouteR = None


# Request/Response Models
class DataScoutRequest(BaseModel):
    data: List[Dict[str, Any]]
    options: Optional[Dict[str, Any]] = {}


class DataScoutResponse(BaseModel):
    success: bool
    result: Any
    message: Optional[str] = None


# Helper function to convert between Python and R
def python_to_r_dataframe(data: List[Dict[str, Any]]):
    """Convert Python list of dicts to R dataframe"""
    df = pd.DataFrame(data)
    with localconverter(ro.default_converter + pandas2ri.converter):
        return ro.conversion.py2rpy(df)


def r_to_python(r_obj):
    """Convert R object to Python"""
    try:
        with localconverter(ro.default_converter + pandas2ri.converter):
            return ro.conversion.rpy2py(r_obj)
    except:
        # Fallback to string representation
        return str(r_obj)


# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "DataScouteR API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "r_package_loaded": datascouteR is not None
    }


@app.get("/gk", response_model=DataScoutResponse)
async def get_goalkeepers():
    """
    Get goalkeeper data using DataScouteR's get_gk() function
    """
    if datascouteR is None:
        raise HTTPException(status_code=500, detail="DataScouteR package not loaded")
    
    try:
        # Call R function get_gk()
        r_result = datascouteR.get_gk()
        
        # Convert R dataframe to pandas, then to dict
        python_result = r_to_python(r_result)
        
        # Convert to list of dicts if it's a DataFrame
        if hasattr(python_result, 'to_dict'):
            result_data = python_result.to_dict(orient='records')
        else:
            result_data = python_result
        
        return DataScoutResponse(
            success=True,
            result=result_data,
            message="Goalkeeper data retrieved successfully"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fw", response_model=DataScoutResponse)
async def get_forwards():
    """
    Get forward player data using DataScouteR's get_fw() function
    
    """
    if datascouteR is None:
        raise HTTPException(status_code=500, detail="DataScouteR package not loaded")
    
    try:
        # Call R function get_fw()
        r_result = datascouteR.get_fw()
        
        # Convert R dataframe to pandas, then to dict
        python_result = r_to_python(r_result)
        
        # Convert to list of dicts if it's a DataFrame
        if hasattr(python_result, 'to_dict'):
            result_data = python_result.to_dict(orient='records')
        else:
            result_data = python_result
        
        return DataScoutResponse(
            success=True,
            result=result_data,
            message="Forward data retrieved successfully"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)