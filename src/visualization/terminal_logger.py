"""
Rich-based terminal visualization for agent communication
Beautiful, live-updating terminal UI
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from rich.console import Console, Group
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.box import ROUNDED, DOUBLE
from collections import deque
import asyncio

from .event_tracker import EventTracker, AgentEvent, EventType, get_event_tracker


class TerminalLogger:
    """Rich-based terminal logger for live agent visualization"""
    
    def __init__(self, event_tracker: Optional[EventTracker] = None, max_messages: int = 15):
        self.console = Console()
        self.event_tracker = event_tracker or get_event_tracker()
        self.max_messages = max_messages
        self.message_buffer = deque(maxlen=max_messages)
        self.layout = Layout()
        self.live = None
        self.protocol_progress: Dict[str, Progress] = {}
        self.running = False
        
        # Setup layout
        self._setup_layout()
    
    def _setup_layout(self):
        """Setup the terminal layout"""
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        
        self.layout["main"].split_row(
            Layout(name="agents", ratio=2),
            Layout(name="messages", ratio=3)
        )
    
    def _create_header(self) -> Panel:
        """Create the header panel"""
        uptime = int(self.event_tracker.get_uptime_seconds())
        msg_rate = self.event_tracker.get_message_rate()
        
        header_text = Text()
        header_text.append("🏥 EDFlow AI ", style="bold cyan")
        header_text.append("Multi-Agent Emergency Department System", style="bold white")
        header_text.append(f" | Uptime: {uptime}s", style="dim")
        header_text.append(f" | Msg Rate: {msg_rate:.1f}/s", style="dim")
        
        return Panel(
            header_text,
            box=DOUBLE,
            style="cyan"
        )
    
    def _create_agent_panel(self) -> Panel:
        """Create the agent status panel"""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            box=ROUNDED,
            padding=(0, 1)
        )
        
        table.add_column("Agent", style="cyan", no_wrap=True, width=25)
        table.add_column("Status", justify="center", width=10)
        table.add_column("Msgs", justify="right", width=8)
        table.add_column("Latency", justify="right", width=10)
        
        # Add all 6 agents
        agent_order = [
            "ed_coordinator",
            "resource_manager",
            "specialist_coordinator",
            "lab_service",
            "pharmacy",
            "bed_management"
        ]
        
        agent_names = {
            "ed_coordinator": "ED Coordinator",
            "resource_manager": "Resource Manager",
            "specialist_coordinator": "Specialist Coord",
            "lab_service": "Lab Service",
            "pharmacy": "Pharmacy",
            "bed_management": "Bed Management"
        }
        
        for agent_key in agent_order:
            emoji = self.event_tracker.get_agent_emoji(agent_key)
            name = agent_names.get(agent_key, agent_key)
            stats = self.event_tracker.get_agent_stats(agent_key)
            
            # Status indicator
            if stats.get("last_activity"):
                time_since = (datetime.utcnow() - stats["last_activity"]).total_seconds()
                if time_since < 5:
                    status = Text("🟢 ACTIVE", style="bold green")
                elif time_since < 30:
                    status = Text("🟡 IDLE", style="yellow")
                else:
                    status = Text("⚪ WAITING", style="dim")
            else:
                status = Text("⚫ READY", style="dim")
            
            # Message count
            msg_count = stats.get("messages_sent", 0) + stats.get("messages_received", 0)
            
            # Latency
            avg_latency = stats.get("avg_latency_ms", 0)
            if avg_latency > 0:
                latency_text = f"{avg_latency:.0f}ms"
                if avg_latency < 50:
                    latency_style = "green"
                elif avg_latency < 100:
                    latency_style = "yellow"
                else:
                    latency_style = "red"
            else:
                latency_text = "-"
                latency_style = "dim"
            
            table.add_row(
                f"{emoji} {name}",
                status,
                str(msg_count),
                Text(latency_text, style=latency_style)
            )
        
        return Panel(
            table,
            title="[bold cyan]🤖 Agent Status[/bold cyan]",
            border_style="cyan",
            box=ROUNDED
        )
    
    def _create_message_panel(self) -> Panel:
        """Create the message stream panel"""
        if not self.message_buffer:
            content = Text("Waiting for agent communication...", style="dim italic")
        else:
            content_lines = []
            for event in self.message_buffer:
                timestamp = event.timestamp.strftime("%H:%M:%S.%f")[:-3]
                
                # Format based on event type
                if event.event_type == EventType.MESSAGE_SENT and event.from_agent and event.to_agent:
                    from_emoji = self.event_tracker.get_agent_emoji(event.from_agent)
                    to_emoji = self.event_tracker.get_agent_emoji(event.to_agent)
                    from_color = self.event_tracker.get_agent_color(event.from_agent)
                    to_color = self.event_tracker.get_agent_color(event.to_agent)
                    
                    line = Text()
                    line.append(f"[{timestamp}] ", style="dim")
                    line.append(from_emoji, style=f"bold {from_color}")
                    line.append("→", style="bold white")
                    line.append(to_emoji, style=f"bold {to_color}")
                    line.append(f"  {event.message_type or 'Message':<22}", style="bold white")
                    line.append(f" | {event.description}", style="white")
                    
                elif event.event_type == EventType.PROTOCOL_ACTIVATED:
                    emoji = self.event_tracker.get_agent_emoji(event.agent_name)
                    line = Text()
                    line.append(f"[{timestamp}] ", style="dim")
                    line.append(f"{emoji}  ", style="bold cyan")
                    line.append(f"🚨 PROTOCOL: {event.protocol.upper()}", style="bold red")
                    line.append(f" - {event.description}", style="yellow")
                    
                elif event.event_type == EventType.PROTOCOL_STEP:
                    line = Text()
                    line.append(f"[{timestamp}] ", style="dim")
                    line.append(f"   ├─ ", style="cyan")
                    line.append(event.description, style="green")
                    
                else:
                    emoji = self.event_tracker.get_agent_emoji(event.agent_name)
                    color = self.event_tracker.get_agent_color(event.agent_name)
                    line = Text()
                    line.append(f"[{timestamp}] ", style="dim")
                    line.append(f"{emoji}  ", style=f"bold {color}")
                    line.append(event.description, style="white")
                
                content_lines.append(line)
            
            content = Group(*content_lines)
        
        return Panel(
            content,
            title="[bold green]📨 Message Flow[/bold green]",
            border_style="green",
            box=ROUNDED
        )
    
    def _create_footer(self) -> Panel:
        """Create the footer panel"""
        footer_text = Text()
        footer_text.append("🎯 ", style="bold yellow")
        footer_text.append("Live Agent Coordination Demo", style="bold white")
        footer_text.append(" | Press Ctrl+C to stop", style="dim")
        
        return Panel(
            footer_text,
            box=ROUNDED,
            style="yellow"
        )
    
    def _render(self) -> Layout:
        """Render the complete layout"""
        self.layout["header"].update(self._create_header())
        self.layout["agents"].update(self._create_agent_panel())
        self.layout["messages"].update(self._create_message_panel())
        self.layout["footer"].update(self._create_footer())
        return self.layout
    
    def add_event(self, event: AgentEvent):
        """Add an event to the message buffer"""
        self.message_buffer.append(event)
    
    async def start(self):
        """Start the live display"""
        self.running = True
        self.live = Live(
            self._render(),
            console=self.console,
            refresh_per_second=4,
            screen=True
        )
        
        # Register callback with event tracker
        self.event_tracker.register_callback(self.add_event)
        
        self.live.start()
    
    def stop(self):
        """Stop the live display"""
        self.running = False
        if self.live:
            self.live.stop()
    
    def update(self):
        """Update the display (for manual refresh)"""
        if self.live:
            self.live.update(self._render())
    
    def print_banner(self, text: str, style: str = "bold cyan"):
        """Print a banner message"""
        self.console.print()
        self.console.rule(f"[{style}]{text}[/{style}]")
        self.console.print()
    
    def print_section(self, title: str, items: List[str], style: str = "cyan"):
        """Print a section with items"""
        self.console.print(f"[bold {style}]{title}[/bold {style}]")
        for item in items:
            self.console.print(f"  {item}")
        self.console.print()
    
    def print_patient_details(self, patient_data: Dict[str, Any]):
        """Print patient details in a formatted way"""
        table = Table(show_header=False, box=ROUNDED, padding=(0, 1))
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Patient ID", patient_data.get("patient_id", "N/A"))
        table.add_row("Priority", f"{patient_data.get('priority', 'N/A')} (CRITICAL)" if patient_data.get('priority') == 1 else str(patient_data.get('priority', 'N/A')))
        table.add_row("Chief Complaint", patient_data.get("chief_complaint", "N/A"))
        
        if "vitals" in patient_data:
            vitals = patient_data["vitals"]
            table.add_row("Heart Rate", f"{vitals.get('hr', 'N/A')} bpm")
            table.add_row("Blood Pressure", f"{vitals.get('bp_sys', 'N/A')}/{vitals.get('bp_dia', 'N/A')} mmHg")
            table.add_row("SpO2", f"{vitals.get('spo2', 'N/A')}%")
        
        self.console.print(Panel(table, title="[bold cyan]📋 Patient Details[/bold cyan]", border_style="cyan"))
        self.console.print()
    
    def print_protocol_info(self, protocol: str):
        """Print protocol activation information"""
        protocol_info = {
            "stemi": {
                "name": "STEMI (Heart Attack)",
                "target": "<5 minutes activation",
                "steps": [
                    "1. ECG acquisition and interpretation → 1 min",
                    "2. STEMI confirmation → 30 sec",
                    "3. Cath lab activation → 1 min",
                    "4. Team assembly → 1 min 30 sec",
                    "5. Resource allocation → 1 min"
                ]
            },
            "stroke": {
                "name": "Stroke Protocol",
                "target": "<7 minutes activation",
                "steps": [
                    "1. NIHSS assessment → 2 min",
                    "2. CT scan order → 1 min",
                    "3. Stroke team activation → 2 min",
                    "4. tPA preparation → 1 min 30 sec"
                ]
            },
            "trauma": {
                "name": "Trauma Protocol",
                "target": "<3 minutes bay ready",
                "steps": [
                    "1. Pre-arrival notification → 30 sec",
                    "2. Trauma bay preparation → 1 min",
                    "3. Team activation → 1 min",
                    "4. Blood products ready → 30 sec"
                ]
            }
        }
        
        info = protocol_info.get(protocol.lower(), {
            "name": protocol.upper(),
            "target": "Unknown",
            "steps": []
        })
        
        self.console.print(f"[bold red]🚨 {info['name']} Protocol Activated[/bold red]")
        self.console.print(f"[yellow]Target: {info['target']}[/yellow]\n")
        
        if info["steps"]:
            self.console.print("[bold]Expected Workflow:[/bold]")
            for step in info["steps"]:
                self.console.print(f"  {step}")
        self.console.print()