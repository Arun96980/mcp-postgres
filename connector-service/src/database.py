import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "mcp-postgres"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("DB_PORT", 5432)
    )

def fetch_data(query: str, limit: int = 10):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Add LIMIT only if not present in query
    final_query = query.strip().rstrip(';')
    
    
    cursor.execute(final_query)
    columns = [desc[0] for desc in cursor.description]
    results = cursor.fetchall()
    conn.close()
    return {"columns": columns, "data": results}

def execute_sql(query: str, params: tuple = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())

        # Return data only for SELECT queries
        if query.strip().lower().startswith("select"):
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            return {"columns": columns, "data": results}
        else:
            conn.commit()
            return {"status": "success"}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
