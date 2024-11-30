from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Define the Base model
Base = declarative_base()

class ScrapedData(Base):
    __tablename__ = 'scraped_data'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

DATABASE_URL = "sqlite:///./app/data.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_results(url: str, data: dict, db):
    try:
        content = str(data)
        scraped_result = ScrapedData(url=url, content=content)
        db.add(scraped_result)
        db.commit()
        db.refresh(scraped_result)
        return scraped_result
    except Exception as e:
        print(f"Error saving results: {e}")
        raise

def get_results(db):
    return db.query(ScrapedData).all()

def delete_result(id: int, db):
    try:
        result = db.query(ScrapedData).filter(ScrapedData.id == id).first()
        if result:
            db.delete(result)
            db.commit()
            return {"message": "Record deleted successfully!"}
        else:
            raise ValueError("Record not found!")
    except Exception as e:
        print(f"Error deleting record: {e}")
        raise
