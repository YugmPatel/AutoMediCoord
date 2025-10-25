"""
AutoMediCoord - Autonomous Medical Coordinator
Emergency Department Flow Optimizer
"""

__version__ = "1.0.0"
__author__ = "AutoMediCoord Team"

# Make modules available at package level
from . import models
from . import utils
from . import ai
from . import agents

__all__ = ["models", "utils", "ai", "agents"]