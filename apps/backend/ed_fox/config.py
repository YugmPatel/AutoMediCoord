import os

class Settings:
    # Core
    asi_one_api_key = os.getenv("ASI_ONE_API_KEY", "")
    
    # Flags
    use_claude = os.getenv("USE_CLAUDE_PLANNER", "true").lower() == "true"
    use_vapi_out = os.getenv("USE_VAPI_OUTBOUND", "false").lower() == "true"
    use_composio_slack = os.getenv("USE_COMPOSIO_SLACK", "false").lower() == "true"
    
    # Keys
    claude_api_key = os.getenv("CLAUDE_API_KEY", "")
    vapi_api_key = os.getenv("VAPI_API_KEY", "")
    composio_api_key = os.getenv("COMPOSIO_API_KEY", "")

settings = Settings()