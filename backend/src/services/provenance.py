import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import psycopg  # type: ignore


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def record_provenance(
    source: str,
    payload: Any,
    cache_key: str,
    storage_dir: Path,
    postgres_dsn: Optional[str] = None,
) -> dict:
    """Persist provenance to file and optionally Postgres."""
    storage_dir.mkdir(parents=True, exist_ok=True)
    ts = _timestamp()
    filename = f"{source}-{cache_key}-{ts}.json"
    file_path = storage_dir / filename
    with file_path.open("w", encoding="utf-8") as f:
        json.dump({"source": source, "cache_key": cache_key, "timestamp": ts, "payload": payload}, f)

    db_record_id: Optional[int] = None
    if postgres_dsn:
        with psycopg.connect(postgres_dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS provenance (id serial PRIMARY KEY, source text, cache_key text, timestamp timestamptz, storage_ref text)"
                )
                cur.execute(
                    "INSERT INTO provenance (source, cache_key, timestamp, storage_ref) VALUES (%s, %s, %s, %s) RETURNING id",
                    (source, cache_key, ts, str(file_path)),
                )
                db_record_id = cur.fetchone()[0]
            conn.commit()

    return {"file_path": str(file_path), "db_record_id": db_record_id, "timestamp": ts}
