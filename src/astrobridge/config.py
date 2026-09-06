from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    rabbitmq_host: str = os.getenv("RABBITMQ_HOST", "127.0.0.1")
    rabbitmq_port: int = int(os.getenv("RABBITMQ_PORT", "5672"))
    rabbitmq_user: str = os.getenv("RABBITMQ_USER", "astrobridge_demo")
    rabbitmq_password: str = os.getenv("RABBITMQ_PASSWORD", "demo_only_change_me")
    data_dir: Path = Path(os.getenv("ASTROBRIDGE_DATA_DIR", ".astrobridge"))
    webhook_secret: str = os.getenv("WEBHOOK_SECRET", "synthetic_demo_secret_change_me")
