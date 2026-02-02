import psycopg2
from psycopg2 import pool, Error
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import pandas as pd
from typing import Optional, List, Tuple, Dict, Any
from contextlib import contextmanager

load_dotenv(".env")

_connection_pool = None

def get_db_params() -> Dict[str, Any]:
    return {
        'host': os.getenv('RDS_HOST'),
        'database': os.getenv('RDS_DATABASE'),
        'user': os.getenv('RDS_USER'),
        'password': os.getenv('RDS_PASSWORD'),
        'port': os.getenv('RDS_PORT'),
        'sslmode': 'require',
        'connect_timeout': 10,
    }

def create_connection_pool(min_conn: int = 1, max_conn: int = 10) -> Optional[pool.SimpleConnectionPool]:
    global _connection_pool
    try:
        db_params = get_db_params()
        _connection_pool = pool.SimpleConnectionPool(min_conn, max_conn, **db_params)
        print(f"Connection pool created successfully with {min_conn}-{max_conn} connections")
        return _connection_pool
    except Error as e:
        print(f"Error creating connection pool: {e}")
        return None

def get_connection_from_pool():
    if not _connection_pool:
        print("Connection pool not created. Creating default pool...")
        create_connection_pool()
    
    try:
        return _connection_pool.getconn()
    except Error as e:
        print(f"Error getting connection from pool: {e}")
        return None

def return_connection_to_pool(connection):
    if _connection_pool and connection:
        _connection_pool.putconn(connection)

def create_single_connection() -> Optional[psycopg2.extensions.connection]:
    try:
        db_params = get_db_params()
        connection = psycopg2.connect(**db_params)
        print("Single connection established successfully")
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def close_connection_pool():
    global _connection_pool
    if _connection_pool:
        _connection_pool.closeall()
        _connection_pool = None
        print("Connection pool closed")

@contextmanager
def get_db_connection(use_pool: bool = True):
    connection = None
    try:
        if use_pool and _connection_pool:
            connection = get_connection_from_pool()
        else:
            connection = create_single_connection()
        
        yield connection
        
    except Error as e:
        print(f"Database error: {e}")
        if connection:
            connection.rollback()
        raise
    finally:
        if connection:
            if use_pool and _connection_pool:
                return_connection_to_pool(connection)
            else:
                connection.close()

@contextmanager
def get_db_cursor(use_pool: bool = True, cursor_factory=None):
    with get_db_connection(use_pool) as connection:
        cursor = connection.cursor(cursor_factory=cursor_factory)
        try:
            yield cursor
            connection.commit()
        except Error as e:
            connection.rollback()
            print(f"Query execution error: {e}")
            raise
        finally:
            cursor.close()

def execute_query(query: str, params: Tuple = None, fetch: bool = True, 
                  use_pool: bool = True) -> Optional[Any]:
    try:
        with get_db_cursor(use_pool) as cursor:
            cursor.execute(query, params)
            
            if fetch and query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                return results, column_names
            else:
                return cursor.rowcount
                
    except Error as e:
        print(f"Error executing query: {e}")
        return None

def execute_query_pandas(query: str, params: Tuple = None, 
                         use_pool: bool = True) -> Optional[pd.DataFrame]:
    try:
        results, columns = execute_query(query, params, fetch=True, use_pool=use_pool)
        if results:
            df = pd.DataFrame(results, columns=columns)
            return df
        return pd.DataFrame()
    except Exception as e:
        print(f"Error converting to DataFrame: {e}")
        return None

def execute_query_dict(query: str, params: Tuple = None, 
                       use_pool: bool = True) -> Optional[List[Dict]]:
    try:
        with get_db_cursor(use_pool, cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return [dict(row) for row in results]
            else:
                return cursor.rowcount
                
    except Error as e:
        print(f"Error executing query with dict cursor: {e}")
        return None

def execute_many(query: str, params_list: List[Tuple], 
                 use_pool: bool = True) -> Optional[int]:
    try:
        with get_db_cursor(use_pool) as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount
    except Error as e:
        print(f"Error executing multiple queries: {e}")
        return None

def execute_transaction(queries: List[Tuple[str, Tuple]], 
                        use_pool: bool = True) -> bool:
    try:
        with get_db_connection(use_pool) as connection:
            cursor = connection.cursor()
            try:
                for query, params in queries:
                    cursor.execute(query, params)
                connection.commit()
                print("Transaction completed successfully")
                return True
            except Error as e:
                connection.rollback()
                print(f"Transaction failed: {e}")
                return False
            finally:
                cursor.close()
    except Error as e:
        print(f"Connection error in transaction: {e}")
        return False

def test_connection() -> bool:
    try:
        with get_db_connection(use_pool=False) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result and result[0] == 1:
                    print("Database connection test passed")
                    return True
        return False
    except Error as e:
        print(f"Database connection test failed: {e}")
        return False

def get_table_info(table_name: str) -> Optional[List[Dict]]:
    query = """
    SELECT column_name, data_type, is_nullable, column_default
    FROM information_schema.columns
    WHERE table_name = %s
    ORDER BY ordinal_position;
    """
    return execute_query_dict(query, (table_name,))

def get_table_row_count(table_name: str) -> Optional[int]:
    """Get row count for a table"""
    query = f"SELECT COUNT(*) FROM {table_name}"
    try:
        result, _ = execute_query(query, fetch=True)
        return result[0][0] if result else None
    except Error as e:
        print(f"Error getting row count: {e}")
        return None

def create_table_if_not_exists(table_name: str, schema: str) -> bool:
    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {schema}
    );
    """
    try:
        execute_query(query, fetch=False)
        print(f"Table '{table_name}' created or already exists")
        return True
    except Error as e:
        print(f"Error creating table: {e}")
        return False

if __name__ == "__main__":  
    if test_connection():
        create_connection_pool()

        with get_db_cursor() as cursor:
            cursor.execute("SELECT version()")
            result = cursor.fetchone()
            print(f"PostgreSQL Version: {result[0]}")
        
        close_connection_pool()