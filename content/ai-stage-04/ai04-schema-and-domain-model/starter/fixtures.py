def demo(cls):
    result=cls.model_validate({"city":"Караганда","check_in":None,"check_out":None,"guests":2})
    assert result.model_dump()=={"city":"Караганда","check_in":None,"check_out":None,"guests":2}
    print(result.model_dump())
