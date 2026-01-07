"""
Base model classes and database configuration for Foreman Office data layer.

Architecture Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
Tenant Isolation: Mandatory organisation_id on all tables
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class TenantIsolatedModel(Base):
    """
    Base class for all tenant-isolated models.
    
    Privacy Guardrails (foreman/privacy-guardrails.md):
    - All tables MUST include organisation_id for tenant isolation
    - Cross-tenant queries MUST be prevented at schema level
    """
    __abstract__ = True
    
    # Tenant isolation field (MANDATORY)
    organisation_id = Column(String(255), nullable=False, index=True)
    
    # Audit timestamps (MANDATORY)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None))


class DatabaseConfig:
    """
    Database configuration and session management.
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize database configuration.
        
        Args:
            database_url: Database connection string (defaults to SQLite for testing)
        """
        self.database_url = database_url or "sqlite:///foreman_office.db"
        # Enable foreign keys for SQLite
        if self.database_url.startswith("sqlite"):
            self.engine = create_engine(
                self.database_url, 
                echo=False,
                connect_args={"check_same_thread": False},
                # Enable foreign key support
                poolclass=None
            )
            # Enable foreign keys on connection
            from sqlalchemy import event
            @event.listens_for(self.engine, "connect")
            def set_sqlite_pragma(dbapi_conn, connection_record):
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
        else:
            self.engine = create_engine(self.database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_all_tables(self):
        """Create all tables defined in the schema."""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_all_tables(self):
        """Drop all tables (for testing purposes)."""
        Base.metadata.drop_all(bind=self.engine)
    
    def get_session(self):
        """Get a new database session."""
        return self.SessionLocal()


# Global database config instance
_db_config: Optional[DatabaseConfig] = None


def init_database(database_url: Optional[str] = None) -> DatabaseConfig:
    """
    Initialize the database configuration.
    
    Args:
        database_url: Database connection string
        
    Returns:
        DatabaseConfig instance
    """
    global _db_config
    _db_config = DatabaseConfig(database_url)
    return _db_config


def get_database() -> DatabaseConfig:
    """
    Get the current database configuration.
    
    Returns:
        DatabaseConfig instance
        
    Raises:
        RuntimeError: If database not initialized
    """
    if _db_config is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    return _db_config
