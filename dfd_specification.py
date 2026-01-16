# dfd_specification.py
# Formal specification of DFD components for Lush Fresh RMS

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class ProcessLevel(Enum):
    CONTEXT = 0
    LEVEL_1 = 1
    LEVEL_2 = 2

@dataclass
class RMSDataStore:
    """Data store specification for Lush Fresh RMS."""
    id: str
    name: str
    description: str
    primary_data_elements: List[str]
    owning_department: str
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "data_elements": self.primary_data_elements,
            "owner": self.owning_department
        }

# Define all data stores for Level 1 DFD
RMS_DATA_STORES = [
    RMSDataStore(
        id="D1",
        name="Customer Data",
        description="Customer profiles, contact information, order history",
        primary_data_elements=["customer_id", "name", "address", "payment_method", "order_history"],
        owning_department="Sales"
    ),
    RMSDataStore(
        id="D2",
        name="Product Data",
        description="Product catalogue with inventory levels and pricing",
        primary_data_elements=["product_id", "name", "price", "stock_level", "reorder_point"],
        owning_department="Operations"
    ),
    RMSDataStore(
        id="D3",
        name="Order Data",
        description="Customer order records with status tracking",
        primary_data_elements=["order_id", "customer_id", "items", "status", "timestamps"],
        owning_department="Sales"
    ),
    RMSDataStore(
        id="D4",
        name="Invoice Data",
        description="Billing records for customers and payment status",
        primary_data_elements=["invoice_id", "order_id", "amount", "payment_status", "due_date"],
        owning_department="Finance"
    ),
    RMSDataStore(
        id="D5",
        name="Supplier Data",
        description="Vendor profiles, contracts, and performance metrics",
        primary_data_elements=["supplier_id", "name", "contact", "rating", "contract_terms"],
        owning_department="Procurement"
    ),
    RMSDataStore(
        id="D6",
        name="Purchase Order Data",
        description="Procurement orders with approval status",
        primary_data_elements=["po_id", "supplier_id", "items", "status", "approval_chain"],
        owning_department="Procurement"
    ),
    RMSDataStore(
        id="D7",
        name="Goods Receipt Data",
        description="Delivery records with quality and quantity verification",
        primary_data_elements=["gr_id", "po_id", "received_items", "discrepancies", "timestamp"],
        owning_department="Warehouse"
    ),
    RMSDataStore(
        id="D8",
        name="Financial Account Data",
        description="Accounts payable and receivable ledgers",
        primary_data_elements=["account_id", "type", "balance", "transactions", "reconciliation_status"],
        owning_department="Finance"
    ),
    RMSDataStore(
        id="D9",
        name="Management Report Data",
        description="Aggregated metrics and KPI snapshots",
        primary_data_elements=["report_id", "report_type", "period", "metrics", "generated_timestamp"],
        owning_department="Executive"
    )
]

@dataclass
class RMSProcess:
    """Process specification for Lush Fresh RMS."""
    id: str
    name: str
    level: ProcessLevel
    parent_id: Optional[str]
    description: str
    inputs: List[str]
    outputs: List[str]
    data_stores_read: List[str]
    data_stores_write: List[str]
    
    def validate_data_store_access(self, valid_stores: List[str]) -> bool:
        """Verify all referenced data stores exist."""
        all_stores = set(self.data_stores_read + self.data_stores_write)
        return all_stores.issubset(set(valid_stores))
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level.name,
            "parent": self.parent_id,
            "description": self.description,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "reads": self.data_stores_read,
            "writes": self.data_stores_write
        }

