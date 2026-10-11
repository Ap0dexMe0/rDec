"""Pretty colored logging for rDec (coloredlogs + stdlib fallback)."""

import logging
import os
import sys

_CONFIGURED = False

# Padded level names keep every message starting at the same column.
_FMT = "%(levelname)-7s %(message)s"
_LEVEL_STYLES = {
    "debug": {"color": "cyan"},
    "info": {"color": "green"},
    "warning": {"color": "yellow"},
    "error": {"color": "red"},
    "critical": {"color": "red", "bold": True},
}

_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def setup(stream=None) -> logging.Logger:
    """Configure root logging once (colored); return the app logger.

    Everything (banner, logging) shares this one stream object so output
    can never interleave or overwrite itself when redirected to a file.
    Set RDEC_LOG_LEVEL=DEBUG to see per-operation internals.
    """
    global _CONFIGURED
    if not _CONFIGURED:
        level = os.getenv("RDEC_LOG_LEVEL", "INFO").upper()
        if level not in _LEVELS:
            level = "INFO"
        stream = stream or sys.stdout
        try:
            import coloredlogs
            coloredlogs.install(
                level=getattr(logging, level),
                fmt=_FMT,
                level_styles=_LEVEL_STYLES,
                stream=stream,
            )
        except ImportError:
            handler = logging.StreamHandler(stream)
            handler.setFormatter(logging.Formatter(_FMT))
            root = logging.getLogger()
            root.handlers = [handler]
            root.setLevel(getattr(logging, level))
        _CONFIGURED = True
    return logging.getLogger("rdec")


def get_logger(name: str = "rdec") -> logging.Logger:
    return logging.getLogger(name)
