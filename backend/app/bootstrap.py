from app import models  # noqa: F401
from app.database import Base, engine
from app.schema_bootstrap import ensure_created_at_columns


def bootstrap_database() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_created_at_columns(engine)
