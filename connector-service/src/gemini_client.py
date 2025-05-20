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

def generate_sql(prompt: str, schema: str = ""):
    full_prompt = f"""
You are an advanced PostgreSQL assistant. Your task is to generate valid SQL statements to fully manage the database. 
You may receive tasks such as querying data, creating tables, inserting data, updating records, or managing triggers.

Schema (if available):
{schema if schema else "None"}

Task:
{prompt}

Output only valid PostgreSQL SQL code. Do not include explanations, markdown, or comments.
Ensure the SQL is executable in psql.
"""
    response = model.generate_content(full_prompt)
    return response.text.strip()
