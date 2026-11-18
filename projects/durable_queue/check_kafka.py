"""Host-side trusted CLI smoke; broker and messages stay in the test network."""

import json
from pathlib import Path
import subprocess
from uuid import uuid4


def main():
    compose = [
        "docker",
        "compose",
        "-f",
        str(Path(__file__).with_name("compose.brokers.yml")),
    ]

    def cli(name, *args, input=None):
        result = subprocess.run(
            compose
            + [
                "exec",
                "-T",
                "-e",
                "KAFKA_HEAP_OPTS=-Xms32m -Xmx128m",
                "kafka",
                f"/opt/kafka/bin/{name}.sh",
                *args,
            ],
            input=input,
            text=True,
            capture_output=True,
            timeout=45,
            check=True,
        )
        return result.stdout.splitlines()

    topic = "learning-" + uuid4().hex
    common = ["--bootstrap-server", "localhost:9092"]
    cli(
        "kafka-topics",
        *common,
        "--create",
        "--topic",
        topic,
        "--partitions",
        "1",
        "--replication-factor",
        "1",
    )
    try:
        cli(
            "kafka-console-producer", *common, "--topic", topic, input="first\nsecond\n"
        )
        for suffix in ["a", "b"]:
            actual = cli(
                "kafka-console-consumer",
                *common,
                "--topic",
                topic,
                "--group",
                topic + suffix,
                "--from-beginning",
                "--max-messages",
                "2",
                "--timeout-ms",
                "15000",
            )
            assert actual == ["first", "second"], actual
    finally:
        cli("kafka-topics", *common, "--delete", "--topic", topic)
    print(
        json.dumps(dict(kafka_retained_replay=True, groups=2, partitions=1, records=2))
    )


if __name__ == "__main__":
    main()
