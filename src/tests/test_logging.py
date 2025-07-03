#!/usr/bin/env python3
"""
Test script to verify the logging system is working correctly.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from proximaai.utils.logger import setup_logging, get_logger

def test_logging():
    """Test the logging functionality."""
    # Setup logging
    logger = setup_logging(level="DEBUG")
    
    # Test different log levels
    logger.debug("This is a debug message", test_data="debug_value")
    logger.info("This is an info message", test_data="info_value")
    logger.warning("This is a warning message", test_data="warning_value")
    logger.error("This is an error message", test_data="error_value")
    
    # Test structured logging
    logger.info("Testing structured logging", 
               user_id="12345", 
               action="test", 
               status="success")
    
    # Test performance logging
    logger.log_performance("test_operation", 1.5, items_processed=100)
    
    # Test step logging
    logger.log_step("test_step", {"step_data": "test_value"})
    
    # Test agent logging
    logger.log_agent_creation("TestAgent", "agent_123", ["tool1", "tool2"])
    logger.log_agent_execution("TestAgent", "completed", 2.5)
    
    # Test tool usage logging
    logger.log_tool_usage("test_tool", "input_data", "result_data")
    
    # Test exception logging
    try:
        raise ValueError("Test exception")
    except Exception as e:
        logger.exception("Test exception caught", error=str(e))
    
    print("✅ Logging test completed! Check the logs directory for detailed logs.")

if __name__ == "__main__":
    test_logging() 