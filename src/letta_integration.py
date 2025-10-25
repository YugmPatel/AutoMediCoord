"""
Letta Integration Module
Provides persistent memory and learning capabilities for EDFlow AI agents
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import json
from .utils import get_config, get_logger

logger = get_logger(__name__)
config = get_config()


class PatientMemoryAgent:
    """
    Letta-powered patient history and context manager
    Provides persistent memory across sessions for learning and context-aware decisions
    """
    
    def __init__(self):
        self.config = config
        self.enabled = config.LETTA_ENABLED
        self.client = None
        self.agent_id = None
        
        # In-memory fallback if Letta is disabled or unavailable
        self.memory_store = {
            "patients": {},
            "protocols": {},
            "resources": {},
            "teams": {}
        }
        
        if self.enabled and config.LETTA_API_KEY:
            try:
                self._initialize_letta()
            except Exception as e:
                logger.warning(f"Letta initialization failed, using fallback memory: {e}")
                self.enabled = False
    
    def _initialize_letta(self):
        """Initialize Letta client and agent"""
        try:
            from letta import create_client
            
            self.client = create_client()
            logger.info("Letta client created successfully")
            
            # Create or get existing agent
            self.agent_id = self._create_or_get_agent()
            logger.info(f"Letta agent initialized: {self.agent_id}")
            
        except ImportError:
            logger.warning("Letta library not installed. Install with: pip install letta")
            self.enabled = False
        except Exception as e:
            logger.error(f"Failed to initialize Letta: {e}")
            self.enabled = False
    
    def _create_or_get_agent(self) -> str:
        """Create or retrieve existing EDFlowAI memory agent"""
        try:
            # Try to find existing agent
            agents = self.client.list_agents()
            for agent in agents:
                if agent.name == "EDFlowAI_memory":
                    return agent.id
            
            # Create new agent with medical context
            agent = self.client.create_agent(
                name="EDFlowAI_memory",
                system="""You are a medical context manager for an emergency department coordination system.
                
Your responsibilities:
1. Remember patient histories, including:
   - Previous visits and their outcomes
   - Known allergies and medical conditions
   - Past protocol activations and their effectiveness
   - Response times and team performance

2. Track protocol effectiveness:
   - Door-to-balloon times for STEMI cases
   - Door-to-needle times for stroke cases
   - Resource utilization patterns
   - Team coordination efficiency

3. Provide actionable context:
   - When a patient arrives, recall their history
   - When a protocol is activated, provide insights from similar past cases
   - When resources are requested, suggest optimal allocation based on patterns

4. Learn and improve:
   - Identify successful patterns
   - Flag potential issues based on historical data
   - Recommend process improvements

Always provide concise, actionable information focused on improving patient outcomes and operational efficiency.""",
                llm_config={
                    "model": "claude-3-5-sonnet-20241022",
                    "model_endpoint": "anthropic",
                    "context_window": 200000
                }
            )
            
            return agent.id
            
        except Exception as e:
            logger.error(f"Failed to create/get Letta agent: {e}")
            raise
    
    async def recall_patient_context(self, patient_id: str, current_complaint: str) -> str:
        """
        Retrieve patient history and context from Letta's memory
        Returns a formatted string with relevant historical information
        """
        if not self.enabled or not self.client:
            # Fallback to in-memory store
            patient_data = self.memory_store["patients"].get(patient_id, {})
            if patient_data:
                return f"Previous visit found: {patient_data.get('last_protocol', 'Unknown')} protocol " \
                       f"on {patient_data.get('last_visit', 'Unknown date')}"
            return "No previous history found (new patient)"
        
        try:
            message = f"""
Patient {patient_id} has arrived with complaint: {current_complaint}

Please provide:
1. Any previous visits and their outcomes
2. Known allergies or medical conditions
3. Previous protocols activated and their effectiveness
4. Any relevant context that could help with this emergency

Be concise and focus on actionable information.
"""
            
            response = self.client.send_message(
                agent_id=self.agent_id,
                message=message,
                role="user"
            )
            
            # Extract text from response
            context_text = response.messages[-1].text if response.messages else "No context available"
            logger.info(f"Retrieved patient context for {patient_id}")
            return context_text
            
        except Exception as e:
            logger.error(f"Error retrieving patient context: {e}")
            return "Context retrieval unavailable"
    
    async def get_protocol_insights(self, protocol: str) -> str:
        """
        Get insights on protocol effectiveness from Letta's memory
        Returns historical performance data and recommendations
        """
        if not self.enabled or not self.client:
            # Fallback to in-memory store
            protocol_data = self.memory_store["protocols"].get(protocol, {})
            if protocol_data:
                avg_time = protocol_data.get('avg_response_time', 'Unknown')
                return f"Historical average response time: {avg_time} minutes"
            return "No historical protocol data available"
        
        try:
            message = f"""
