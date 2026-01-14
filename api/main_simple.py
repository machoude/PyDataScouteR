from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Optional
import json
import os

app = FastAPI(title="DataScouteR API", version="1.0.0")

class DataScoutResponse(BaseModel):
    success: bool
    result: Any
    message: Optional[str] = None

# Load real data from JSON files
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return []

GK_DATA = load_data('gk_data.json')
FW_DATA = load_data('fw_data.json')

@app.get("/")
async def root():
    return {"message": "DataScouteR API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/gk")
async def get_gk():
    return DataScoutResponse(success=True, result=GK_DATA)

@app.get("/fw")
async def get_fw():
    return DataScoutResponse(success=True, result=FW_DATA)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
