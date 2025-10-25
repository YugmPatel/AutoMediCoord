"""
Base agent class for EDFlow AI
"""

from typing import Optional
from uagents import Agent, Context
from ...utils.config import get_config
from ...utils.logger import get_logger
from .protocol_handler import ChatProtocolHandler

logger = get_logger(__name__)


class BaseEDFlowAgent:
    """
    Base class for all EDFlow AI agents
    Provides common functionality including chat protocol support
    """
    
    def __init__(
        self,
        name: str,
        seed: str,
        port: Optional[int] = None,
        enable_mailbox: bool = False
    ):
        """
        Initialize base agent
        
        Args:
            name: Agent name
            seed: Recovery phrase for consistent address
            port: Port for local development (optional)
            enable_mailbox: Enable mailbox for Agentverse deployment
        """
        self.name = name
        self.config = get_config()
        
        # Create agent based on deployment mode
        if enable_mailbox or self.config.is_agentverse_mode():
            # Agentverse mode - use mailbox
            self.agent = Agent(
                name=name,
                seed=seed,
                mailbox=True
            )
            logger.info(f"Created {name} agent with mailbox for Agentverse")
        else:
            # Local mode - use port and endpoint
            endpoint = self.config.get_agent_endpoint(port) if port else None
            self.agent = Agent(
                name=name,
                seed=seed,
                port=port,
                endpoint=[endpoint] if endpoint else None
            )
            logger.info(f"Created {name} agent for local development on port {port}")
        
        # Initialize chat protocol handler
        self.chat_handler = ChatProtocolHandler(name)
        self.agent.include(self.chat_handler.get_protocol(), publish_manifest=True)
        
        # Setup default event handlers
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """Setup default event handlers"""
        
        @self.agent.on_event("startup")
        async def startup_handler(ctx: Context):
            """Handle agent startup"""
            logger.info(f"Agent {self.name} started")
            logger.info(f"Agent address: {ctx.agent.address}")
            await self.on_startup(ctx)
        
        @self.agent.on_event("shutdown")
        async def shutdown_handler(ctx: Context):
            """Handle agent shutdown"""
            logger.info(f"Agent {self.name} shutting down")
            await self.on_shutdown(ctx)
    
    async def on_startup(self, ctx: Context):
        """
        Override this method to add custom startup logic
        
        Args:
            ctx: Agent context
        """
        pass
    
    async def on_shutdown(self, ctx: Context):
        """
        Override this method to add custom shutdown logic
        
        Args:
            ctx: Agent context
        """
        pass
    
    def register_message_handler(self, handler_name: str, handler):
        """
        Register a custom message handler with the chat protocol
        
        Args:
            handler_name: Name of the handler
            handler: Async function to handle messages
        """
        self.chat_handler.register_message_handler(handler_name, handler)
    
    async def send_chat_message(self, ctx: Context, recipient: str, message: str):
        """
        Send a chat message to another agent
        
        Args:
            ctx: Agent context
            recipient: Recipient agent address
            message: Message text
        """
        await self.chat_handler.send_message(ctx, recipient, message)
    
    def get_agent(self) -> Agent:
        """Get the underlying uAgent instance"""
        return self.agent
    
    def get_address(self) -> str:
        """Get the agent's address"""
        return self.agent.address
    
    def run(self):
        """Run the agent"""
        logger.info(f"Starting {self.name} agent...")
        self.agent.run()