We're about to activate the {protocol.upper()} protocol.

Based on your memory of past {protocol.upper()} cases, please provide:
1. Average response times (door-to-balloon, door-to-needle, etc.)
2. Common issues or bottlenecks encountered
3. Best practices that led to successful outcomes
4. Any recommendations for this activation

Be brief and actionable.
"""
            
            response = self.client.send_message(
                agent_id=self.agent_id,
                message=message,
                role="user"
            )
            
            insights = response.messages[-1].text if response.messages else "No insights available"
            logger.info(f"Retrieved protocol insights for {protocol}")
            return insights
            
        except Exception as e:
            logger.error(f"Error retrieving protocol insights: {e}")
            return "Insights unavailable"
    
    async def remember_patient_case(
        self,
        patient_id: str,
        protocol: str,
        vitals: Dict[str, Any],
        outcome: Dict[str, Any]
    ):
        """
        Store patient case in Letta's persistent memory for future learning
        """
        if not self.enabled or not self.client:
            # Store in fallback memory
            self.memory_store["patients"][patient_id] = {
                "last_protocol": protocol,
                "last_visit": datetime.utcnow().isoformat(),
                "vitals": vitals,
                "outcome": outcome
            }
            logger.info(f"Stored case in fallback memory: {patient_id}")
            return
        
        try:
            message = f"""
Please remember this patient case for future reference:

Patient ID: {patient_id}
Protocol: {protocol.upper()}
Visit Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}

Vitals:
- Heart Rate: {vitals.get('hr', 'N/A')} bpm
- Blood Pressure: {vitals.get('bp_sys', 'N/A')}/{vitals.get('bp_dia', 'N/A')} mmHg
- SpO2: {vitals.get('spo2', 'N/A')}%
- Temperature: {vitals.get('temp', 'N/A')}°C

Outcome:
{json.dumps(outcome, indent=2)}

Store this case in your memory for future reference when this patient returns or when similar cases occur.
"""
            
            self.client.send_message(
                agent_id=self.agent_id,
                message=message,
                role="user"
            )
            
            logger.info(f"Stored patient case in Letta memory: {patient_id}")
            
        except Exception as e:
            logger.error(f"Error storing patient case: {e}")
    
    async def get_resource_recommendations(self, resource_type: str, patient_priority: int) -> str:
        """
        Get resource allocation recommendations based on historical patterns
        """
        if not self.enabled or not self.client:
            return f"Standard {resource_type} allocation for priority {patient_priority}"
        
        try:
            message = f"""
We need to allocate a {resource_type} for a priority {patient_priority} patient.

Based on your memory:
1. What resources have been most effective for similar cases?
2. Are there any patterns in resource availability we should consider?
3. Any recommendations for optimal allocation?

Keep it brief and actionable.
"""
            
            response = self.client.send_message(
                agent_id=self.agent_id,
                message=message,
                role="user"
            )
            
            recommendations = response.messages[-1].text if response.messages else "No recommendations"
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting resource recommendations: {e}")
            return "Recommendations unavailable"
    
    async def store_protocol_performance(
        self,
        protocol: str,
        response_time_seconds: float,
        success: bool,
        notes: Optional[str] = None
    ):
        """
        Store protocol performance metrics for learning
        """
        if not self.enabled or not self.client:
            # Update fallback memory
            if protocol not in self.memory_store["protocols"]:
                self.memory_store["protocols"][protocol] = {
                    "total_cases": 0,
                    "total_time": 0,
                    "successes": 0
                }
            
            data = self.memory_store["protocols"][protocol]
            data["total_cases"] += 1
            data["total_time"] += response_time_seconds
            if success:
                data["successes"] += 1
            data["avg_response_time"] = data["total_time"] / data["total_cases"]
            
            return
        
        try:
            message = f"""
Protocol performance data to remember:

Protocol: {protocol.upper()}
Response Time: {response_time_seconds:.1f} seconds ({response_time_seconds/60:.2f} minutes)
Success: {'Yes' if success else 'No'}
Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
{f'Notes: {notes}' if notes else ''}

Use this to improve future protocol activations and identify patterns.
"""
            
            self.client.send_message(
                agent_id=self.agent_id,
                message=message,
                role="user"
            )
            
            logger.info(f"Stored protocol performance: {protocol}")
            
        except Exception as e:
            logger.error(f"Error storing protocol performance: {e}")
    
    def is_available(self) -> bool:
        """Check if Letta is available and working"""
        return self.enabled and self.client is not None


# Global instance
_memory_agent: Optional[PatientMemoryAgent] = None


def get_memory_agent() -> PatientMemoryAgent:
    """Get or create the global memory agent instance"""
    global _memory_agent
    if _memory_agent is None:
        _memory_agent = PatientMemoryAgent()
    return _memory_agent