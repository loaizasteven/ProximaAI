"""
Logging configuration for ProximaAI system.
Provides centralized logging with different levels and formatters.
"""

import logging
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json


class ProximaAILogger:
    """Centralized logger for ProximaAI system."""
    
    def __init__(self, name: str = "proximaai", level: str = "INFO"):
        self.name = name
        self.level = getattr(logging, level.upper())
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup the logger with handlers and formatters."""
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        
        # Clear any existing handlers to avoid duplicates
        logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # Console handler with simple format
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.level)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)
        
        # File handler with detailed format
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"proximaai_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def debug(self, message: str, **kwargs):
        """Log debug message with optional structured data."""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs, default=str)}"
        self.logger.debug(message)
    
    def info(self, message: str, **kwargs):
        """Log info message with optional structured data."""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs, default=str)}"
        self.logger.info(message)
    
    def warning(self, message: str, **kwargs):
        """Log warning message with optional structured data."""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs, default=str)}"
        self.logger.warning(message)
    
    def error(self, message: str, **kwargs):
        """Log error message with optional structured data."""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs, default=str)}"
        self.logger.error(message)
    
    def critical(self, message: str, **kwargs):
        """Log critical message with optional structured data."""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs, default=str)}"
        self.logger.critical(message)
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback."""
        if kwargs:
            message = f"{message} | {json.dumps(kwargs, default=str)}"
        self.logger.exception(message)
    
    def log_step(self, step_name: str, step_data: Optional[Dict[str, Any]] = None):
        """Log a workflow step with structured data."""
        message = f"🔄 STEP: {step_name}"
        if step_data:
            self.info(message, step_data=step_data)
        else:
            self.info(message)
    
    def log_agent_creation(self, agent_name: str, agent_id: str, tools: list):
        """Log agent creation with details."""
        self.info(f"🤖 AGENT CREATED: {agent_name}", 
                 agent_id=agent_id, 
                 tools=tools)
    
    def log_agent_execution(self, agent_name: str, status: str, duration: Optional[float] = None):
        """Log agent execution status."""
        data = {"agent_name": agent_name, "status": status}
        if duration:
            data["duration_seconds"] = str(duration)
        
        if status == "completed":
            self.info(f"✅ AGENT COMPLETED: {agent_name}", **data)
        elif status == "failed":
            self.error(f"❌ AGENT FAILED: {agent_name}", **data)
        else:
            self.info(f"🔄 AGENT STATUS: {agent_name} - {status}", **data)
    
    def log_tool_usage(self, tool_name: str, input_data: str, result: str):
        """Log tool usage with input and result."""
        # Truncate long inputs/results for readability
        input_preview = input_data[:100] + "..." if len(input_data) > 100 else input_data
        result_preview = result[:200] + "..." if len(result) > 200 else result
        
        self.debug(f"🛠️ TOOL USED: {tool_name}", 
                  input_preview=input_preview,
                  result_preview=result_preview)
    
    def log_performance(self, operation: str, duration: float, **kwargs):
        """Log performance metrics."""
        self.info(f"⏱️ PERFORMANCE: {operation}", 
                 duration_seconds=duration, **kwargs)


# Global logger instance
_logger_instance: Optional[ProximaAILogger] = None


def get_logger(name: str = "proximaai", level: str = "INFO") -> ProximaAILogger:
    """Get or create a logger instance."""
    global _logger_instance
    
    if _logger_instance is None:
        _logger_instance = ProximaAILogger(name, level)
    
    return _logger_instance


def setup_logging(level: str = "INFO", log_to_file: bool = True):
    """Setup logging configuration for the entire application."""
    # Set the global logging level
    logging.getLogger().setLevel(getattr(logging, level.upper()))
    
    # Create the main logger
    logger = get_logger("proximaai", level)
    
    # Log the setup
    logger.info("🚀 ProximaAI logging system initialized", 
               level=level, 
               log_to_file=log_to_file)
    
    return logger


# Convenience functions for quick logging
def debug(message: str, **kwargs):
    """Quick debug logging."""
    get_logger().debug(message, **kwargs)


def info(message: str, **kwargs):
    """Quick info logging."""
    get_logger().info(message, **kwargs)


def warning(message: str, **kwargs):
    """Quick warning logging."""
    get_logger().warning(message, **kwargs)


def error(message: str, **kwargs):
    """Quick error logging."""
    get_logger().error(message, **kwargs)


def critical(message: str, **kwargs):
    """Quick critical logging."""
    get_logger().critical(message, **kwargs)


def exception(message: str, **kwargs):
    """Quick exception logging."""
    get_logger().exception(message, **kwargs) 