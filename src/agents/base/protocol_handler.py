"""
Chat protocol handler for EDFlow AI agents
"""

from datetime import datetime
from uuid import uuid4
from typing import Callable, Awaitable
from uagents import Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    chat_protocol_spec,
)
from ...utils.logger import get_logger

logger = get_logger(__name__)


class ChatProtocolHandler:
    """
    Handles chat protocol communication for agents
    Implements standardized message handling and acknowledgments
    """
    
    def __init__(self, agent_name: str):
        """
        Initialize chat protocol handler
        
        Args:
            agent_name: Name of the agent using this handler
        """
        self.agent_name = agent_name
        self.protocol = Protocol(spec=chat_protocol_spec)
        self.message_handlers = {}
        
        # Setup default handlers
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup default chat protocol handlers"""
        
        @self.protocol.on_message(ChatMessage)
        async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
            """Handle incoming chat messages"""
            logger.info(f"{self.agent_name} received chat message from {sender}")
            
            # Send acknowledgment
            await ctx.send(
                sender,
                ChatAcknowledgement(
                    timestamp=datetime.utcnow(),
                    acknowledged_msg_id=msg.msg_id
                )
            )
            
            # Process message content
            for item in msg.content:
                if isinstance(item, TextContent):
                    logger.debug(f"Message content: {item.text}")
                    
                    # Call custom handlers if registered
                    for handler in self.message_handlers.values():
                        await handler(ctx, sender, item.text)
        
        @self.protocol.on_message(ChatAcknowledgement)
        async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
            """Handle message acknowledgments"""
            logger.debug(f"{self.agent_name} received ack for message {msg.acknowledged_msg_id} from {sender}")
    
    def register_message_handler(
        self,
        handler_name: str,
        handler: Callable[[Context, str, str], Awaitable[None]]
    ):
        """
        Register a custom message handler
        
        Args:
            handler_name: Name of the handler
            handler: Async function to handle messages (ctx, sender, text)
        """
        self.message_handlers[handler_name] = handler
        logger.info(f"Registered message handler: {handler_name}")
    
    async def send_message(
        self,
        ctx: Context,
        recipient: str,
        message_text: str
    ):
        """
        Send a chat message to another agent
        
        Args:
            ctx: Agent context
            recipient: Recipient agent address
            message_text: Text content to send
        """
        msg = ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[
                TextContent(type="text", text=message_text)
            ]
        )
        
        await ctx.send(recipient, msg)
        logger.info(f"{self.agent_name} sent message to {recipient}")
    
    def get_protocol(self) -> Protocol:
        """Get the chat protocol instance"""
        return self.protocol