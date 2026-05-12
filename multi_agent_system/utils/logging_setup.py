"""
utils/logging_setup.py
----------------------
One-stop logging configuration for the multi-agent system.

Call :func:`setup_logging` once at the start of any entry point
(``main.py``, ``frontend/app.py``) and every module that uses
``logging.getLogger(__name__)`` will produce consistent, well-formatted
output. Subsequent calls are no-ops, so calling it from multiple entry
points is safe.

Format
------
    [HH:MM:SS] INFO    agents.movie_agent: MovieAgent ▶ tell me about Inception
"""

from __future__ import annotations

import logging
import os


_CONFIGURED: bool = False

_FORMAT: str = "[%(asctime)s] %(levelname)-7s %(name)s: %(message)s"
_DATE_FORMAT: str = "%H:%M:%S"


def setup_logging(level: str | None = None) -> None:
    """
    Configure the root logger once.

    Parameters
    ----------
    level : str, optional
        Log level name (``"DEBUG"``, ``"INFO"``, ``"WARNING"``, …).
        Falls back to the ``LOG_LEVEL`` environment variable, then to
        ``"INFO"``.
    """
    global _CONFIGURED
    if _CONFIGURED:
        return

    level_name = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    level_value = getattr(logging, level_name, logging.INFO)

    logging.basicConfig(level=level_value, format=_FORMAT, datefmt=_DATE_FORMAT)
    _CONFIGURED = True


__all__ = ["setup_logging"]
