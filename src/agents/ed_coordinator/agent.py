"""
ED Coordinator Agent - Central orchestrator for Emergency Department operations
"""

from datetime import datetime
from typing import Dict, Any, Optional
from uagents import Context
from ..base.base_agent import BaseEDFlowAgent
from ...models.patient import PatientArrivalNotification, PatientUpdate
from ...models.messages import ProtocolActivation, StatusUpdate, Alert
from ...ai.claude_engine import ClaudeEngine
from ...utils.config import get_config
from ...utils.logger import get_logger

logger = get_logger(__name__)


class EDCoordinatorAgent(BaseEDFlowAgent):
    """
    ED Coordinator Agent - Central orchestration for all ED operations
    
    Responsibilities:
    - Receive patient arrival notifications
    - Coordinate with AI engine for protocol decisions
    - Route patients to appropriate emergency protocols
    - Coordinate with all other agents
    - Monitor overall ED status
    - Track metrics and KPIs
    """
    
    def __init__(self):
        """Initialize ED Coordinator Agent"""
        config = get_config()
        
        super().__init__(
            name="ed_coordinator",
            seed=config.ED_COORDINATOR_SEED,
            port=config.ED_COORDINATOR_PORT,
            enable_mailbox=config.is_agentverse_mode()
        )
        
        # Initialize Claude AI engine
        self.ai_engine = ClaudeEngine()
        
        # Track active patients
        self.active_patients: Dict[str, Dict[str, Any]] = {}
        
        # Agent addresses (will be populated)
        self.agent_addresses = {
            "resource_manager": None,
            "specialist_coordinator": None,
            "lab_service": None,
            "pharmacy": None,
            "bed_management": None,
        }
        
        # Setup message handlers
        self._setup_handlers()
        
        logger.info("ED Coordinator Agent initialized")
    
    def _setup_handlers(self):
        """Setup message handlers for the agent"""
        
        # Register custom message handler
        async def handle_custom_messages(ctx: Context, sender: str, text: str):
            """Handle custom messages"""
            logger.info(f"ED Coordinator received: {text} from {sender}")
            
            # Parse and route messages
            if "patient arrival" in text.lower():
                await self._handle_patient_notification(ctx, sender, text)
            elif "status update" in text.lower():
                await self._handle_status_update(ctx, sender, text)
            elif "alert" in text.lower():
                await self._handle_alert(ctx, sender, text)
        
        self.register_message_handler("custom_handler", handle_custom_messages)
        
        # Setup specific model handlers
        @self.agent.on_message(model=PatientArrivalNotification)
        async def handle_patient_arrival(ctx: Context, sender: str, msg: PatientArrivalNotification):
            """Handle patient arrival notifications"""
            await self._process_patient_arrival(ctx, sender, msg)
        
        @self.agent.on_message(model=StatusUpdate)
        async def handle_status_update(ctx: Context, sender: str, msg: StatusUpdate):
            """Handle status updates from other agents"""
            await self._process_status_update(ctx, sender, msg)
    
    async def on_startup(self, ctx: Context):
        """Custom startup logic"""
        logger.info("ED Coordinator Agent starting up...")
        logger.info(f"Agent address: {ctx.agent.address}")
        
        # Send startup notification
        await self.send_chat_message(
            ctx,
            ctx.agent.address,  # Self-message for testing
            "ED Coordinator Agent is online and ready"
        )
    
    async def _process_patient_arrival(
        self,
        ctx: Context,
        sender: str,
        msg: PatientArrivalNotification
    ):
        """
        Process patient arrival notification
        
        Args:
            ctx: Agent context
            sender: Sender address
            msg: Patient arrival notification
        """
        logger.info(f"Processing patient arrival: {msg.patient_id}")
        
        try:
            # Add to active patients
            self.active_patients[msg.patient_id] = {
                "arrival_time": msg.arrival_time,
                "vitals": msg.vitals,
                "chief_complaint": msg.chief_complaint,
                "priority": msg.priority,
                "status": "arriving"
            }
            
            # Analyze with AI engine
            analysis = await self.ai_engine.analyze_patient_acuity(
                vitals=msg.vitals,
                symptoms=msg.chief_complaint,
                history=msg.demographics.get("medical_history") if msg.demographics else None
            )
            
            logger.info(f"AI Analysis: Acuity {analysis.get('acuity_level')}, Protocol: {analysis.get('protocol')}")
            
            # Update patient info
            self.active_patients[msg.patient_id].update({
                "acuity_level": analysis.get("acuity_level"),
                "recommended_protocol": analysis.get("protocol"),
                "risk_factors": analysis.get("risk_factors", []),
                "confidence": analysis.get("confidence", 0.0)
            })
            
            # Determine if protocol activation is needed
            protocol = analysis.get("protocol", "general")
            if protocol in ["stemi", "stroke", "trauma", "pediatric"]:
                await self._activate_protocol(ctx, msg.patient_id, protocol)
            else:
                # Standard ED workflow
                await self._initiate_standard_workflow(ctx, msg.patient_id)
            
            # Notify all agents about new patient
            await self._broadcast_patient_status(ctx, msg.patient_id, "triaged")
            
        except Exception as e:
            logger.error(f"Error processing patient arrival: {str(e)}")
            await self._send_alert(
                ctx,
                "error",
                f"Failed to process patient {msg.patient_id}: {str(e)}"
            )
    
    async def _activate_protocol(
        self,
        ctx: Context,
        patient_id: str,
        protocol_type: str
    ):
        """
        Activate an emergency protocol
        
        Args:
            ctx: Agent context
            patient_id: Patient identifier
            protocol_type: Protocol to activate (stemi, stroke, trauma, pediatric)
        """
        logger.info(f"Activating {protocol_type.upper()} protocol for patient {patient_id}")
        
        activation_time = datetime.utcnow()
        
        # Calculate target completion based on protocol
        targets = {
            "stemi": 300,  # 5 minutes
            "stroke": 420,  # 7 minutes
            "trauma": 180,  # 3 minutes
            "pediatric": 240,  # 4 minutes
        }
        
        target_seconds = targets.get(protocol_type, 300)
        
        # Create protocol activation message
        activation = ProtocolActivation(
            activation_id=f"{protocol_type}_{patient_id}_{int(activation_time.timestamp())}",
            protocol_type=protocol_type,
            patient_id=patient_id,
            activation_time=activation_time,
            target_completion=datetime.fromtimestamp(
                activation_time.timestamp() + target_seconds
            ),
            checklist=[
                {"task": "team_activation", "status": "pending"},
                {"task": "resource_allocation", "status": "pending"},
                {"task": "lab_orders", "status": "pending"},
                {"task": "bed_assignment", "status": "pending"},
            ],
            activating_agent=ctx.agent.address
        )
        
        # Update patient status
        self.active_patients[patient_id]["protocol_activated"] = protocol_type
        self.active_patients[patient_id]["activation_time"] = activation_time
        
        # Broadcast protocol activation to all agents
        await self._broadcast_protocol_activation(ctx, activation)
        
        logger.info(f"Protocol {protocol_type.upper()} activated. Target: {target_seconds}s")
    
    async def _initiate_standard_workflow(
        self,
        ctx: Context,
        patient_id: str
    ):
        """
        Initiate standard ED workflow for non-critical patients
        
        Args:
            ctx: Agent context
            patient_id: Patient identifier
        """
        logger.info(f"Initiating standard workflow for patient {patient_id}")
        
        # Request resources
        if self.agent_addresses["resource_manager"]:
            await self.send_chat_message(
                ctx,
                self.agent_addresses["resource_manager"],
                f"Resource request for patient {patient_id}"
            )
        
        # Order routine labs
        if self.agent_addresses["lab_service"]:
            await self.send_chat_message(
                ctx,
                self.agent_addresses["lab_service"],
                f"Routine lab orders for patient {patient_id}"
            )
    
    async def _broadcast_protocol_activation(
        self,
        ctx: Context,
        activation: ProtocolActivation
    ):
        """
        Broadcast protocol activation to all agents
        
        Args:
            ctx: Agent context
            activation: Protocol activation details
        """
        message = f"PROTOCOL ACTIVATION: {activation.protocol_type.upper()} for patient {activation.patient_id}"
        
        # Send to all known agents
        for agent_name, address in self.agent_addresses.items():
            if address:
                try:
                    await self.send_chat_message(ctx, address, message)
                    logger.info(f"Protocol activation sent to {agent_name}")
                except Exception as e:
                    logger.error(f"Failed to notify {agent_name}: {str(e)}")
    
    async def _broadcast_patient_status(
        self,
        ctx: Context,
        patient_id: str,
        status: str
    ):
        """
        Broadcast patient status update to all agents
        
        Args:
            ctx: Agent context
            patient_id: Patient identifier
            status: New status
        """
        message = f"Patient {patient_id} status: {status}"
        
        for agent_name, address in self.agent_addresses.items():
            if address:
                try:
                    await self.send_chat_message(ctx, address, message)
                except Exception as e:
                    logger.error(f"Failed to notify {agent_name}: {str(e)}")
    
    async def _handle_patient_notification(
        self,
        ctx: Context,
        sender: str,
        text: str
    ):
        """Handle patient notification messages"""
        logger.info(f"Patient notification from {sender}: {text}")
    
    async def _handle_status_update(
        self,
        ctx: Context,
        sender: str,
        text: str
    ):
        """Handle status update messages"""
        logger.info(f"Status update from {sender}: {text}")
    
    async def _handle_alert(
        self,
        ctx: Context,
        sender: str,
        text: str
    ):
        """Handle alert messages"""
        logger.warning(f"Alert from {sender}: {text}")
    
    async def _process_status_update(
        self,
        ctx: Context,
        sender: str,
        msg: StatusUpdate
    ):
        """Process status updates from other agents"""
        logger.info(f"Status update for {msg.entity_type} {msg.entity_id}: {msg.status}")
        
        # Update internal state if it's a patient status
        if msg.entity_type == "patient" and msg.entity_id in self.active_patients:
            self.active_patients[msg.entity_id]["status"] = msg.status
            self.active_patients[msg.entity_id]["last_updated"] = msg.timestamp
    
    async def _send_alert(
        self,
        ctx: Context,
        alert_type: str,
        message: str
    ):
        """
        Send an alert to relevant parties
        
        Args:
            ctx: Agent context
            alert_type: Type of alert (critical, warning, info)
            message: Alert message
        """
        alert = Alert(
            alert_id=f"alert_{int(datetime.utcnow().timestamp())}",
            alert_type=alert_type,
            title=f"ED Coordinator Alert",
            message=message,
            timestamp=datetime.utcnow(),
            source_agent=ctx.agent.address,
            requires_action=(alert_type == "critical")
        )
        
        logger.warning(f"Alert ({alert_type}): {message}")
        
        # Broadcast to relevant agents
        for address in self.agent_addresses.values():
            if address:
                await self.send_chat_message(ctx, address, f"ALERT: {message}")
    
    def get_patient_count(self) -> int:
        """Get current number of active patients"""
        return len(self.active_patients)
    
    def get_patient_status(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific patient"""
        return self.active_patients.get(patient_id)
    
    def register_agent_address(self, agent_name: str, address: str):
        """
        Register another agent's address for communication
        
        Args:
            agent_name: Name of the agent
            address: Agent's address
        """
        if agent_name in self.agent_addresses:
            self.agent_addresses[agent_name] = address
            logger.info(f"Registered {agent_name} at {address}")
        else:
            logger.warning(f"Unknown agent name: {agent_name}")


# Main entry point for running the agent
if __name__ == "__main__":
    agent = EDCoordinatorAgent()
    agent.run()