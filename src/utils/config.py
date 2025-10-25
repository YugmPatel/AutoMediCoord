"""
Configuration management for EDFlow AI
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Central configuration for EDFlow AI system"""
    
    # API Keys
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    AGENTVERSE_API_KEY: str = os.getenv("AGENTVERSE_API_KEY", "")
    
    # Agent Seeds
    ED_COORDINATOR_SEED: str = os.getenv("ED_COORDINATOR_SEED", "ed_coordinator_seed")
    RESOURCE_MANAGER_SEED: str = os.getenv("RESOURCE_MANAGER_SEED", "resource_manager_seed")
    SPECIALIST_COORDINATOR_SEED: str = os.getenv("SPECIALIST_COORDINATOR_SEED", "specialist_coordinator_seed")
    LAB_SERVICE_SEED: str = os.getenv("LAB_SERVICE_SEED", "lab_service_seed")
    PHARMACY_SEED: str = os.getenv("PHARMACY_SEED", "pharmacy_seed")
    BED_MANAGEMENT_SEED: str = os.getenv("BED_MANAGEMENT_SEED", "bed_management_seed")
    
    # Agent Ports (for local development)
    ED_COORDINATOR_PORT: int = int(os.getenv("ED_COORDINATOR_PORT", "8000"))
    RESOURCE_MANAGER_PORT: int = int(os.getenv("RESOURCE_MANAGER_PORT", "8001"))
    SPECIALIST_COORDINATOR_PORT: int = int(os.getenv("SPECIALIST_COORDINATOR_PORT", "8002"))
    LAB_SERVICE_PORT: int = int(os.getenv("LAB_SERVICE_PORT", "8003"))
    PHARMACY_PORT: int = int(os.getenv("PHARMACY_PORT", "8004"))
    BED_MANAGEMENT_PORT: int = int(os.getenv("BED_MANAGEMENT_PORT", "8005"))
    
    # Deployment Mode
    DEPLOYMENT_MODE: str = os.getenv("DEPLOYMENT_MODE", "local")  # "local" or "agentverse"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Performance Targets
    AI_RESPONSE_TIMEOUT_SECONDS: int = int(os.getenv("AI_RESPONSE_TIMEOUT_SECONDS", "2"))
    AGENT_COMM_TIMEOUT_SECONDS: int = int(os.getenv("AGENT_COMM_TIMEOUT_SECONDS", "1"))
    
    # System Configuration
    MAX_CONCURRENT_PATIENTS: int = int(os.getenv("MAX_CONCURRENT_PATIENTS", "50"))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        required_keys = [
            "ANTHROPIC_API_KEY",
        ]
        
        for key in required_keys:
            value = getattr(cls, key, None)
            if not value or value == "":
                print(f"Warning: {key} is not set in environment")
                return False
        
        return True
    
    @classmethod
    def is_local_mode(cls) -> bool:
        """Check if running in local mode"""
        return cls.DEPLOYMENT_MODE.lower() == "local"
    
    @classmethod
    def is_agentverse_mode(cls) -> bool:
        """Check if deploying to Agentverse"""
        return cls.DEPLOYMENT_MODE.lower() == "agentverse"
    
    @classmethod
    def get_agent_endpoint(cls, port: int) -> str:
        """Get agent endpoint URL"""
        if cls.is_local_mode():
            return f"http://localhost:{port}/submit"
        return ""  # Agentverse handles endpoints automatically


# Singleton instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get configuration singleton"""
    global _config
    if _config is None:
        _config = Config()
    return _config