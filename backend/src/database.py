from sqlmodel import create_engine, Session, SQLModel

# Use an in-memory SQLite database for testing and development by default
# IMPORTANT: For production, this should be a proper PostgreSQL URL from an environment variable.
DATABASE_URL = "sqlite:///./database.db" # This will create a file-based SQLite database

# For production/deployment, uncomment and configure an environment variable:
# import os
# DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@host:port/database")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