# Define Level 1 processes
LEVEL_1_PROCESSES = [
    RMSProcess(
        id="1.0",
        name="Process Customer Order & Invoice",
        level=ProcessLevel.LEVEL_1,
        parent_id="0.0",
        description="Handle customer orders from receipt through invoicing",
        inputs=["Order Details", "Customer Payment"],
        outputs=["Order Confirmation", "Invoice", "Fulfilment Request"],
        data_stores_read=["D1", "D2"],
        data_stores_write=["D1", "D3", "D4"]
    ),
    RMSProcess(
        id="2.0",
        name="Manage Fulfilment & Inventory",
        level=ProcessLevel.LEVEL_1,
        parent_id="0.0",
        description="Coordinate warehouse operations and inventory management",
        inputs=["Fulfilment Request", "Product Data"],
        outputs=["Delivery Data", "Stock Requirements"],
        data_stores_read=["D2", "D3"],
        data_stores_write=["D2", "D3"]
    ),
    RMSProcess(
        id="3.0",
        name="Manage Procurement",
        level=ProcessLevel.LEVEL_1,
        parent_id="0.0",
        description="Generate and process purchase requisitions and orders",
        inputs=["Stock Requirements", "Supplier Data"],
        outputs=["Purchase Order"],
        data_stores_read=["D2", "D5"],
        data_stores_write=["D6"]
    ),
    RMSProcess(
        id="4.0",
        name="Process Goods Receipt",
        level=ProcessLevel.LEVEL_1,
        parent_id="0.0",
        description="Receive and verify supplier deliveries",
        inputs=["Delivery Data", "Purchase Order Data"],
        outputs=["Goods Receipt Record", "Supplier Performance Report"],
        data_stores_read=["D6"],
        data_stores_write=["D2", "D7"]
    ),
    RMSProcess(
        id="5.0",
        name="Manage Accounts & Payments",
        level=ProcessLevel.LEVEL_1,
        parent_id="0.0",
        description="Handle financial transactions and reconciliation",
        inputs=["Invoice Data", "Goods Receipt Data", "Payment Confirmation"],
        outputs=["Payment Instruction", "Account Status Update"],
        data_stores_read=["D4", "D6", "D7"],
        data_stores_write=["D4", "D8"]
    ),
    RMSProcess(
        id="6.0",
        name="Generate Management Reports",
        level=ProcessLevel.LEVEL_1,
        parent_id="0.0",
        description="Produce operational and financial analytics",
        inputs=["Financial Data", "Operational Data"],
        outputs=["Management Report"],
        data_stores_read=["D3", "D4", "D8"],
        data_stores_write=["D9"]
    )
]

# Define Level 2 decomposition of Process 1.0
PROCESS_1_DECOMPOSITION = [
    RMSProcess(
        id="1.1",
        name="Capture Order Request",
        level=ProcessLevel.LEVEL_2,
        parent_id="1.0",
        description="Receive and parse customer order with payment information",
        inputs=["Customer Order Input"],
        outputs=["Parsed Order Request"],
        data_stores_read=["D1"],
        data_stores_write=["D1", "D3"]
    ),
    RMSProcess(
        id="1.2",
        name="Check Customer & Stock Availability",
        level=ProcessLevel.LEVEL_2,
        parent_id="1.0",
        description="Validate customer status and verify product availability",
        inputs=["Parsed Order Request"],
        outputs=["Validated Order"],
        data_stores_read=["D1", "D2"],
        data_stores_write=[]
    ),
    RMSProcess(
        id="1.3",
        name="Execute Payment Transaction",
        level=ProcessLevel.LEVEL_2,
        parent_id="1.0",
        description="Process payment via direct or BNPL channels",
        inputs=["Validated Order"],
        outputs=["Payment Success Notice", "BNPL Activation"],
        data_stores_read=["D1", "D3"],
        data_stores_write=["D3"]
    ),
    RMSProcess(
        id="1.4",
        name="Generate Invoice Document",
        level=ProcessLevel.LEVEL_2,
        parent_id="1.0",
        description="Create billing record with itemised charges",
        inputs=["Payment Success Notice"],
        outputs=["Invoice Output"],
        data_stores_read=["D3"],
        data_stores_write=["D4"]
    ),
    RMSProcess(
        id="1.5",
        name="Final Order Confirmation",
        level=ProcessLevel.LEVEL_2,
        parent_id="1.0",
        description="Compile and send confirmation to customer",
        inputs=["Invoice Output"],
        outputs=["Order Confirmation", "Delivery Estimate"],
        data_stores_read=["D3", "D4"],
        data_stores_write=["D3"]
    ),
    RMSProcess(
        id="1.6",
        name="Create Fulfilment Request",
        level=ProcessLevel.LEVEL_2,
        parent_id="1.0",
        description="Generate pick list and dispatch instructions",
        inputs=["Order Confirmation"],
        outputs=["Fulfilment Request", "Pick List"],
        data_stores_read=["D2", "D3"],
        data_stores_write=["D3"]
    )
]

