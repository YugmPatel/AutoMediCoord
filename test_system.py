"""
AutoMediCoord System Tests
"""

import asyncio
import pytest
from datetime import datetime
from src.models import (
    PatientArrivalNotification,
    ResourceRequest,
    TeamActivationRequest,
    LabOrder,
    MedicationOrder,
    BedRequest
)
from src.ai import ClaudeEngine


class TestModels:
    """Test data models"""
    
    def test_patient_arrival_creation(self):
        """Test creating patient arrival notification"""
        patient = PatientArrivalNotification(
            patient_id="TEST_001",
            arrival_time=datetime.utcnow(),
            vitals={"hr": 90, "bp": "120/80"},
            chief_complaint="Test complaint",
            ems_report="Test report",
            priority=1
        )
        assert patient.patient_id == "TEST_001"
        assert patient.priority == 1
    
    def test_resource_request_creation(self):
        """Test creating resource request"""
        request = ResourceRequest(
            request_id="REQ_001",
            resource_type="bed",
            requirements={},
            priority=1,
            patient_id="TEST_001",
            requesting_agent="test_agent",
            timestamp=datetime.utcnow()
        )
        assert request.resource_type == "bed"
        assert request.priority == 1


class TestClaudeAI:
    """Test Claude AI engine"""
    
    @pytest.mark.asyncio
    async def test_acuity_analysis_fallback(self):
        """Test acuity analysis with fallback (no API key needed)"""
        engine = ClaudeEngine()
        
        result = await engine.analyze_patient_acuity(
            vitals={"hr": 95, "bp": "145/90"},
            symptoms="chest pain radiating to left arm"
        )
        
        assert "acuity_level" in result
        assert "protocol" in result
        assert result["protocol"] == "stemi"  # Should detect STEMI from symptoms
        assert result["acuity_level"] == "1"  # Critical
    
    @pytest.mark.asyncio
    async def test_acuity_analysis_stroke(self):
        """Test stroke detection"""
        engine = ClaudeEngine()
        
        result = await engine.analyze_patient_acuity(
            vitals={"hr": 88, "bp": "165/95"},
            symptoms="sudden weakness and facial droop"
        )
        
        assert result["protocol"] == "stroke"
        assert result["acuity_level"] == "1"
    
    @pytest.mark.asyncio
    async def test_acuity_analysis_trauma(self):
        """Test trauma detection"""
        engine = ClaudeEngine()
        
        result = await engine.analyze_patient_acuity(
            vitals={"hr": 125, "bp": "85/55"},
            symptoms="motor vehicle accident, chest trauma"
        )
        
        assert result["protocol"] == "trauma"
        assert result["acuity_level"] == "1"


def run_tests():
    """Run all tests"""
    print("Running AutoMediCoord Tests...")
    print("=" * 60)
    
    # Test models
    print("\n📦 Testing Data Models...")
    test_models = TestModels()
    test_models.test_patient_arrival_creation()
    test_models.test_resource_request_creation()
    print("✅ Data models: PASSED")
    
    # Test AI (using asyncio)
    print("\n🧠 Testing Claude AI Engine...")
    test_ai = TestClaudeAI()
    
    async def run_ai_tests():
        await test_ai.test_acuity_analysis_fallback()
        await test_ai.test_acuity_analysis_stroke()
        await test_ai.test_acuity_analysis_trauma()
    
    asyncio.run(run_ai_tests())
    print("✅ Claude AI engine: PASSED")
    
    print("\n" + "=" * 60)
    print("✅ All Tests Passed!")
    print("=" * 60)
    print("\nSystem is ready for deployment.")


if __name__ == "__main__":
    run_tests()