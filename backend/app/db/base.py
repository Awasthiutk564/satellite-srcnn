from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


# Import all models so that Alembic can detect them for migrations.
# These imports are intentionally placed at the bottom to avoid circular imports.
try:  # pragma: no cover - import side effects only
    from app.db.models.user import User  # noqa: F401
    from app.db.models.image import Image  # noqa: F401
    from app.db.models.result import Result  # noqa: F401
except Exception:
    # During certain tooling operations, app packages may not be importable.
    # This fail-safe keeps Base importable without breaking migrations.
    pass

