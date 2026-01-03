"""
Structured logging infrastructure for AI Video Production System.

Provides consistent logging across all components with support for
multiple formats (console, JSON), log levels, and contextual information.
"""

import logging
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add custom fields if present
        if hasattr(record, "agent_name"):
            log_data["agent_name"] = record.agent_name
        if hasattr(record, "session_id"):
            log_data["session_id"] = record.session_id
        if hasattr(record, "duration"):
            log_data["duration_ms"] = record.duration

        return json.dumps(log_data)


class ColoredConsoleFormatter(logging.Formatter):
    """Colored console formatter for better readability."""

    # Color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"

        # Add agent name if present
        if hasattr(record, "agent_name"):
            record.msg = f"[{record.agent_name}] {record.msg}"

        return super().format(record)


class AgentLogger:
    """Logger with agent-specific context."""

    def __init__(
        self, logger: logging.Logger, agent_name: str, session_id: Optional[str] = None
    ):
        self.logger = logger
        self.agent_name = agent_name
        self.session_id = session_id

    def _log(self, level: int, msg: str, **kwargs):
        """Log with agent context."""
        extra = {"agent_name": self.agent_name, "session_id": self.session_id}
        extra.update(kwargs)
        self.logger.log(level, msg, extra=extra)

    def debug(self, msg: str, **kwargs):
        """Log debug message."""
        self._log(logging.DEBUG, msg, **kwargs)

    def info(self, msg: str, **kwargs):
        """Log info message."""
        self._log(logging.INFO, msg, **kwargs)

    def warning(self, msg: str, **kwargs):
        """Log warning message."""
        self._log(logging.WARNING, msg, **kwargs)

    def error(self, msg: str, **kwargs):
        """Log error message."""
        self._log(logging.ERROR, msg, **kwargs)

    def critical(self, msg: str, **kwargs):
        """Log critical message."""
        self._log(logging.CRITICAL, msg, **kwargs)


def setup_logging(
    name: str,
    log_dir: Optional[Path] = None,
    level: str = "INFO",
    json_logs: bool = False,
    console_output: bool = True,
) -> logging.Logger:
    """
    Setup logging with file and console handlers.

    Args:
        name: Logger name
        log_dir: Directory for log files
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_logs: Use JSON format for file logs
        console_output: Enable console output

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    logger.handlers.clear()  # Clear existing handlers

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        console_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        console_formatter = ColoredConsoleFormatter(console_format)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"{name}.log"

        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
        )
        file_handler.setLevel(logging.DEBUG)

        if json_logs:
            file_formatter = JSONFormatter()
        else:
            file_format = "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s"
            file_formatter = logging.Formatter(file_format)

        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str, agent_name: Optional[str] = None) -> logging.Logger:
    """
    Get or create a logger.

    Args:
        name: Logger name (typically module name)
        agent_name: Optional agent name for context

    Returns:
        Logger instance or AgentLogger if agent_name provided
    """
    logger = logging.getLogger(name)

    if agent_name:
        return AgentLogger(logger, agent_name)

    return logger


# Create default application logger
def create_app_logger(
    log_dir: Optional[Path] = None, level: str = "INFO"
) -> logging.Logger:
    """Create the main application logger."""
    return setup_logging(
        "ai_video", log_dir=log_dir, level=level, json_logs=False, console_output=True
    )
