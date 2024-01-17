# file: pr_ports.py
# author: JunhaoBai
# date: 2023/11/24
# last modify: 2024-1-15 16:18:16

from __future__ import annotations  # 用于解决循环引用问题
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class NumericalValueSpecification:
    value: int | float
    short_label: Optional[str] = None


@dataclass
class Elements:
    # TODO: 数组中的Elements可能还会存在ArrayValueSpecification和RecordValueSpecification
    numerical_value_specification: List[NumericalValueSpecification] = None
    array_value_specification: List[ArrayValueSpecification] = None
    record_value_specification: List[RecordValueSpecification] = None


@dataclass
class Fields:
    # TODO: 结构体中的Fields可能还会存在ArrayValueSpecification和RecordValueSpecification
    numerical_value_specification: List[NumericalValueSpecification] = None
    array_value_specification: List[ArrayValueSpecification] = None
    record_value_specification: List[RecordValueSpecification] = None


@dataclass
class ArrayValueSpecification:
    elements: Elements


@dataclass
class RecordValueSpecification:
    fields: Fields


@dataclass
class InitValue:
    numerical_value_specification: Optional[NumericalValueSpecification] = None
    array_value_specification: Optional[ArrayValueSpecification] = None
    record_value_specification: Optional[RecordValueSpecification] = None


@dataclass
class Filter:
    data_filter_type: str


@dataclass
class DataElementRef:
    dest: str
    value: str


@dataclass
class NonQueuedReceiverComSpec:
    uses_end_to_end_protection: bool
    filter: Filter
    alive_timeout: Optional[float] = None
    enable_update: Optional[bool] = None
    handle_never_received: Optional[bool] = None
    data_element_ref: Optional[DataElementRef] = None


@dataclass
class QueuedReceiverComSpec:
    data_element_ref: DataElementRef
    external_replacement_ref: str
    dest_external_replacement_ref: str
    queue_length: int


@dataclass
class NonQueuedSenderComSpec:
    uses_end_to_end_protection: bool
    init_value: Optional[InitValue] = None
    data_element_ref: Optional[DataElementRef] = None


@dataclass
class OperationRef:
    dest: str
    value: str


@dataclass
class ServerComSpec:
    operation_ref: OperationRef
    queue_length: int


@dataclass
class RequiredComSpecs:
    queued_receiver_com_spec: Optional[QueuedReceiverComSpec] = None
    nonqueued_receiver_com_spec: Optional[NonQueuedReceiverComSpec] = None


@dataclass
class ProvidedComSpecs:
    nonqueued_sender_com_spec: Optional[NonQueuedSenderComSpec] = None
    server_com_spec: Optional[ServerComSpec] = None


@dataclass
class RequiredInterfaceTref:
    dest: str
    value: str


@dataclass
class RPortPrototype:
    UUID: str
    short_name: str
    required_interface_tref: RequiredInterfaceTref
    required_com_specs: Optional[RequiredComSpecs] = None


@dataclass
class ProvidedInterfaceTref:
    dest: str
    value: str


@dataclass
class PPortPrototype:
    UUID: str
    short_name: str
    provided_interface_tref: ProvidedInterfaceTref
    provided_com_specs: Optional[ProvidedComSpecs] = None


@dataclass
class Ports:
    r_port_prototype: List[RPortPrototype] = None
    p_port_prototype: List[PPortPrototype] = None
