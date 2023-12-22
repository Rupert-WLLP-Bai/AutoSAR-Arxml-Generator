# file: componentTypes.py
# author: JunhaoBai
# date: 2023/11/24

from dataclasses import dataclass
from typing import Optional
from .adminData import AdminData
from .prPorts import Ports
from .internalBehaviors import InternalBehaviors


@dataclass
class ComponentType:
    UUID: str
    short_name: str
    admin_data: Optional[AdminData] = None
    ports: Optional[Ports] = None
    internal_behaviors: Optional[InternalBehaviors] = None
