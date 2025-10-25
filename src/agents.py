"""
All EDFlow AI Agents - Consolidated Implementation
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from uagents import Agent, Context, Protocol, Model
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    chat_protocol_spec,
)
from uuid import uuid4

from .models import (
    PatientArrivalNotification,
    ResourceRequest,
    ResourceAllocation,
    ResourceConflict,
    TeamActivationRequest,
    TeamStatus,
    LabOrder,
    LabResult,
    MedicationOrder,
    MedicationDelivery,
    BedRequest,
    BedAssignment,
    ProtocolActivation,
    StatusUpdate,
    Alert,
)
from .ai import ClaudeEngine
from .utils import get_config, get_logger

logger = get_logger(__name__)
config = get_config()


# ============================================================================
# BASE AGENT CLASS
# ============================================================================

class BaseEDFlowAgent:
    """Base class for all EDFlow AI agents"""
    
    def __init__(self, name: str, seed: str, port: Optional[int] = None):
        self.name = name
        
        # Create agent
        if config.is_agentverse_mode():
            self.agent = Agent(name=name, seed=seed, mailbox=True)
        else:
            endpoint = f"http://localhost:{port}/submit" if port else None
            self.agent = Agent(
                name=name,
                seed=seed,
                port=port,
                endpoint=[endpoint] if endpoint else None
            )
        
        # Setup chat protocol
        self.chat_proto = Protocol(spec=chat_protocol_spec)
        self._setup_chat_handlers()
        self.agent.include(self.chat_proto, publish_manifest=True)
        
        logger.info(f"{name} agent initialized")
    
    def _setup_chat_handlers(self):
        @self.chat_proto.on_message(ChatMessage)
        async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
            await ctx.send(sender, ChatAcknowledgement(
                timestamp=datetime.utcnow(),
                acknowledged_msg_id=msg.msg_id
            ))
            for item in msg.content:
                if isinstance(item, TextContent):
                    await self.on_message(ctx, sender, item.text)
        
        @self.chat_proto.on_message(ChatAcknowledgement)
        async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
            logger.debug(f"Ack received: {msg.acknowledged_msg_id}")
    
    async def on_message(self, ctx: Context, sender: str, text: str):
        """Override this to handle messages"""
        logger.info(f"{self.name} received: {text}")
    
    async def send_message(self, ctx: Context, recipient: str, text: str):
        """Send a chat message"""
        await ctx.send(recipient, ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=text)]
        ))
    
    def run(self):
        self.agent.run()


# ============================================================================
# 1. ED COORDINATOR AGENT
# ============================================================================

class EDCoordinatorAgent(BaseEDFlowAgent):
    """Central orchestrator for ED operations"""
    
    def __init__(self):
        super().__init__("ed_coordinator", config.ED_COORDINATOR_SEED, config.ED_COORDINATOR_PORT)
        self.ai_engine = ClaudeEngine()
        self.active_patients = {}
        self.agents = {}
        
        @self.agent.on_event("startup")
        async def startup(ctx: Context):
            logger.info(f"ED Coordinator started: {ctx.agent.address}")
        
        @self.agent.on_message(model=PatientArrivalNotification)
        async def handle_arrival(ctx: Context, sender: str, msg: PatientArrivalNotification):
            await self._process_arrival(ctx, msg)
    
    async def _process_arrival(self, ctx: Context, msg: PatientArrivalNotification):
        logger.info(f"Patient {msg.patient_id} arriving")
        
        # AI analysis
        analysis = await self.ai_engine.analyze_patient_acuity(
            msg.vitals, msg.chief_complaint
        )
        
        self.active_patients[msg.patient_id] = {
            "acuity": analysis.get("acuity_level"),
            "protocol": analysis.get("protocol"),
            "status": "triaged"
        }
        
        # Activate protocol if needed
        if analysis.get("protocol") in ["stemi", "stroke", "trauma", "pediatric"]:
            await self._activate_protocol(ctx, msg.patient_id, analysis.get("protocol"))
    
    async def _activate_protocol(self, ctx: Context, patient_id: str, protocol: str):
        logger.info(f"Activating {protocol.upper()} protocol for {patient_id}")
        for agent_addr in self.agents.values():
            if agent_addr:
                await self.send_message(ctx, agent_addr, 
                    f"PROTOCOL: {protocol.upper()} - Patient {patient_id}")


# ============================================================================
# 2. RESOURCE MANAGER AGENT
# ============================================================================

class ResourceManagerAgent(BaseEDFlowAgent):
    """Manages all ED resources"""
    
    def __init__(self):
        super().__init__("resource_manager", config.RESOURCE_MANAGER_SEED, config.RESOURCE_MANAGER_PORT)
        self.resources = {"beds": 10, "equipment": 20}
        
        @self.agent.on_message(model=ResourceRequest)
        async def handle_request(ctx: Context, sender: str, msg: ResourceRequest):
            await self._allocate_resource(ctx, sender, msg)
    
    async def _allocate_resource(self, ctx: Context, sender: str, msg: ResourceRequest):
        logger.info(f"Resource request: {msg.resource_type}")
        allocated = self.resources.get(msg.resource_type, 0) > 0
        
        if allocated:
            self.resources[msg.resource_type] -= 1
        
        await ctx.send(sender, ResourceAllocation(
            request_id=msg.request_id,
            resource_id=f"res_{msg.request_id}" if allocated else None,
            resource_type=msg.resource_type,
            allocated=allocated,
            timestamp=datetime.utcnow()
        ))


# ============================================================================
# 3. SPECIALIST COORDINATOR AGENT
# ============================================================================

class SpecialistCoordinatorAgent(BaseEDFlowAgent):
    """Coordinates specialist teams"""
    
    def __init__(self):
        super().__init__("specialist_coordinator", config.SPECIALIST_COORDINATOR_SEED, config.SPECIALIST_COORDINATOR_PORT)
        self.teams = {"stemi": [], "stroke": [], "trauma": []}
        
        @self.agent.on_message(model=TeamActivationRequest)
        async def handle_activation(ctx: Context, sender: str, msg: TeamActivationRequest):
            await self._activate_team(ctx, sender, msg)
    
    async def _activate_team(self, ctx: Context, sender: str, msg: TeamActivationRequest):
        logger.info(f"Activating {msg.team_type} team")
        
        await ctx.send(sender, TeamStatus(
            activation_id=msg.activation_id,
            team_type=msg.team_type,
            team_members=[],
            ready=True,
            location="ED",
            timestamp=datetime.utcnow()
        ))


# ============================================================================
# 4. LAB SERVICE AGENT
# ============================================================================

class LabServiceAgent(BaseEDFlowAgent):
    """Manages laboratory services"""
    
    def __init__(self):
        super().__init__("lab_service", config.LAB_SERVICE_SEED, config.LAB_SERVICE_PORT)
        
        @self.agent.on_message(model=LabOrder)
        async def handle_order(ctx: Context, sender: str, msg: LabOrder):
            await self._process_order(ctx, sender, msg)
    
    async def _process_order(self, ctx: Context, sender: str, msg: LabOrder):
        logger.info(f"Lab order for patient {msg.patient_id}: {msg.tests}")
        
        # Simulate processing
        for test in msg.tests:
            await ctx.send(sender, LabResult(
                result_id=f"result_{msg.order_id}_{test}",
                order_id=msg.order_id,
                patient_id=msg.patient_id,
                test_name=test,
                result_value="Normal",
                critical=False,
                result_time=datetime.utcnow(),
                reported_by="Lab System"
            ))


# ============================================================================
# 5. PHARMACY AGENT
# ============================================================================

class PharmacyAgent(BaseEDFlowAgent):
    """Manages medication orders"""
    
    def __init__(self):
        super().__init__("pharmacy", config.PHARMACY_SEED, config.PHARMACY_PORT)
        
        @self.agent.on_message(model=MedicationOrder)
        async def handle_order(ctx: Context, sender: str, msg: MedicationOrder):
            await self._process_order(ctx, sender, msg)
    
    async def _process_order(self, ctx: Context, sender: str, msg: MedicationOrder):
        logger.info(f"Medication order: {msg.medication_name} for {msg.patient_id}")
        
        await ctx.send(sender, MedicationDelivery(
            delivery_id=f"delivery_{msg.order_id}",
            order_id=msg.order_id,
            patient_id=msg.patient_id,
            medication_name=msg.medication_name,
            status="delivered",
            delivery_time=datetime.utcnow()
        ))


# ============================================================================
# 6. BED MANAGEMENT AGENT
# ============================================================================

class BedManagementAgent(BaseEDFlowAgent):
    """Manages bed assignments"""
    
    def __init__(self):
        super().__init__("bed_management", config.BED_MANAGEMENT_SEED, config.BED_MANAGEMENT_PORT)
        self.available_beds = ["Bed1", "Bed2", "Bed3", "Bed4", "Bed5"]
        
        @self.agent.on_message(model=BedRequest)
        async def handle_request(ctx: Context, sender: str, msg: BedRequest):
            await self._assign_bed(ctx, sender, msg)
    
    async def _assign_bed(self, ctx: Context, sender: str, msg: BedRequest):
        logger.info(f"Bed request for patient {msg.patient_id}")
        
        bed_id = self.available_beds.pop(0) if self.available_beds else None
        
        await ctx.send(sender, BedAssignment(
            assignment_id=f"assign_{msg.request_id}",
            request_id=msg.request_id,
            patient_id=msg.patient_id,
            bed_id=bed_id,
            bed_location=f"ED-{bed_id}" if bed_id else None,
            assigned=bed_id is not None,
            assignment_time=datetime.utcnow() if bed_id else None
        ))


# ============================================================================
# AGENT FACTORY
# ============================================================================

def create_agent(agent_type: str):
    """Factory function to create agents"""
    agents = {
        "ed_coordinator": EDCoordinatorAgent,
        "resource_manager": ResourceManagerAgent,
        "specialist_coordinator": SpecialistCoordinatorAgent,
        "lab_service": LabServiceAgent,
        "pharmacy": PharmacyAgent,
        "bed_management": BedManagementAgent,
    }
    
    if agent_type not in agents:
        raise ValueError(f"Unknown agent type: {agent_type}")
    
    return agents[agent_type]()


# Main entry point
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        agent = create_agent(sys.argv[1])
        agent.run()
    else:
        print("Usage: python agents.py <agent_type>")
        print("Agent types: ed_coordinator, resource_manager, specialist_coordinator, lab_service, pharmacy, bed_management")