# Define Level 2 decomposition of Process 5.0
PROCESS_5_DECOMPOSITION = [
    RMSProcess(
        id="5.1",
        name="Retrieve Financial Documents",
        level=ProcessLevel.LEVEL_2,
        parent_id="5.0",
        description="Fetch invoice, PO, and GR records for matching",
        inputs=["Document Request"],
        outputs=["Combined Financial Docs"],
        data_stores_read=["D4", "D6", "D7"],
        data_stores_write=[]
    ),
    RMSProcess(
        id="5.2",
        name="Perform 3-Way Match",
        level=ProcessLevel.LEVEL_2,
        parent_id="5.0",
        description="Compare PO, GR, and invoice for discrepancies",
        inputs=["Combined Financial Docs"],
        outputs=["Match Result"],
        data_stores_read=[],
        data_stores_write=[]
    ),
    RMSProcess(
        id="5.3",
        name="Flag Discrepancies",
        level=ProcessLevel.LEVEL_2,
        parent_id="5.0",
        description="Document mismatches and notify relevant parties",
        inputs=["Match Result"],
        outputs=["Discrepancy Log"],
        data_stores_read=[],
        data_stores_write=["D8", "D9"]
    ),
    RMSProcess(
        id="5.4",
        name="Approve Validated Invoices",
        level=ProcessLevel.LEVEL_2,
        parent_id="5.0",
        description="Management review and authorisation",
        inputs=["Validated Invoice"],
        outputs=["Approval Record"],
        data_stores_read=["D4"],
        data_stores_write=["D4", "D8"]
    ),
    RMSProcess(
        id="5.5",
        name="Update Financial Accounts",
        level=ProcessLevel.LEVEL_2,
        parent_id="5.0",
        description="Post approved transactions to ledgers",
        inputs=["Approval Record"],
        outputs=["Reconciliation Data"],
        data_stores_read=["D8"],
        data_stores_write=["D8"]
    ),
    RMSProcess(
        id="5.6",
        name="Issue Payment Instruction",
        level=ProcessLevel.LEVEL_2,
        parent_id="5.0",
        description="Generate and transmit payment to bank",
        inputs=["Payment Data"],
        outputs=["Payment Instruction", "Payment Confirmation"],
        data_stores_read=["D8"],
        data_stores_write=["D8"]
    )
]


@dataclass
class ExternalEntity:
    """External entity specification for context diagram."""
    id: str
    name: str
    entity_type: str  # customer, supplier, partner, regulator
    inbound_flows: List[str]
    outbound_flows: List[str]
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.entity_type,
            "receives": self.outbound_flows,
            "sends": self.inbound_flows
        }

# Context diagram external entities
EXTERNAL_ENTITIES = [
    ExternalEntity(
        id="E1",
        name="Customer",
        entity_type="customer",
        inbound_flows=["Order Details", "Online Payment"],
        outbound_flows=["Order Confirmation", "Invoice", "Delivery Details"]
    ),
    ExternalEntity(
        id="E2",
        name="Supplier",
        entity_type="supplier",
        inbound_flows=["Delivery Notification", "Supplier Invoice"],
        outbound_flows=["Purchase Order", "Payment Confirmation"]
    ),
    ExternalEntity(
        id="E3",
        name="Bank",
        entity_type="partner",
        inbound_flows=["Payment Confirmation", "Bank Statement"],
        outbound_flows=["Payment Instruction", "Customer Payment Request"]
    ),
    ExternalEntity(
        id="E4",
        name="Warehouse Staff",
        entity_type="internal",
        inbound_flows=["Goods Receipt Confirmation", "Shipping Confirmation"],
        outbound_flows=["Pick List", "Shipping Instructions"]
    )
]


