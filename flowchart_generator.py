# flowchart_generator.py
# System flowchart specification and validation module for Lush Fresh RMS

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum
import json

class FlowchartSymbol(Enum):
    """Standard flowchart symbol types."""
    TERMINATOR = "oval"           # Start/End
    PROCESS = "rectangle"          # System/User task
    MANUAL_PROCESS = "wavy_rect"   # Human-performed task
    DECISION = "diamond"           # Yes/No branch
    DOCUMENT = "document"          # Paper document
    DATA = "parallelogram"         # Data input/output
    DATABASE = "cylinder"          # Data storage/archive
    NOTE = "slanted_rect"          # Alert/log/warning
    CONNECTOR = "circle"           # Flow connector

class FlowDirection(Enum):
    """Flow arrow types."""
    NORMAL = "solid"
    EXCEPTION = "dashed"
    CONDITIONAL = "dotted"

@dataclass
class FlowchartNode:
    """Individual node in a system flowchart."""
    node_id: str
    symbol: FlowchartSymbol
    label: str
    swimlane: str
    description: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.node_id,
            "symbol": self.symbol.value,
            "label": self.label,
            "lane": self.swimlane,
            "description": self.description
        }

@dataclass
class FlowchartEdge:
    """Connection between flowchart nodes."""
    source_id: str
    target_id: str
    direction: FlowDirection
    label: str = ""
    condition: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "from": self.source_id,
            "to": self.target_id,
            "type": self.direction.value,
            "label": self.label,
            "condition": self.condition
        }

@dataclass
class Swimlane:
    """Swimlane definition for process ownership."""
    lane_id: str
    name: str
    actor_type: str  # system, human, external
    order: int
    
