import time

from sqlalchemy.exc import OperationalError

from app.bootstrap import bootstrap_database


def main() -> None:
    attempts = 20
    delay_seconds = 3

    for attempt in range(1, attempts + 1):
        try:
            bootstrap_database()
            print("Database bootstrap completed.")
            return
        except OperationalError as error:
            if attempt == attempts:
                raise
            print(
                f"Database is not ready yet "
                f"(attempt {attempt}/{attempts}): {error}"
            )
            time.sleep(delay_seconds)


if __name__ == "__main__":
    main()
