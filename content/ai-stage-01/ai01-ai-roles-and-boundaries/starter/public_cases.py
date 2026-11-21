def run_examples(choose):
    cases = [
        ("Цена", {"fixed_rules"}, "python"),
        ("Спам", {"learned_prediction"}, "ml"),
        ("Инструкция", {"existing_document", "new_text"}, "retrieval"),
        ("Черновик", {"new_text"}, "llm"),
        ("Риск", {"learned_prediction", "fixed_rules"}, "ml"),
        ("Отчёт", {"database", "fixed_rules"}, "sql"),
    ]
    for label, requirements, expected in cases:
        actual = choose(requirements)
        assert actual == expected, f"{label}: ожидалось {expected}, получено {actual}"
        print(f"{label}: {actual}")