def generate_dfd_specification_report() -> str:
    """Generate comprehensive DFD specification document."""
    report = []
    report.append("=" * 70)
    report.append("LUSH FRESH RMS - DATA FLOW DIAGRAM SPECIFICATION")
    report.append("=" * 70)
    
    report.append("\n\nEXTERNAL ENTITIES")
    report.append("-" * 40)
    for entity in EXTERNAL_ENTITIES:
        report.append(f"\n{entity.id}: {entity.name} ({entity.entity_type})")
        report.append(f"  Sends to system: {', '.join(entity.inbound_flows)}")
        report.append(f"  Receives from system: {', '.join(entity.outbound_flows)}")
    
    report.append("\n\nDATA STORES")
    report.append("-" * 40)
    for store in RMS_DATA_STORES:
        report.append(f"\n{store.id}: {store.name}")
        report.append(f"  Owner: {store.owning_department}")
        report.append(f"  Description: {store.description}")
        report.append(f"  Key Elements: {', '.join(store.primary_data_elements)}")
    
    report.append("\n\nLEVEL 1 PROCESSES")
    report.append("-" * 40)
    for process in LEVEL_1_PROCESSES:
        report.append(f"\n{process.id}: {process.name}")
        report.append(f"  Description: {process.description}")
        report.append(f"  Inputs: {', '.join(process.inputs)}")
        report.append(f"  Outputs: {', '.join(process.outputs)}")
        report.append(f"  Reads from: {', '.join(process.data_stores_read)}")
        report.append(f"  Writes to: {', '.join(process.data_stores_write)}")
    
    report.append("\n\nPROCESS 1.0 DECOMPOSITION (LEVEL 2)")
    report.append("-" * 40)
    for process in PROCESS_1_DECOMPOSITION:
        report.append(f"\n{process.id}: {process.name}")
        report.append(f"  Description: {process.description}")
        report.append(f"  Inputs: {', '.join(process.inputs)}")
        report.append(f"  Outputs: {', '.join(process.outputs)}")
        if process.data_stores_read:
            report.append(f"  Reads from: {', '.join(process.data_stores_read)}")
        if process.data_stores_write:
            report.append(f"  Writes to: {', '.join(process.data_stores_write)}")
    
    report.append("\n\nPROCESS 5.0 DECOMPOSITION (LEVEL 2)")
    report.append("-" * 40)
    for process in PROCESS_5_DECOMPOSITION:
        report.append(f"\n{process.id}: {process.name}")
        report.append(f"  Description: {process.description}")
        report.append(f"  Inputs: {', '.join(process.inputs)}")
        report.append(f"  Outputs: {', '.join(process.outputs)}")
        if process.data_stores_read:
            report.append(f"  Reads from: {', '.join(process.data_stores_read)}")
        if process.data_stores_write:
            report.append(f"  Writes to: {', '.join(process.data_stores_write)}")
    
    report.append("\n\n" + "=" * 70)
    
    return "\n".join(report)


def validate_dfd_completeness() -> Dict[str, bool]:
    """Validate DFD specification completeness."""
    results = {}
    
    # Check all Level 1 processes reference valid data stores
    valid_store_ids = [s.id for s in RMS_DATA_STORES]
    
    for process in LEVEL_1_PROCESSES:
        results[f"{process.id}_store_refs"] = process.validate_data_store_access(valid_store_ids)
    
    # Check decomposition coverage
    level_2_parent_ids = set(p.parent_id for p in PROCESS_1_DECOMPOSITION + PROCESS_5_DECOMPOSITION)
    decomposed_processes = {"1.0", "5.0"}
    results["decomposition_coverage"] = level_2_parent_ids == decomposed_processes
    
    # Check external entity flow balance
    all_inbound = []
    all_outbound = []
    for entity in EXTERNAL_ENTITIES:
        all_inbound.extend(entity.inbound_flows)
        all_outbound.extend(entity.outbound_flows)
    results["entity_flows_defined"] = len(all_inbound) > 0 and len(all_outbound) > 0
    
    return results


if __name__ == "__main__":
    print(generate_dfd_specification_report())
    print("\n\nVALIDATION RESULTS:")
    print("-" * 40)
    for check, result in validate_dfd_completeness().items():
        status = "PASS" if result else "FAIL"
        print(f"  {check}: {status}")
