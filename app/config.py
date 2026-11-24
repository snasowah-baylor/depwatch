import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./depwatch.db")
    max_upload_bytes: int = int(os.getenv("MAX_UPLOAD_BYTES", "1048576"))
    osv_timeout_seconds: float = float(os.getenv("OSV_TIMEOUT_SECONDS", "10"))


settings = Settings()
