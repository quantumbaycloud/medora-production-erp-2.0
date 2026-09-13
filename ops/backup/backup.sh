#!/usr/bin/env bash
set -euo pipefail
: "${PGHOST:?PGHOST required}" "${PGUSER:?PGUSER required}" "${PGDATABASE:?PGDATABASE required}" "${BACKUP_DIR:?BACKUP_DIR required}"
mkdir -p "$BACKUP_DIR"
pg_dump --format=custom --no-owner --file="$BACKUP_DIR/medorax_$(date -u +%Y%m%dT%H%M%SZ).dump" "$PGDATABASE"
find "$BACKUP_DIR" -type f -name '*.dump' -mtime +14 -delete
