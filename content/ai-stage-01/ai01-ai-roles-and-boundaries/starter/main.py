from public_cases import run_examples


def choose_approach(requirements: set[str]) -> str:
    raise NotImplementedError("Сопоставь флаги с первым шагом")


if __name__ == "__main__":
    run_examples(choose_approach)
