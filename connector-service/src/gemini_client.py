import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-pro-latest')

def analyze_data(prompt: str, data: dict):
    full_prompt = f"""
    Database Schema: {data['columns']}
    Sample Data: {data['data']}
    
    Task: {prompt}
    """
    response = model.generate_content(full_prompt)
    return response.text

def generate_sql(nl_prompt: str, table_schema: str):
    prompt = f"""
You are a SQL expert. Based on the schema below, write a SQL SELECT query that fulfills the user's request.

Schema:
{table_schema}

User Request:
{nl_prompt}

Respond with only the SQL query. Do not include explanations, markdown, or formatting.
"""
    response = model.generate_content(prompt)
    raw_sql = response.text.strip()

    # Clean output if Gemini still returns markdown formatting
    cleaned_sql = re.sub(r"```sql|```", "", raw_sql, flags=re.IGNORECASE).strip()

    # Optionally just extract the first valid statement
    return cleaned_sql.split(";")[0] + ";"

