#!/usr/bin/env bash
set -euo pipefail

err() { echo "[ERROR] $*" >&2; }
info() { echo "[INFO] $*"; }

trap 'err "Script failed at line ${LINENO}"' ERR

if ! command -v df >/dev/null 2>&1; then
	err "df command not found"
	exit 1
fi

info "User: $(whoami)"
info "Date: $(date --iso-8601=seconds || date)"

info "Disk Usage:"
df -h || err "df failed"

if [ "$#" -gt 0 ]; then
	info "Additional command provided: $*"
	"$@"
fi

info "All checks completed successfully."
