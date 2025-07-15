"""
OBELISK Agent System Integration
7 specialized agents for comprehensive software development
"""

from .code_architect_agent import create_code_architect_agent
from .code_generator_agent import create_code_generator_agent
from .quality_checker_agent import create_quality_checker_agent
from .test_harness_agent import create_test_harness_agent
from .ideas_agent import create_ideas_agent
from .creativity_agent import create_creativity_agent
from .self_scoring_agent import create_self_scoring_agent

__all__ = [
    "create_code_architect_agent",
    "create_code_generator_agent", 
    "create_quality_checker_agent",
    "create_test_harness_agent",
    "create_ideas_agent",
    "create_creativity_agent",
    "create_self_scoring_agent"
]