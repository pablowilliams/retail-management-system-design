# integration_architecture.py
# Integration specifications for Lush Fresh RMS

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class IntegrationType(Enum):
    REST_API = "rest_api"
    SFTP = "sftp"
    EMAIL = "email"
    WEBHOOK = "webhook"
    HARDWARE = "hardware_interface"
    EDI = "edi"

class DataFormat(Enum):
    JSON = "json"
    XML = "xml"
    CSV = "csv"
    PDF = "pdf"
    BINARY = "binary"

@dataclass
class IntegrationEndpoint:
    """Specification for external system integration point."""
    name: str
    external_system: str
    integration_type: IntegrationType
    data_format: DataFormat
    direction: str  # inbound, outbound, bidirectional
    frequency: str  # real-time, batch, event-driven
    security_requirements: List[str]
    data_elements: List[str]
    error_handling: str
    
    def generate_interface_spec(self) -> Dict:
        return {
            "endpoint": self.name,
            "system": self.external_system,
            "type": self.integration_type.value,
            "format": self.data_format.value,
            "direction": self.direction,
            "frequency": self.frequency,
            "security": self.security_requirements,
            "payload": self.data_elements,
            "error_handling": self.error_handling
        }

# Define integration endpoints
RMS_INTEGRATIONS = [
    IntegrationEndpoint(
        name="Customer Order Submission",
        external_system="Lush Fresh Website",
        integration_type=IntegrationType.REST_API,
        data_format=DataFormat.JSON,
        direction="inbound",
        frequency="real-time",
        security_requirements=["TLS 1.3", "API Key Authentication", "Rate Limiting"],
        data_elements=["customer_id", "order_items", "delivery_address", "payment_token"],
        error_handling="Synchronous error response with retry guidance"
    ),
    IntegrationEndpoint(
        name="Order Status Updates",
        external_system="Lush Fresh Website",
        integration_type=IntegrationType.WEBHOOK,
        data_format=DataFormat.JSON,
        direction="outbound",
        frequency="event-driven",
        security_requirements=["TLS 1.3", "Webhook Signature Verification"],
        data_elements=["order_id", "status", "timestamp", "details"],
        error_handling="Exponential backoff retry with dead letter queue"
    ),
    IntegrationEndpoint(
        name="Payment Authorisation",
        external_system="Bank Payment Gateway",
        integration_type=IntegrationType.REST_API,
        data_format=DataFormat.JSON,
        direction="bidirectional",
        frequency="real-time",
        security_requirements=["PCI-DSS Compliance", "TLS 1.3", "Tokenisation"],
        data_elements=["payment_token", "amount", "currency", "merchant_reference"],
        error_handling="Timeout handling with idempotency keys"
    ),
    IntegrationEndpoint(
        name="Batch Payment Processing",
        external_system="Bank",
        integration_type=IntegrationType.SFTP,
        data_format=DataFormat.CSV,
        direction="outbound",
        frequency="batch",
        security_requirements=["SSH Key Authentication", "File Encryption"],
        data_elements=["payment_id", "beneficiary", "amount", "reference"],
        error_handling="Reconciliation file processing with exception reporting"
    ),
    IntegrationEndpoint(
        name="Purchase Order Transmission",
        external_system="Suppliers",
        integration_type=IntegrationType.EMAIL,
        data_format=DataFormat.PDF,
        direction="outbound",
        frequency="event-driven",
        security_requirements=["TLS Email", "Digital Signature"],
        data_elements=["po_number", "line_items", "delivery_date", "terms"],
        error_handling="Delivery confirmation tracking with escalation"
    ),
    IntegrationEndpoint(
        name="Barcode Scanner Events",
        external_system="Warehouse Hardware",
        integration_type=IntegrationType.HARDWARE,
        data_format=DataFormat.BINARY,
        direction="inbound",
        frequency="real-time",
        security_requirements=["Network Segmentation", "Device Authentication"],
        data_elements=["barcode_data", "scanner_id", "timestamp", "location"],
        error_handling="Local buffering with sync on reconnection"
    ),
    IntegrationEndpoint(
        name="Supplier Invoice Receipt",
        external_system="Supplier Portal",
        integration_type=IntegrationType.EMAIL,
        data_format=DataFormat.PDF,
        direction="inbound",
        frequency="event-driven",
        security_requirements=["Sender Verification", "Attachment Scanning"],
        data_elements=["invoice_number", "po_reference", "line_items", "total"],
        error_handling="OCR parsing with manual review queue for failures"
    ),
    IntegrationEndpoint(
        name="Bank Statement Import",
        external_system="Bank",
        integration_type=IntegrationType.SFTP,
        data_format=DataFormat.CSV,
        direction="inbound",
        frequency="batch",
        security_requirements=["SSH Key Authentication", "IP Whitelisting"],
        data_elements=["transaction_id", "date", "amount", "reference", "balance"],
        error_handling="Automated reconciliation with exception flagging"
    )
]


def generate_integration_matrix() -> str:
    """Generate integration architecture summary."""
    lines = []
    lines.append("=" * 80)
    lines.append("LUSH FRESH RMS - INTEGRATION ARCHITECTURE MATRIX")
    lines.append("=" * 80)
    
    for endpoint in RMS_INTEGRATIONS:
        lines.append(f"\n{endpoint.name}")
        lines.append("-" * len(endpoint.name))
        lines.append(f"External System: {endpoint.external_system}")
        lines.append(f"Type: {endpoint.integration_type.value}")
        lines.append(f"Format: {endpoint.data_format.value}")
        lines.append(f"Direction: {endpoint.direction}")
        lines.append(f"Frequency: {endpoint.frequency}")
        lines.append(f"Security: {', '.join(endpoint.security_requirements)}")
        lines.append(f"Data Elements: {', '.join(endpoint.data_elements)}")
        lines.append(f"Error Handling: {endpoint.error_handling}")
    
    lines.append("\n" + "=" * 80)
    return "\n".join(lines)


def generate_security_summary() -> str:
    """Generate security requirements summary across all integrations."""
    lines = []
    lines.append("=" * 60)
    lines.append("SECURITY REQUIREMENTS SUMMARY")
    lines.append("=" * 60)
    
    all_requirements = set()
    for endpoint in RMS_INTEGRATIONS:
        all_requirements.update(endpoint.security_requirements)
    
    lines.append("\nUnique Security Requirements:")
    for req in sorted(all_requirements):
        endpoints = [e.name for e in RMS_INTEGRATIONS if req in e.security_requirements]
        lines.append(f"\n  {req}")
        lines.append(f"    Applied to: {', '.join(endpoints)}")
    
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


if __name__ == "__main__":
    print(generate_integration_matrix())
    print("\n")
    print(generate_security_summary())
