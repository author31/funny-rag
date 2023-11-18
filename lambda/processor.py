import os

class Processor:
    def __init__(self):
        self.conn = os.getenv("POSTGRESQL_URL")

    def init_db(self):
        pass

    def init_open_ai_client(self):
        pass
    
    def execute_query(self):
        pass
    
    def add_pgvector(self):
        pass
    
    def create_hn_embeddings_table(self):
        pass
    
    def insert_into_embeddings_table(self):
        pass
    
    def transform(self):
        pass
    
    def fetch_top_stories(self):
        pass
    
    def fetch(self):
        pass