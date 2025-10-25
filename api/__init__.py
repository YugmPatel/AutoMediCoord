"""
EDFlow AI API Package
FastAPI wrapper for uAgents backend
"""

__version__ = "1.0.0"
__author__ = "EDFlow AI Team"
__description__ = "Emergency Department Flow Optimization API"

from .main import app, socket_app

__all__ = ["app", "socket_app"]