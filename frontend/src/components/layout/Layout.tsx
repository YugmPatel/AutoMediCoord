import React, { useState, useEffect } from "react";
import Header from "./Header";
import MetricsCards from "../dashboard/MetricsCards";
import LiveCases from "../dashboard/LiveCases";
import ActivityLog from "../dashboard/ActivityLog";
import ChatInterface from "../chat/ChatInterface";
import {
  mockData,
  simulatePatientArrival,
  addNewMockMessage,
} from "../../services/mockData";
import {
  PatientCase,
  DashboardMetrics,
  ActivityEntry,
  ChatMessage,
} from "../../services/types";

const Layout: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics>(mockData.metrics);
  const [cases, setCases] = useState<PatientCase[]>(mockData.cases);
  const [activities, setActivities] = useState<ActivityEntry[]>(
    mockData.activities
  );
  const [messages, setMessages] = useState<ChatMessage[]>(mockData.messages);
  const [isConnected, setIsConnected] = useState(true);

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      // Update metrics
      setMetrics((prev) => ({
        ...prev,
        lastUpdated: new Date(),
      }));

      // Simulate occasional new activities
      if (Math.random() < 0.3) {
        const newActivity: ActivityEntry = {
          id: String(Date.now()),
          timestamp: new Date(),
          type: ["Lab", "Pharm", "System"][
            Math.floor(Math.random() * 3)
          ] as ActivityEntry["type"],
          message: [
            "Lab results ready",
            "Medication prepared",
            "Bed assignment updated",
            "Doctor notification sent",
          ][Math.floor(Math.random() * 4)],
          status: ["Ready", "Complete", "Pending"][
            Math.floor(Math.random() * 3)
          ] as ActivityEntry["status"],
        };

        setActivities((prev) => [newActivity, ...prev].slice(0, 20));
      }
    }, 10000); // Update every 10 seconds

    return () => clearInterval(interval);
  }, []);

  const handleSimulateSTEMI = () => {
    const newPatient = simulatePatientArrival("STEMI");
    setCases((prev) => [newPatient, ...prev]);

    // Update metrics
    setMetrics((prev) => ({
      ...prev,
      activeCases: prev.activeCases + 1,
      lastUpdated: new Date(),
    }));

    // Add system message
    const systemMessage = addNewMockMessage(
      `New STEMI patient arrived: ${newPatient.id}`,
      "System"
    );
    setMessages((prev) => [...prev, systemMessage]);

    // Add activity
    const newActivity: ActivityEntry = {
      id: String(Date.now()),
      timestamp: new Date(),
      type: "System",
      message: `STEMI protocol activated for ${newPatient.id}`,
      status: "In Progress",
      caseId: newPatient.id,
    };
    setActivities((prev) => [newActivity, ...prev]);
  };

  const handleSimulateStroke = () => {
    const newPatient = simulatePatientArrival("Stroke");
    setCases((prev) => [newPatient, ...prev]);

    // Update metrics
    setMetrics((prev) => ({
      ...prev,
      activeCases: prev.activeCases + 1,
      lastUpdated: new Date(),
    }));

    // Add system message
    const systemMessage = addNewMockMessage(
      `New Stroke patient arrived: ${newPatient.id}`,
      "System"
    );
    setMessages((prev) => [...prev, systemMessage]);

    // Add activity
    const newActivity: ActivityEntry = {
      id: String(Date.now()),
      timestamp: new Date(),
      type: "System",
      message: `Stroke protocol activated for ${newPatient.id}`,
      status: "In Progress",
      caseId: newPatient.id,
    };
    setActivities((prev) => [newActivity, ...prev]);
  };

  const handleSendMessage = (message: string) => {
    const userMessage = addNewMockMessage(message, "User");
    setMessages((prev) => [...prev, userMessage]);

    // Simulate agent response after a delay
    setTimeout(() => {
      const agentResponse = addNewMockMessage(
        "Message received. Processing request...",
        "ED Coordinator",
        "ed_coordinator"
      );
      setMessages((prev) => [...prev, agentResponse]);
    }, 1000);
  };

  const handleCaseClick = (caseId: string) => {
    console.log("Case clicked:", caseId);
    // Here you would typically open a detailed view or modal
  };

  return (
    <div className="min-h-screen bg-gray-950">
      <Header
        onSimulateSTEMI={handleSimulateSTEMI}
        onSimulateStroke={handleSimulateStroke}
        isConnected={isConnected}
      />

      <main className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-3 space-y-8">
            {/* Metrics Cards */}
            <MetricsCards metrics={metrics} />

            {/* Live Cases */}
            <LiveCases cases={cases} onCaseClick={handleCaseClick} />

            {/* Activity Log */}
            <ActivityLog entries={activities} />
          </div>

          {/* Chat Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8">
              <ChatInterface
                messages={messages}
                onSendMessage={handleSendMessage}
                isConnected={isConnected}
                className="h-[600px]"
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Layout;
