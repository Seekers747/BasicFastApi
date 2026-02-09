from sqlalchemy import Column, Integer, String # type: ignore[reportMissingImports]
from sqlalchemy.ext.declarative import declarative_base # type: ignore[reportMissingImports]

Base = declarative_base()

class User(Base):
    """Database model for users table."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)  # In production, this would be hashed
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"