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
    db_connection = None
    try:
        if use_pool and _connection_pool:
            db_connection = get_connection_from_pool()
        else:
            db_connection = create_single_connection()
        
        yield db_connection
        
    except Error as e:
        print(f"Database error: {e}")
        if db_connection:
            db_connection.rollback()
        raise
    finally:
        if db_connection:
            if use_pool and _connection_pool:
                return_connection_to_pool(db_connection)
            else:
                db_connection.close()

@contextmanager
def get_db_cursor(use_pool: bool = True, cursor_factory=None):
    with get_db_connection(use_pool) as db_connection:
        cursor = db_connection.cursor(cursor_factory=cursor_factory)
        try:
            yield cursor
            db_connection.commit()
        except Error as e:
            db_connection.rollback()
            print(f"Query execution error: {e}")
            raise
        finally:
            cursor.close()