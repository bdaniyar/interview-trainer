from main import UserProfile

def test_nested_and_defaults():
    first = UserProfile(id=1, address={"city": "Almaty", "country_code": "KZ"})
    second = UserProfile(id=2, address={"city": "Astana", "country_code": "KZ"})
    first.tags.append("python")
    assert first.address.city == "Almaty" and second.tags == []
