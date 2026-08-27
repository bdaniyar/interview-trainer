from main import active_emails

def test_filters_and_normalizes():
    users = [
        {"active": True, "email": " A@EXAMPLE.COM "},
        {"active": False, "email": "b@example.com"},
        {"active": True},
    ]
    assert active_emails(users) == ["a@example.com"]
