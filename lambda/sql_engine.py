import os
import psycopg2
from psycopg2 import pool
from typing import List, Dict
from dotenv import load_dotenv
from contextlib import contextmanager

class SQLEngine:
    def __init__(self, 
                 host: str, 
                 database: str, 
                 user: str, 
                 password: str, 
                 minconn: int= 1, 
                 maxconn: int= 5) -> None:
        self.pool = pool.SimpleConnectionPool(
            minconn= minconn,
            maxconn= maxconn,
            host= host,
            database= database,
            user= user,
            password= password
        )
        self.rate_limit_enabled = True

    @contextmanager
    def get_cursor(self) -> psycopg2.extensions.cursor:
        conn = self.pool.getconn()
        try:
            yield conn.cursor()
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.pool.putconn(conn)

    def execute_query(self, query, insert_data: tuple=None) -> None:
        with self.get_cursor() as cursor:
            cursor.execute(query, insert_data)
    
    def execute_insert_query(self, query, insert_data: tuple=None) -> None:
        with self.get_cursor() as cursor:
            cursor.execute(query, insert_data)
            
    def execute_select_query(self, query, select_data: tuple=None) -> List:
        with self.get_cursor() as cursor:
            cursor.execute(query, select_data)
            return cursor.fetchall()
    