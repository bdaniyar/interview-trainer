from main import unsafe_operations

def test_classifies():
    operations = [
        "ADD COLUMN nickname TEXT",
        "DROP COLUMN legacy",
        "ALTER COLUMN email SET NOT NULL",
        "create index ix_user_email",
    ]
    assert unsafe_operations(operations) == ["DROP COLUMN legacy", "ALTER COLUMN email SET NOT NULL"]
def test_empty(): assert unsafe_operations([]) == []
