"""Plotting backend selection and feature flags."""

from __future__ import annotations

import os
from typing import Optional

_DEFAULT_BACKEND = os.getenv("QS_PLOT_BACKEND", os.getenv("QUANTSTATS_PLOT_BACKEND", "hvplot"))
_BACKEND = _DEFAULT_BACKEND.strip().lower()


def get_backend() -> str:
    """Return the configured backend name (may be unresolved)."""
    return _BACKEND


def set_backend(name: str) -> None:
    """Set the default plotting backend for this process."""
    global _BACKEND
    _BACKEND = (name or "").strip().lower()


def resolve_backend(backend: Optional[str] = None) -> str:
    """Resolve backend with support for 'auto' and aliases."""
    name = (backend or _BACKEND or "").strip().lower()
    if name in {"", "default"}:
        name = _BACKEND
    if name in {"auto", "prefer"}:
        if _has_hvplot():
            return "hvplot"
        return "matplotlib"
    if name in {"mpl", "matplotlib", "plt"}:
        return "matplotlib"
    if name in {"hv", "hvplot", "holoviews"}:
        return "hvplot"
    return name


def is_hvplot(backend: Optional[str] = None) -> bool:
    return resolve_backend(backend) == "hvplot"


def is_matplotlib(backend: Optional[str] = None) -> bool:
    return resolve_backend(backend) == "matplotlib"


def _has_hvplot() -> bool:
    try:
        import hvplot  # noqa: F401

        return True
    except Exception:
        return False
