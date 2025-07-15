"""
Village-of-Intelligence Agent System
Self-evolving agent ecosystem with collective intelligence
"""

from .thinker_agent import create_thinker_agent
from .builder_agent import create_builder_agent
from .artist_agent import create_artist_agent
from .guardian_agent import create_guardian_agent
from .trainer_agent import create_trainer_agent

__all__ = [
    "create_thinker_agent",
    "create_builder_agent",
    "create_artist_agent",
    "create_guardian_agent",
    "create_trainer_agent"
]