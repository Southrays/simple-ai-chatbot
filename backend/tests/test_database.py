from sqlalchemy import inspect


def test_database_tables_are_created(test_engine):
    inspector = inspect(test_engine)

    table_names = inspector.get_table_names()

    assert "user_memories" in table_names