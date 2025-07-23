"""
Database schema definitions for McDonald's scraper
"""

# SQL schema for outlets table
CREATE_OUTLETS_TABLE = """
CREATE TABLE IF NOT EXISTS outlets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    address TEXT NOT NULL,
    operating_hours TEXT,
    waze_link TEXT,
    latitude REAL,
    longitude REAL,
    features TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Indexes for better performance
CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_outlets_name ON outlets(name);",
    "CREATE INDEX IF NOT EXISTS idx_outlets_address ON outlets(address);",
    "CREATE INDEX IF NOT EXISTS idx_outlets_location ON outlets(latitude, longitude);",
    "CREATE INDEX IF NOT EXISTS idx_outlets_created_at ON outlets(created_at);"
]

# Unique constraint for existing tables (migration)
ADD_UNIQUE_CONSTRAINT = """
CREATE UNIQUE INDEX IF NOT EXISTS idx_outlets_name_unique ON outlets(name);
"""

# Add features column to existing tables (migration)
ADD_FEATURES_COLUMN = """
ALTER TABLE outlets ADD COLUMN features TEXT;
"""

# Trigger to update updated_at timestamp
CREATE_UPDATE_TRIGGER = """
CREATE TRIGGER IF NOT EXISTS update_outlets_updated_at
AFTER UPDATE ON outlets
FOR EACH ROW
BEGIN
    UPDATE outlets SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
"""

def get_schema_queries():
    """Get all schema creation queries"""
    queries = [CREATE_OUTLETS_TABLE]
    queries.extend(CREATE_INDEXES)
    queries.append(CREATE_UPDATE_TRIGGER)
    return queries

def get_migration_queries():
    """Get migration queries for existing databases"""
    return [ADD_UNIQUE_CONSTRAINT, ADD_FEATURES_COLUMN] 