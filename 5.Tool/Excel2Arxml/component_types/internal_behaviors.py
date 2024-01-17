# file: internal_behaviors.py
# author: JunhaoBai
# date: 2023/11/24
# last modified: 2023-12-21 20:47:15

from __future__ import annotations
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class DataTypeMappingRef:
    dest: str
    value: str


@dataclass
class DataTypeMappingRefs:
    data_type_mapping_ref: List[DataTypeMappingRef] = None


@dataclass
class TimingEvent:
    UUID: str
    short_name: str
    start_on_event_ref: Optional[str] = None
    dest: Optional[str] = None
    period: Optional[float] = None


@dataclass
class InitEvent:
    UUID: str
    short_name: str
    start_on_event_ref: str
    dest: str


# 定义R_Event对应的DATA-SEND-EVENT的数据结构中的DATA-IREF FIX: 2023-12-21 17:23:50
@dataclass
class DataIref:
    context_r_port_ref: str
    target_data_element_ref: str


# 定义R_Event对应的DATA-RECEIVED-EVENT的数据结构 FIX: 2023-12-21 17:23:50
@dataclass
class DataReceivedEvent:
    UUID: str
    short_name: str
    start_on_event_ref: str
    data_iref: DataIref


# 定义OperationIrefPPort的数据结构 FIX: 2024-1-16 11:14:32
@dataclass
class OperationIrefPPort:
    context_p_port_ref: str
    target_provided_operation_ref: str


# 定义OPERATION-INVOKED-EVENT的数据结构 FIX: 2024-1-15 16:37:27
@dataclass
class OpreationInvokedEvent:
    UUID: str
    short_name: str
    start_on_event_ref: str
    operation_iref: OperationIrefPPort


@dataclass
class Events:
    timing_event: List[TimingEvent] = None
    init_event: Optional[InitEvent] = None
    data_received_event: List[DataReceivedEvent] = None
    opreation_invoked_event: List[OpreationInvokedEvent] = None


@dataclass
class PortPrototypeRef:
    dest: str
    value: str


@dataclass
class TargetDataPrototypeRef:
    dest: str
    value: str


@dataclass
class AutosarVariableIref:
    port_prototype_ref: PortPrototypeRef
    target_data_prototype_ref: TargetDataPrototypeRef


@dataclass
class AccessedVariable:
    autosar_variable_iref: AutosarVariableIref


@dataclass
class VariableAccess:
    short_name: str
    accessed_variable: AccessedVariable


@dataclass
class DataReceivePointByArguments:
    variable_access: List[VariableAccess] = None


@dataclass
class DataSendPoints:
    variable_access: List[VariableAccess] = None


@dataclass
class ContextRPortRef:
    dest: str
    value: str


@dataclass
class TargetRequiredOperationRef:
    dest: str
    value: str


@dataclass
class OperationIref:
    context_r_port_ref: ContextRPortRef
    target_required_operation_ref: TargetRequiredOperationRef


@dataclass
class SynchronousServerCallPoint:
    UUID: str
    short_name: str
    operation_iref: OperationIref


@dataclass
class ServerCallPoints:
    synchronous_server_call_point: List[SynchronousServerCallPoint] = None


@dataclass
class RunnableEntity:
    UUID: str
    short_name: str
    minimum_start_interval: float
    can_be_invoked_concurrently: bool
    data_receive_point_by_arguments: Optional[DataReceivePointByArguments] = None
    data_send_points: Optional[DataSendPoints] = None
    server_call_points: Optional[ServerCallPoints] = None
    symbol: Optional[str] = None


@dataclass
class Runnables:
    runnable_entity: List[RunnableEntity]


@dataclass
class SwcInternalBehavior:
    UUID: Optional[str] = None
    short_name: Optional[str] = None
    events: Optional[Events] = None
    runnables: Optional[Runnables] = None
    data_type_mapping_refs: Optional[DataTypeMappingRefs] = None


@dataclass
class InternalBehaviors:
    swc_internal_behavior: Optional[SwcInternalBehavior] = None
