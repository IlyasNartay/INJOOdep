from sqlalchemy import text
from sqlalchemy.engine import Engine


def ensure_created_at_columns(engine: Engine) -> None:
    if engine.dialect.name != "postgresql":
        return

    statements = (
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS note TEXT NULL",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NULL",
        "ALTER TABLE users ALTER COLUMN created_at SET DEFAULT NOW()",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS status VARCHAR(20) NULL",
        "ALTER TABLE users ALTER COLUMN status SET DEFAULT 'active'",
        "UPDATE users SET status = 'active' WHERE status IS NULL",
        "ALTER TABLE users ALTER COLUMN status SET NOT NULL",
        "ALTER TABLE telegram_users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NULL",
        "ALTER TABLE telegram_users ALTER COLUMN created_at SET DEFAULT NOW()",
    )

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
