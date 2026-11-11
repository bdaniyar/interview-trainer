"""Fixed trusted bootstrap command, invoked only as OS postgres by the grader.

Hidden bundle files and reference SQL are not included in the sandbox image.
This one seed is transported through an argv array before any student connection.
"""
import sys
import psycopg


def install(seed):
    if len(seed.encode("utf-8")) > 65536:
        raise ValueError("Fixture bootstrap budget")
    with psycopg.connect(host="/var/run/postgresql", user="postgres", dbname="lab") as connection:
        connection.execute("SET LOCAL search_path = lab, pg_catalog")
        connection.execute("TRUNCATE lab.order_items, lab.orders, lab.products, lab.users")
        if seed.strip():
            connection.execute(seed, prepare=False)


if __name__ == "__main__":
    install(sys.argv[1])
    sys.stdout.write("ready")
