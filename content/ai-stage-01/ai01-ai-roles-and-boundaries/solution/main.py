from public_cases import run_examples


def choose_approach(requirements: set[str]) -> str:
    known = {"fixed_rules", "database", "learned_prediction", "existing_document", "new_text"}
    if not requirements or requirements - known:
        raise ValueError("Требуются известные флаги")
    sources = requirements & {"database", "existing_document"}
    if len(sources) == 2:
        raise ValueError("Сначала выбери основной источник данных")
    if sources:
        return "sql" if "database" in sources else "retrieval"
    if {"learned_prediction", "new_text"} <= requirements:
        raise ValueError("Раздели прогноз и генерацию")
    if "learned_prediction" in requirements:
        return "ml"
    if "new_text" in requirements:
        return "llm"
    return "python"


if __name__ == "__main__":
    run_examples(choose_approach)
