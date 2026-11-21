from contracts import Generation, ProviderUnavailable


class Scripted:
    def __init__(self, outcome):
        self.outcome = outcome

    async def generate(self, question):
        if self.outcome == "unavailable":
            raise ProviderUnavailable()
        if self.outcome == "incomplete":
            return Generation("incomplete", "часть", 0)
        return Generation("completed", f"Материал найден: {question}", None)


async def exercise(dispatch):
    for outcome in ("completed", "unavailable", "incomplete"):
        result = await dispatch(Scripted(outcome), "расписание")
        assert result.status == outcome
        assert (result.text is not None) == (outcome == "completed")
        print(result)
