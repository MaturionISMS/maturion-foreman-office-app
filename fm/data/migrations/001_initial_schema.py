"""
Initial migration: Create Conversational Interface schema.

Architecture Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
QA Coverage: QA-001 to QA-018
Migration Date: 2026-01-02

This migration creates the foundational schema for the Conversational Interface subsystem:
- conversations table (CONV-01)
- messages table (CONV-02)
- conversation_contexts table (CONV-03)
- clarification_sessions table (CONV-04)

Tenant Isolation: All tables include organisation_id for strict tenant isolation.
"""

from typing import Optional
from fm.data.models import Base, init_database, get_database


def upgrade(database_url: Optional[str] = None) -> None:
    """
    Apply migration: Create all Conversational Interface tables.
    
    Args:
        database_url: Database connection string (optional)
    """
    # Initialize database
    if database_url:
        init_database(database_url)
    
    db = get_database()
    
    # Create all tables
    Base.metadata.create_all(bind=db.engine)
    
    print("✅ Migration applied: Conversational Interface schema created")
    print("   - conversations table (CONV-01)")
    print("   - messages table (CONV-02)")
    print("   - conversation_contexts table (CONV-03)")
    print("   - clarification_sessions table (CONV-04)")


def downgrade(database_url: Optional[str] = None) -> None:
    """
    Rollback migration: Drop all Conversational Interface tables.
    
    Args:
        database_url: Database connection string (optional)
    """
    # Initialize database
    if database_url:
        init_database(database_url)
    
    db = get_database()
    
    # Drop all tables
    Base.metadata.drop_all(bind=db.engine)
    
    print("✅ Migration rolled back: Conversational Interface schema dropped")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python 001_initial_schema.py [upgrade|downgrade] [database_url]")
        sys.exit(1)
    
    command = sys.argv[1]
    db_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    if command == "upgrade":
        upgrade(db_url)
    elif command == "downgrade":
        downgrade(db_url)
    else:
        print(f"Unknown command: {command}")
        print("Usage: python 001_initial_schema.py [upgrade|downgrade] [database_url]")
        sys.exit(1)