class SystemFlowchart:
    """
    Complete system flowchart specification with validation.
    Supports swimlane organisation, decision branching, and exception paths.
    """
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.swimlanes: Dict[str, Swimlane] = {}
        self.nodes: Dict[str, FlowchartNode] = {}
        self.edges: List[FlowchartEdge] = []
        self.validation_errors: List[str] = []
    
    def add_swimlane(self, lane: Swimlane) -> None:
        """Add swimlane to flowchart."""
        self.swimlanes[lane.lane_id] = lane
    
    def add_node(self, node: FlowchartNode) -> bool:
        """Add node with swimlane validation."""
        if node.swimlane not in self.swimlanes:
            self.validation_errors.append(
                f"Node '{node.node_id}' references undefined swimlane '{node.swimlane}'"
            )
            return False
        self.nodes[node.node_id] = node
        return True
    
    def add_edge(self, edge: FlowchartEdge) -> bool:
        """Add edge with node validation."""
        if edge.source_id not in self.nodes:
            self.validation_errors.append(
                f"Edge source '{edge.source_id}' not found"
            )
            return False
        if edge.target_id not in self.nodes:
            self.validation_errors.append(
                f"Edge target '{edge.target_id}' not found"
            )
            return False
        self.edges.append(edge)
        return True
    
    def validate_single_start_end(self) -> bool:
        """Ensure exactly one start and at least one end terminator."""
        terminators = [
            n for n in self.nodes.values() 
            if n.symbol == FlowchartSymbol.TERMINATOR
        ]
        
        start_nodes = [n for n in terminators if "start" in n.label.lower()]
        end_nodes = [n for n in terminators if "end" in n.label.lower()]
        
        if len(start_nodes) != 1:
            self.validation_errors.append(
                f"Expected 1 start node, found {len(start_nodes)}"
            )
            return False
        
        if len(end_nodes) < 1:
            self.validation_errors.append("No end nodes found")
            return False
        
        return True
    
    def validate_decision_branches(self) -> bool:
        """Ensure all decision nodes have exactly two outgoing edges."""
        valid = True
        
        for node_id, node in self.nodes.items():
            if node.symbol == FlowchartSymbol.DECISION:
                outgoing = [e for e in self.edges if e.source_id == node_id]
                if len(outgoing) != 2:
                    self.validation_errors.append(
                        f"Decision node '{node_id}' has {len(outgoing)} branches, expected 2"
                    )
                    valid = False
        
        return valid
    
    def validate_connectivity(self) -> bool:
        """Ensure all non-terminator nodes are reachable and have exits."""
        valid = True
        
        # Find start node
        start_node = next(
            (n for n in self.nodes.values() 
             if n.symbol == FlowchartSymbol.TERMINATOR and "start" in n.label.lower()),
            None
        )
        
        if not start_node:
            return False
        
        # BFS to find reachable nodes
        reachable: Set[str] = set()
        queue = [start_node.node_id]
        
        while queue:
            current = queue.pop(0)
            if current in reachable:
                continue
            reachable.add(current)
            
            for edge in self.edges:
                if edge.source_id == current and edge.target_id not in reachable:
                    queue.append(edge.target_id)
        
        # Check for unreachable nodes
        for node_id in self.nodes:
            if node_id not in reachable:
                self.validation_errors.append(
                    f"Node '{node_id}' is unreachable from start"
                )
                valid = False
        
        return valid
    
    def run_all_validations(self) -> Tuple[bool, List[str]]:
        """Execute all flowchart validations."""
        self.validation_errors = []
        
        checks = [
            self.validate_single_start_end,
            self.validate_decision_branches,
            self.validate_connectivity
        ]
        
        all_valid = all(check() for check in checks)
        return all_valid, self.validation_errors
    
    def export_specification(self) -> Dict:
        """Export complete flowchart specification as dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "swimlanes": [lane.__dict__ for lane in self.swimlanes.values()],
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "edges": [edge.to_dict() for edge in self.edges]
        }
    
    def generate_text_representation(self) -> str:
        """Generate ASCII text representation of flowchart structure."""
        lines = []
        lines.append("=" * 70)
        lines.append(f"FLOWCHART: {self.name}")
        lines.append("=" * 70)
        lines.append(f"\nDescription: {self.description}")
        
        lines.append("\n\nSWIMLANES:")
        lines.append("-" * 40)
        for lane in sorted(self.swimlanes.values(), key=lambda l: l.order):
            lines.append(f"  [{lane.order}] {lane.name} ({lane.actor_type})")
        
        lines.append("\n\nNODES BY SWIMLANE:")
        lines.append("-" * 40)
        for lane_id, lane in self.swimlanes.items():
            lane_nodes = [n for n in self.nodes.values() if n.swimlane == lane_id]
            if lane_nodes:
                lines.append(f"\n{lane.name}:")
                for node in lane_nodes:
                    symbol_icon = {
                        FlowchartSymbol.TERMINATOR: "(O)",
                        FlowchartSymbol.PROCESS: "[P]",
                        FlowchartSymbol.MANUAL_PROCESS: "[M]",
                        FlowchartSymbol.DECISION: "<D>",
                        FlowchartSymbol.DATABASE: "{=}",
                        FlowchartSymbol.DOCUMENT: "[/]",
                    }.get(node.symbol, "[?]")
                    lines.append(f"    {symbol_icon} {node.node_id}: {node.label}")
        
        lines.append("\n\nFLOW EDGES:")
        lines.append("-" * 40)
        for edge in self.edges:
            arrow = "-->" if edge.direction == FlowDirection.NORMAL else "..>"
            label = f" [{edge.label}]" if edge.label else ""
            lines.append(f"  {edge.source_id} {arrow} {edge.target_id}{label}")
        
        lines.append("\n" + "=" * 70)
        return "\n".join(lines)


def create_customer_order_flowchart() -> SystemFlowchart:
    """
    Create complete Customer Order Lifecycle flowchart specification.
    """
    flowchart = SystemFlowchart(
        name="Customer Order Lifecycle",
        description="End-to-end order processing from placement through delivery and payment"
    )
    
    # Define swimlanes
    swimlanes = [
        Swimlane("CUST", "Customer", "external", 1),
        Swimlane("WEB", "Lush Website", "system", 2),
        Swimlane("OMS", "Order Management System", "system", 3),
        Swimlane("FUL", "Fulfilment System", "system", 4),
        Swimlane("INV", "Invoicing System", "system", 5),
        Swimlane("AR", "Accounts Receivable", "human", 6),
        Swimlane("BNPL", "BNPL Collection", "human", 7),
    ]
    
    for lane in swimlanes:
        flowchart.add_swimlane(lane)
    
    # Define nodes
    nodes = [
        FlowchartNode("START", FlowchartSymbol.TERMINATOR, "Start", "CUST"),
        FlowchartNode("C1", FlowchartSymbol.PROCESS, "Place Order", "CUST"),
        FlowchartNode("W1", FlowchartSymbol.PROCESS, "Receive Order", "WEB"),
        FlowchartNode("W2", FlowchartSymbol.PROCESS, "Send to OMS", "WEB"),
        FlowchartNode("O1", FlowchartSymbol.PROCESS, "Validate Order", "OMS"),
        FlowchartNode("O2", FlowchartSymbol.DECISION, "Stock & Payment OK?", "OMS"),
        FlowchartNode("O3", FlowchartSymbol.PROCESS, "Flag Issue", "OMS"),
        FlowchartNode("O4", FlowchartSymbol.MANUAL_PROCESS, "Manual Resolution", "OMS"),
        FlowchartNode("O5", FlowchartSymbol.PROCESS, "Process Payment", "OMS"),
        FlowchartNode("O6", FlowchartSymbol.DECISION, "Payment Accepted?", "OMS"),
        FlowchartNode("O7", FlowchartSymbol.PROCESS, "Notify Failure", "OMS"),
        FlowchartNode("O8", FlowchartSymbol.PROCESS, "Confirm Order", "OMS"),
        FlowchartNode("F1", FlowchartSymbol.MANUAL_PROCESS, "Pick & Pack", "FUL"),
        FlowchartNode("F2", FlowchartSymbol.DECISION, "Damage Detected?", "FUL"),
        FlowchartNode("F3", FlowchartSymbol.PROCESS, "Log & Replace", "FUL"),
        FlowchartNode("F4", FlowchartSymbol.PROCESS, "Schedule Courier", "FUL"),
        FlowchartNode("I1", FlowchartSymbol.PROCESS, "Generate Invoice", "INV"),
        FlowchartNode("I2", FlowchartSymbol.PROCESS, "Email to Customer", "INV"),
        FlowchartNode("I3", FlowchartSymbol.PROCESS, "Send to AR", "INV"),
        FlowchartNode("A1", FlowchartSymbol.PROCESS, "Receive Invoice", "AR"),
        FlowchartNode("A2", FlowchartSymbol.DECISION, "BNPL Used?", "AR"),
        FlowchartNode("A3", FlowchartSymbol.DATABASE, "Archive Transaction", "AR"),
        FlowchartNode("B1", FlowchartSymbol.PROCESS, "Track BNPL Account", "BNPL"),
        FlowchartNode("END1", FlowchartSymbol.TERMINATOR, "End", "AR"),
        FlowchartNode("END2", FlowchartSymbol.TERMINATOR, "End (Failure)", "CUST"),
    ]
    
    for node in nodes:
        flowchart.add_node(node)
    
    # Define edges
    edges = [
        FlowchartEdge("START", "C1", FlowDirection.NORMAL),
        FlowchartEdge("C1", "W1", FlowDirection.NORMAL),
        FlowchartEdge("W1", "W2", FlowDirection.NORMAL),
        FlowchartEdge("W2", "O1", FlowDirection.NORMAL),
        FlowchartEdge("O1", "O2", FlowDirection.NORMAL),
        FlowchartEdge("O2", "O5", FlowDirection.NORMAL, "Yes"),
        FlowchartEdge("O2", "O3", FlowDirection.EXCEPTION, "No"),
        FlowchartEdge("O3", "O4", FlowDirection.NORMAL),
        FlowchartEdge("O4", "O1", FlowDirection.EXCEPTION, "Retry"),
        FlowchartEdge("O5", "O6", FlowDirection.NORMAL),
        FlowchartEdge("O6", "O8", FlowDirection.NORMAL, "Yes"),
        FlowchartEdge("O6", "O7", FlowDirection.EXCEPTION, "No"),
        FlowchartEdge("O7", "END2", FlowDirection.NORMAL),
        FlowchartEdge("O8", "F1", FlowDirection.NORMAL),
        FlowchartEdge("F1", "F2", FlowDirection.NORMAL),
        FlowchartEdge("F2", "F4", FlowDirection.NORMAL, "No"),
        FlowchartEdge("F2", "F3", FlowDirection.EXCEPTION, "Yes"),
        FlowchartEdge("F3", "F4", FlowDirection.NORMAL),
        FlowchartEdge("F4", "I1", FlowDirection.NORMAL),
        FlowchartEdge("I1", "I2", FlowDirection.NORMAL),
        FlowchartEdge("I2", "I3", FlowDirection.NORMAL),
        FlowchartEdge("I3", "A1", FlowDirection.NORMAL),
        FlowchartEdge("A1", "A2", FlowDirection.NORMAL),
        FlowchartEdge("A2", "A3", FlowDirection.NORMAL, "No"),
        FlowchartEdge("A2", "B1", FlowDirection.NORMAL, "Yes"),
        FlowchartEdge("B1", "A3", FlowDirection.NORMAL),
        FlowchartEdge("A3", "END1", FlowDirection.NORMAL),
    ]
    
    for edge in edges:
        flowchart.add_edge(edge)
    
    return flowchart


def create_goods_receipt_flowchart() -> SystemFlowchart:
    """
    Create complete Goods Receipt Process flowchart specification.
    """
    flowchart = SystemFlowchart(
        name="Goods Receipt Process",
        description="Supplier delivery processing through three-way matching and payment"
    )
    
    # Define swimlanes
    swimlanes = [
        Swimlane("SUP", "Supplier", "external", 1),
        Swimlane("WH", "Warehouse Staff", "human", 2),
        Swimlane("RMS", "Retail Management System", "system", 3),
        Swimlane("IM", "Inventory Manager", "human", 4),
        Swimlane("FIN", "Accounting & Finance", "human", 5),
        Swimlane("BANK", "Bank", "external", 6),
    ]
    
    for lane in swimlanes:
        flowchart.add_swimlane(lane)
    
    # Define nodes
    nodes = [
        FlowchartNode("START", FlowchartSymbol.TERMINATOR, "Start", "SUP"),
        FlowchartNode("S1", FlowchartSymbol.PROCESS, "Deliver Goods", "SUP"),
        FlowchartNode("W1", FlowchartSymbol.MANUAL_PROCESS, "Scan Barcodes/RFID", "WH"),
        FlowchartNode("R1", FlowchartSymbol.PROCESS, "Receive Scan Data", "RMS"),
        FlowchartNode("R2", FlowchartSymbol.PROCESS, "Match with PO", "RMS"),
        FlowchartNode("R3", FlowchartSymbol.DECISION, "PO Match?", "RMS"),
        FlowchartNode("R4", FlowchartSymbol.NOTE, "Log Discrepancy", "RMS"),
        FlowchartNode("R5", FlowchartSymbol.PROCESS, "Create GR Record", "RMS"),
        FlowchartNode("R6", FlowchartSymbol.PROCESS, "Update Inventory", "RMS"),
        FlowchartNode("I1", FlowchartSymbol.MANUAL_PROCESS, "Review GR", "IM"),
        FlowchartNode("I2", FlowchartSymbol.DECISION, "Approve GR?", "IM"),
        FlowchartNode("R7", FlowchartSymbol.PROCESS, "Receive Vendor Invoice", "RMS"),
        FlowchartNode("F1", FlowchartSymbol.PROCESS, "3-Way Match", "FIN"),
        FlowchartNode("F2", FlowchartSymbol.DECISION, "Match OK?", "FIN"),
        FlowchartNode("F3", FlowchartSymbol.PROCESS, "Approve Invoice", "FIN"),
        FlowchartNode("F4", FlowchartSymbol.NOTE, "Flag for Review", "FIN"),
        FlowchartNode("R8", FlowchartSymbol.PROCESS, "Send Payment Request", "RMS"),
        FlowchartNode("B1", FlowchartSymbol.PROCESS, "Transfer Funds", "BANK"),
        FlowchartNode("R9", FlowchartSymbol.DATABASE, "Archive Records", "RMS"),
        FlowchartNode("END", FlowchartSymbol.TERMINATOR, "End", "RMS"),
    ]
    
    for node in nodes:
        flowchart.add_node(node)
    
    # Define edges
    edges = [
        FlowchartEdge("START", "S1", FlowDirection.NORMAL),
        FlowchartEdge("S1", "W1", FlowDirection.NORMAL),
        FlowchartEdge("W1", "R1", FlowDirection.NORMAL),
        FlowchartEdge("R1", "R2", FlowDirection.NORMAL),
        FlowchartEdge("R2", "R3", FlowDirection.NORMAL),
        FlowchartEdge("R3", "R5", FlowDirection.NORMAL, "Yes"),
        FlowchartEdge("R3", "R4", FlowDirection.EXCEPTION, "No"),
        FlowchartEdge("R4", "R2", FlowDirection.EXCEPTION, "Retry"),
        FlowchartEdge("R5", "R6", FlowDirection.NORMAL),
        FlowchartEdge("R6", "I1", FlowDirection.NORMAL),
        FlowchartEdge("I1", "I2", FlowDirection.NORMAL),
        FlowchartEdge("I2", "R7", FlowDirection.NORMAL, "Yes"),
        FlowchartEdge("I2", "R4", FlowDirection.EXCEPTION, "No"),
        FlowchartEdge("R7", "F1", FlowDirection.NORMAL),
        FlowchartEdge("F1", "F2", FlowDirection.NORMAL),
        FlowchartEdge("F2", "F3", FlowDirection.NORMAL, "Yes"),
        FlowchartEdge("F2", "F4", FlowDirection.EXCEPTION, "No"),
        FlowchartEdge("F4", "F1", FlowDirection.EXCEPTION, "Retry"),
        FlowchartEdge("F3", "R8", FlowDirection.NORMAL),
        FlowchartEdge("R8", "B1", FlowDirection.NORMAL),
        FlowchartEdge("B1", "R9", FlowDirection.NORMAL),
        FlowchartEdge("R9", "END", FlowDirection.NORMAL),
    ]
    
    for edge in edges:
        flowchart.add_edge(edge)
    
    return flowchart


def main():
    """Generate and validate both system flowcharts."""
    
    # Customer Order Lifecycle
    order_flowchart = create_customer_order_flowchart()
    is_valid, errors = order_flowchart.run_all_validations()
    
    print(order_flowchart.generate_text_representation())
    print(f"\nValidation Status: {'PASSED' if is_valid else 'FAILED'}")
    if errors:
        for error in errors:
            print(f"  - {error}")
    
    print("\n" + "=" * 70 + "\n")
    
    # Goods Receipt Process
    gr_flowchart = create_goods_receipt_flowchart()
    is_valid, errors = gr_flowchart.run_all_validations()
    
    print(gr_flowchart.generate_text_representation())
    print(f"\nValidation Status: {'PASSED' if is_valid else 'FAILED'}")
    if errors:
        for error in errors:
            print(f"  - {error}")


if __name__ == "__main__":
    main()
