"""
Claude AI Engine - Consolidated
"""

import asyncio
import json
import re
from typing import Dict, Any, List
from anthropic import AsyncAnthropic
from .utils import get_config, get_logger

logger = get_logger(__name__)


class ClaudeEngine:
    """Claude AI reasoning engine for EDFlow AI"""
    
    def __init__(self):
        config = get_config()
        self.api_key = config.ANTHROPIC_API_KEY
        self.timeout = config.AI_RESPONSE_TIMEOUT_SECONDS
        self.client = AsyncAnthropic(api_key=self.api_key) if self.api_key else None
        self.model = "claude-3-5-sonnet-20241022"
        logger.info(f"Claude AI engine initialized")
    
    async def analyze_patient_acuity(
        self,
        vitals: Dict[str, Any],
        symptoms: str,
        history: str = None,
        context: str = None
    ) -> Dict[str, Any]:
        """
        Analyze patient acuity and recommend protocol
        
        Args:
            vitals: Patient vital signs
            symptoms: Chief complaint/symptoms
            history: Medical history
            context: Additional context from Letta memory (patient history, similar cases)
        """
        if not self.client:
            return self._fallback_acuity(vitals, symptoms)
        
        # Build prompt with context if available
        context_section = ""
        if context:
            context_section = f"\nHistorical Context from Previous Cases:\n{context}\n"
        
        prompt = f"""Emergency medicine AI assistant analyzing patient:

Vitals: {vitals}
Symptoms: {symptoms}
History: {history or 'Not provided'}{context_section}

Analyze the patient and provide:
1. ESI acuity level (1=immediate, 5=non-urgent)
2. Recommended protocol
3. Key risk factors
4. Confidence in assessment
5. Immediate actions needed

{f"Consider the historical context when making your assessment." if context else ""}

JSON format:
{{
    "acuity_level": "1-5",
    "protocol": "stemi|stroke|trauma|pediatric|general",
    "risk_factors": ["factor1"],
    "confidence": 0.0-1.0,
    "immediate_actions": ["action1"]
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
            
            content = response.content[0].text
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return self._fallback_acuity(vitals, symptoms)
        except Exception as e:
            logger.error(f"Claude AI error: {str(e)}")
            return self._fallback_acuity(vitals, symptoms)
    
    def _fallback_acuity(self, vitals: Dict[str, Any], symptoms: str) -> Dict[str, Any]:
        """Rule-based fallback"""
        acuity = "3"
        protocol = "general"
        
        if any(word in symptoms.lower() for word in ["chest pain", "mi", "stemi"]):
            protocol = "stemi"
            acuity = "1"
        elif any(word in symptoms.lower() for word in ["stroke", "cva", "weakness"]):
            protocol = "stroke"
            acuity = "1"
        elif any(word in symptoms.lower() for word in ["trauma", "accident", "injury"]):
            protocol = "trauma"
            acuity = "1"
        
        return {
            "acuity_level": acuity,
            "protocol": protocol,
            "risk_factors": [],
            "confidence": 0.7,
            "immediate_actions": ["assess", "monitor"]
        }