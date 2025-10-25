"""
Utility functions - Consolidated
"""

import os
import logging
import sys
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Central configuration"""
    
    # API Keys
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    AGENTVERSE_API_KEY: str = os.getenv("AGENTVERSE_API_KEY", "")
    LETTA_API_KEY: str = os.getenv("LETTA_API_KEY", "")
    
    # Letta Configuration
    LETTA_ENABLED: bool = os.getenv("LETTA_ENABLED", "true").lower() == "true"
    
    # Agent Seeds
    ED_COORDINATOR_SEED: str = os.getenv("ED_COORDINATOR_SEED", "ed_coordinator_seed")
    RESOURCE_MANAGER_SEED: str = os.getenv("RESOURCE_MANAGER_SEED", "resource_manager_seed")
    SPECIALIST_COORDINATOR_SEED: str = os.getenv("SPECIALIST_COORDINATOR_SEED", "specialist_coordinator_seed")
    LAB_SERVICE_SEED: str = os.getenv("LAB_SERVICE_SEED", "lab_service_seed")
    PHARMACY_SEED: str = os.getenv("PHARMACY_SEED", "pharmacy_seed")
    BED_MANAGEMENT_SEED: str = os.getenv("BED_MANAGEMENT_SEED", "bed_management_seed")
    
    # Agent Ports
    ED_COORDINATOR_PORT: int = int(os.getenv("ED_COORDINATOR_PORT", "8000"))
    RESOURCE_MANAGER_PORT: int = int(os.getenv("RESOURCE_MANAGER_PORT", "8001"))
    SPECIALIST_COORDINATOR_PORT: int = int(os.getenv("SPECIALIST_COORDINATOR_PORT", "8002"))
    LAB_SERVICE_PORT: int = int(os.getenv("LAB_SERVICE_PORT", "8003"))
    PHARMACY_PORT: int = int(os.getenv("PHARMACY_PORT", "8004"))
    BED_MANAGEMENT_PORT: int = int(os.getenv("BED_MANAGEMENT_PORT", "8005"))
    
    # Deployment
    DEPLOYMENT_MODE: str = os.getenv("DEPLOYMENT_MODE", "local")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Performance
    AI_RESPONSE_TIMEOUT_SECONDS: int = int(os.getenv("AI_RESPONSE_TIMEOUT_SECONDS", "2"))
    AGENT_COMM_TIMEOUT_SECONDS: int = int(os.getenv("AGENT_COMM_TIMEOUT_SECONDS", "1"))
    MAX_CONCURRENT_PATIENTS: int = int(os.getenv("MAX_CONCURRENT_PATIENTS", "50"))
    
    @classmethod
    def is_local_mode(cls) -> bool:
        return cls.DEPLOYMENT_MODE.lower() == "local"
    
    @classmethod
    def is_agentverse_mode(cls) -> bool:
        return cls.DEPLOYMENT_MODE.lower() == "agentverse"


_config: Optional[Config] = None

def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config()
    return _config


# ============================================================================
# LOGGING
# ============================================================================

def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Setup logger with consistent formatting"""
    config = get_config()
    log_level = level or config.LOG_LEVEL
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    if logger.handlers:
        return logger
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, log_level.upper()))
    
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get or create logger"""
    return setup_logger(name)