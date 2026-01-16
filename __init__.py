# MSCI304 Retail Management System Design
# Enterprise system architecture for Lush Fresh grocery delivery

"""
Retail Management System Design Module

This package provides systems analysis tools for designing enterprise
resource planning systems with focus on Order-to-Cash and Procure-to-Pay
cycle automation.

Modules:
    - systems_analysis_framework: DFD validation and process modelling
    - dfd_specification: Formal data flow diagram specifications
    - flowchart_generator: System flowchart creation and validation
    - integration_architecture: External system integration specifications

Example usage:
    from src.dfd_specification import RMS_DATA_STORES, LEVEL_1_PROCESSES
    from src.flowchart_generator import create_customer_order_flowchart
    
    flowchart = create_customer_order_flowchart()
    is_valid, errors = flowchart.run_all_validations()
"""

__version__ = "1.0.0"
__author__ = "MSCI304 Coursework"

from .dfd_specification import (
    RMSDataStore,
    RMSProcess,
    ProcessLevel,
    RMS_DATA_STORES,
    LEVEL_1_PROCESSES,
    PROCESS_1_DECOMPOSITION,
    generate_dfd_specification_report
)

from .flowchart_generator import (
    FlowchartSymbol,
    FlowDirection,
    FlowchartNode,
    FlowchartEdge,
    Swimlane,
    SystemFlowchart,
    create_customer_order_flowchart,
    create_goods_receipt_flowchart
)

__all__ = [
    "RMSDataStore",
    "RMSProcess",
    "ProcessLevel",
    "RMS_DATA_STORES",
    "LEVEL_1_PROCESSES",
    "PROCESS_1_DECOMPOSITION",
    "generate_dfd_specification_report",
    "FlowchartSymbol",
    "FlowDirection",
    "FlowchartNode",
    "FlowchartEdge",
    "Swimlane",
    "SystemFlowchart",
    "create_customer_order_flowchart",
    "create_goods_receipt_flowchart"
]
