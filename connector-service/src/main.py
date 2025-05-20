import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.database import fetch_data
from src.gemini_client import generate_sql
from src.database import execute_sql

app = FastAPI()

class NLQueryRequest(BaseModel):
    prompt: str



@app.post("/nlquery")
async def nlquery_endpoint(request: NLQueryRequest):
    try:
        table_schema = "sample_data(id SERIAL PRIMARY KEY, content TEXT, created_at TIMESTAMP)"
        
        sql = generate_sql(request.prompt, table_schema)
        data = execute_sql(sql)
        return {"generated_sql": sql, "results": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

class ExecuteRequest(BaseModel):
    prompt: str
    #schema: str = ""  

@app.post("/execute")
async def execute_endpoint(request: ExecuteRequest):
    try:
        # Generate SQL from Gemini
        sql = generate_sql(request.prompt, request.schema)

        # Execute SQL against database
        result = execute_sql(sql)

        return {
            "generated_sql": sql,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))