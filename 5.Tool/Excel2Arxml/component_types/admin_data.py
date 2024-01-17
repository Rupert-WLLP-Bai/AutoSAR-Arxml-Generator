# file: admin_data.py
# author: JunhaoBai
# date: 2023/11/24

from dataclasses import dataclass


@dataclass
class SDG:
    GID: str
    SD: bool


@dataclass
class SDGS:
    SDG: SDG


@dataclass
class AdminData:
    SDGS: SDGS
