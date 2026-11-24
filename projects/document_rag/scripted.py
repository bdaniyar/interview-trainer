"""Synthetic feature embeddings and extractive generator with no network I/O."""
import re
from math import hypot

from projects.vector_search.contracts import DIMENSIONS

from .pipeline import Claim, Draft


TOPICS = {
    "bridge": {"bridge", "мост", "моста", "көпір", "көпірдің"},
    "archive": {"archive", "архив", "архива", "мұрағат", "мұрағаттың"},
    "locker": {"locker", "шкафчик", "шкафчика", "жәшік", "жәшіктің"},
    "vault": {"vault", "хранилище", "хранилища", "қойма", "қойманың"},
    "weather": {"weather", "погода", "погоды", "ауа", "жауын"},
    "calendar": {"calendar", "календарь", "календаря", "күнтізбе", "күнтізбенің"},
    "boat": {"boat", "лодка", "лодки", "қайық", "қайықтың"},
    "ferry": {"ferry", "паром", "парома", "өткел", "өткелдің"},
    "library": {"library", "библиотека", "библиотеки", "кітапхана", "кітапхананың"},
    "tunnel": {"tunnel", "тоннель", "тоннеля", "туннель", "үңгір"},
}
FEATURES = tuple(TOPICS)
FACT = re.compile(r"^Fact: ([a-z]+) = ([A-Za-z0-9:_-]{1,32})$", re.MULTILINE)


def tokens(text):
    return tuple(re.findall(r"[^\W_]+", text.casefold()))


def topic(text):
    words = set(tokens(text))
    return next((key for key, aliases in TOPICS.items() if words & aliases), None)


def lexical_query(question):
    words = tokens(question)
    aliases = TOPICS.get(topic(question), ())
    return next((word for word in words if word in aliases), words[0] if words else "")


def embed(text):
    words = set(tokens(text))
    vector = [float(bool(words & TOPICS[key])) for key in FEATURES] + [0.0] * (DIMENSIONS - len(FEATURES))
    vector[-1] = 0.15 if any(vector) else 1.0
    magnitude = hypot(*vector)
    return tuple(value / magnitude for value in vector)


def batch(texts):
    return tuple(embed(text) for text in texts)


def rerank_script(question, keys, evidence):
    words = set(tokens(question))
    target = topic(question)
    return [
        (key, len(words.intersection(tokens(evidence[key].text)))
         + 3 * int(any(fact_topic == target for fact_topic, _ in FACT.findall(evidence[key].text))))
        for key in keys
    ]


def facts_for(evidence):
    return {f"{key}={value}" for key, value in FACT.findall(evidence.text)}


def generate(context):
    expected = topic(context.question)
    seen = {}
    for evidence in context.evidence:
        for key, value in FACT.findall(evidence.text):
            if key == expected:
                seen.setdefault(value, []).append(evidence.source)
    if not seen:
        return Draft("abstain")
    if len(seen) > 1:
        return Draft("conflict")
    value, sources = next(iter(seen.items()))
    return Draft("answer", (Claim(f"{expected}={value}", tuple(dict.fromkeys(sources))),))
