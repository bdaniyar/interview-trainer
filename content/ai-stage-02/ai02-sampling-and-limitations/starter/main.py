from random import Random


def candidates(logits, temperature, top_p):
    raise NotImplementedError("Преобразуй веса и выбери префикс")


def sample(logits, temperature, top_p, rng):
    raise NotImplementedError("Используй один случайный выбор")


if __name__ == "__main__":
    assert candidates([1, 1], 1, 0.5) == [(0, 1)]
    print(sample([1, 1], 1, 1, Random(4)))
