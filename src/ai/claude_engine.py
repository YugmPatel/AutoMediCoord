"""
Claude AI integration for EDFlow AI reasoning engine
"""

import asyncio
from typing import Dict, Any, Optional, List
from anthropic import Anthropic, AsyncAnthropic
from ..utils.config import get_config
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ClaudeEngine:
    """
    Claude AI reasoning engine for EDFlow AI
    Provides intelligent decision-making capabilities
    """
    
    def __init__(self):
        """Initialize Claude AI client"""
        config = get_config()
        self.api_key = config.ANTHROPIC_API_KEY
        self.timeout = config.AI_RESPONSE_TIMEOUT_SECONDS
        
        if not self.api_key:
            logger.warning("ANTHROPIC_API_KEY not set - AI features will be limited")
        
        # Initialize async client
        self.client = AsyncAnthropic(api_key=self.api_key) if self.api_key else None
        self.model = "claude-3-5-sonnet-20241022"  # Latest Claude model
        
        logger.info(f"Claude AI engine initialized with model: {self.model}")
    
    async def analyze_patient_acuity(
        self,
        vitals: Dict[str, Any],
        symptoms: str,
        history: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze patient acuity and recommend protocol
        
        Args:
            vitals: Patient vital signs
            symptoms: Chief complaint and symptoms
            history: Medical history (optional)
            
        Returns:
            Dict with acuity score, protocol recommendation, risk factors
        """
        if not self.client:
            logger.warning("Claude AI not configured - using fallback")
            return self._fallback_acuity_analysis(vitals, symptoms)
        
        prompt = f"""You are an emergency medicine AI assistant analyzing a patient presentation.

Patient Information:
- Vitals: {vitals}
- Chief Complaint/Symptoms: {symptoms}
- Medical History: {history or 'Not provided'}

Based on the Emergency Severity Index (ESI), analyze this patient and provide:
1. ESI Level (1-5, where 1 is most critical)
2. Recommended emergency protocol (STEMI, Stroke, Trauma, Pediatric, or General)
3. Key risk factors identified
4. Confidence level (0.0-1.0)
5. Recommended immediate actions

Respond in JSON format:
{{
    "acuity_level": "1-5",
    "protocol": "STEMI|Stroke|Trauma|Pediatric|General",
    "risk_factors": ["factor1", "factor2"],
    "confidence": 0.0-1.0,
    "immediate_actions": ["action1", "action2"],
    "reasoning": "brief explanation"
}}"""
        
        try:
            response = await asyncio.wait_for(
                self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                ),
                timeout=self.timeout
            )
            
            # Parse response
            content = response.content[0].text
            # Extract JSON from response (handling potential markdown formatting)
            import json
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                logger.info(f"Patient acuity analysis complete: Level {result.get('acuity_level')}")
                return result
            else:
                logger.error("Failed to parse Claude response")
                return self._fallback_acuity_analysis(vitals, symptoms)
                
        except asyncio.TimeoutError:
            logger.error(f"Claude AI timeout after {self.timeout}s")
            return self._fallback_acuity_analysis(vitals, symptoms)
        except Exception as e:
            error_msg = str(e) if str(e) else f"{type(e).__name__}: {repr(e)}"
            logger.error(f"Claude AI error: {error_msg}")
            logger.debug(f"Full exception: {e.__class__.__module__}.{e.__class__.__name__}")
            if hasattr(e, 'response'):
                logger.debug(f"Response: {e.response}")
            if "authentication" in error_msg.lower() or "api_key" in error_msg.lower():
                logger.error("API Key issue - check ANTHROPIC_API_KEY in .env")
            return self._fallback_acuity_analysis(vitals, symptoms)
    
    async def optimize_resources(
        self,
        available_resources: Dict[str, Any],
        patient_needs: List[Dict[str, Any]],
        current_load: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Optimize resource allocation across multiple patients
        
        Args:
            available_resources: Available beds, equipment, staff
            patient_needs: List of patient resource requirements
            current_load: Current ED load and utilization
            
        Returns:
            Optimal resource allocation plan
        """
        if not self.client:
            return self._fallback_resource_optimization(available_resources, patient_needs)
        
        prompt = f"""You are an ED resource optimization AI.

Available Resources: {available_resources}
Patient Needs: {patient_needs}
Current Load: {current_load}

Provide an optimal allocation plan that:
1. Prioritizes critical patients (acuity level 1-2)
2. Maximizes resource utilization
3. Minimizes wait times
4. Identifies potential conflicts

Respond in JSON format with allocation plan and reasoning."""
        
        try:
            response = await asyncio.wait_for(
                self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                ),
                timeout=self.timeout
            )
            
            content = response.content[0].text
            import json
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._fallback_resource_optimization(available_resources, patient_needs)
                
        except Exception as e:
            logger.error(f"Resource optimization error: {str(e)}")
            return self._fallback_resource_optimization(available_resources, patient_needs)
    
    async def sequence_priorities(
        self,
        patients: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Sequence multiple concurrent patients by priority
        
        Args:
            patients: List of patient information
            
        Returns:
            Prioritized sequence with timing recommendations
        """
        if not self.client:
            return self._fallback_priority_sequencing(patients)
        
        prompt = f"""You are an ED patient sequencing AI.

Concurrent Patients: {patients}

Determine the optimal sequence for:
1. Treatment initiation order
2. Resource allocation timing
3. Parallel vs sequential processing

Respond in JSON format with prioritized sequence and reasoning."""
        
        try:
            response = await asyncio.wait_for(
                self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                ),
                timeout=self.timeout
            )
            
            content = response.content[0].text
            import json
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._fallback_priority_sequencing(patients)
                
        except Exception as e:
            logger.error(f"Priority sequencing error: {str(e)}")
            return self._fallback_priority_sequencing(patients)
    
    async def resolve_conflict(
        self,
        conflict_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Resolve resource conflicts intelligently
        
        Args:
            conflict_details: Details of the resource conflict
            
        Returns:
            Resolution strategy and alternatives
        """
        if not self.client:
            return self._fallback_conflict_resolution(conflict_details)
        
        prompt = f"""You are an ED conflict resolution AI.

Conflict Details: {conflict_details}

Provide a resolution strategy that:
1. Minimizes patient risk
2. Offers alternative solutions
3. Escalates if necessary
4. Explains the reasoning

Respond in JSON format with resolution strategy."""
        
        try:
            response = await asyncio.wait_for(
                self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                ),
                timeout=self.timeout
            )
            
            content = response.content[0].text
            import json
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._fallback_conflict_resolution(conflict_details)
                
        except Exception as e:
            logger.error(f"Conflict resolution error: {str(e)}")
            return self._fallback_conflict_resolution(conflict_details)
    
    # Fallback methods when Claude AI is not available
    
    def _fallback_acuity_analysis(self, vitals: Dict[str, Any], symptoms: str) -> Dict[str, Any]:
        """Simple rule-based fallback for acuity analysis"""
        logger.info("Using fallback acuity analysis")
        
        # Simple heuristics
        acuity = "3"  # Default moderate
        protocol = "general"
        
        # Check for critical vitals
        if vitals.get("heart_rate", 0) > 120 or vitals.get("blood_pressure_systolic", 0) > 180:
            acuity = "2"
        
        # Check for STEMI keywords
        if any(word in symptoms.lower() for word in ["chest pain", "mi", "stemi", "cardiac"]):
            protocol = "stemi"
            acuity = "1"
        
        # Check for stroke keywords
        elif any(word in symptoms.lower() for word in ["stroke", "cva", "facial droop", "weakness"]):
            protocol = "stroke"
            acuity = "1"
        
        # Check for trauma keywords
        elif any(word in symptoms.lower() for word in ["trauma", "mva", "accident", "injury"]):
            protocol = "trauma"
            acuity = "1"
        
        return {
            "acuity_level": acuity,
            "protocol": protocol,
            "risk_factors": ["vitals_abnormal"] if acuity in ["1", "2"] else [],
            "confidence": 0.7,
            "immediate_actions": ["assess", "monitor"],
            "reasoning": "Rule-based fallback analysis"
        }
    
    def _fallback_resource_optimization(
        self,
        available_resources: Dict[str, Any],
        patient_needs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Simple fallback for resource optimization"""
        logger.info("Using fallback resource optimization")
        return {
            "allocation_plan": "sequential_by_priority",
            "reasoning": "Simple priority-based allocation",
            "estimated_wait_times": {}
        }
    
    def _fallback_priority_sequencing(self, patients: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simple fallback for priority sequencing"""
        logger.info("Using fallback priority sequencing")
        return {
            "sequence": sorted(patients, key=lambda p: p.get("acuity", 5)),
            "reasoning": "Simple acuity-based ordering"
        }
    
    def _fallback_conflict_resolution(self, conflict_details: Dict[str, Any]) -> Dict[str, Any]:
        """Simple fallback for conflict resolution"""
        logger.info("Using fallback conflict resolution")
        return {
            "resolution": "escalate_to_human",
            "alternatives": [],
            "reasoning": "Complex conflict requires human decision"
        }