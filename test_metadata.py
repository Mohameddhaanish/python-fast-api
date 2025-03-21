from app.db.session import Base

print("Metadata object:", Base.metadata)
print("Tables:", Base.metadata.tables.keys())