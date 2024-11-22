from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Define the Base model
Base = declarative_base()

# Define the ScrapedData model (Table schema)
class ScrapedData(Base):
    __tablename__ = 'scraped_data'
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Database URL (SQLite example, can be changed to PostgreSQL, etc.)
DATABASE_URL = "sqlite:///./app/data.db"  # Make sure the path is correct

# Create the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # SQLite specific argument
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to save scraped results in the database
def save_results(url: str, data: dict, db):
    print("Inside Saved Results=================================================")
    content = str(data)  # Convert the data to a string (could be a JSON serialization)
    scraped_result = ScrapedData(url=url, content=content)
    db.add(scraped_result)
    db.commit()
    db.refresh(scraped_result)  # Ensure the object is refreshed with its generated id
    return scraped_result

# Function to get all saved results from the database
def get_results(db):
    print("Inside Get Results=================================================")
    return db.query(ScrapedData).all()

# Function to delete a scraped result by its ID
def delete_result(id: int, db):
    print("Inside Delete Results=================================================")
    result = db.query(ScrapedData).filter(ScrapedData.id == id).first()
    if result:
        db.delete(result)
        db.commit()
        return {"message": "Record deleted successfully!"}
    else:
        return {"message": "Record not found!"}
