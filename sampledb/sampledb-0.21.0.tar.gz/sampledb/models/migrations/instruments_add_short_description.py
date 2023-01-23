# coding: utf-8
"""
Add short_description and short_description_is_markdown columns to instruments table.
"""

import os

import flask_sqlalchemy

MIGRATION_INDEX = 40
MIGRATION_NAME, _ = os.path.splitext(os.path.basename(__file__))


def run(db: flask_sqlalchemy.SQLAlchemy) -> bool:
    # Skip migration by condition
    column_names = db.session.execute(db.text("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'instruments'
    """)).fetchall()
    if ('short_description',) in column_names:
        return False
    if ('name', ) not in column_names:
        return False

    # Perform migration
    db.session.execute(db.text("""
        ALTER TABLE instruments
        ADD short_description TEXT NOT NULL DEFAULT ''
    """))
    db.session.execute(db.text("""
        ALTER TABLE instruments
        ADD short_description_is_markdown BOOLEAN NOT NULL DEFAULT FALSE
    """))
    db.session.execute(db.text("""
        UPDATE instruments
        SET short_description = description, short_description_is_markdown=description_is_markdown
    """))
    return True
