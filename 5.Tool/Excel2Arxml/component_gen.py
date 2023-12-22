# /*
#  * @Author: junhao.bai
#  * @Date: 2023-11-27
#  * @Last Modified by:   junhao.bai
#  * @Last Modified time: 2023-12-21 20:46:55
#  */

import os
import uuid
from lxml import etree
import pandas as pd
from typing import List, Dict, Optional, Set, Tuple

from component_types.componentTypes import ComponentType
from component_types.prPorts import (
    ArrayValueSpecification,
    Elements,
    Fields,
    Filter,
    InitValue,
    NumericalValueSpecification,
    RecordValueSpecification,
    Ports,
    RPortPrototype,
    PPortPrototype,
    RequiredInterfaceTref,
    ProvidedInterfaceTref,
    RequiredComSpecs,
    ProvidedComSpecs,
    NonQueuedReceiverComSpec,
    NonQueuedSenderComSpec,
)
from component_types.ports_creator import create_ports_xml
from component_types.internal_behaviors_creator import create_internal_behaviors_xml
from component_types.internalBehaviors import (
    AccessedVariable,
    AutosarVariableIref,
    DataIref,
    DataReceivePointByArguments,
    DataReceivedEvent,
    DataSendPoints,
    Events,
    InitEvent,
    InternalBehaviors,
    PortPrototypeRef,
    RunnableEntity,
    Runnables,
    SwcInternalBehavior,
    TargetDataPrototypeRef,
    TimingEvent,
    VariableAccess,
)

import logging

logging.basicConfig(level=logging.WARNING)  # 设置日志级别 开发时为DEBUG, 运行时为WARNING
logger = logging.getLogger(__name__)


class CtApManager:
    def __init__(self, excel_path: str):
        self.basic_types = [
            "sint8",
            "uint8",
            "sint16",
            "uint16",
            "sint32",
            "sint64",
            "uint32",
            "uint64",
            "float32",
            "float64",
            "boolean",
        ]
        """初始化函数, 加载excel数据"""
        self.df = pd.read_excel(excel_path)
        self.complete_df = self.df.copy()  # 用于存储完整的DataFrame, 用于生成依赖关系字典
        self.definitions = {"Value": {}, "Array": {}, "Structure": {}}  # 用于存储依赖关系字典
        self.parse_definitions()  # 解析DataFrame中定义的数据结构, 生成依赖关系字典。
        self.df = self.df.dropna(
            axis=0, how="any", subset=["Sender /Server"]
        )  # 去除Sender /Server为空的行的数据, 用于生成CtAp_M_XXXX字典

    def parse_definitions(self):
        """
        解析DataFrame中定义的数据结构, 生成依赖关系字典。
        """
        # 需要用到的列是：Element(Structure/Array/Value), Data type, Base Type, Signal, DLC, Initial value
        # 总共是三个字典, Value, Array, Structure
        # 1.1 Data type是Structure的行, 若Element(Structure/Array/Value)相同则说明是同一个结构体, Signal是结构体的成员变量
        # 1.2 Data type是Structure的行, 若Base Type不是基本类型, 则说明Signal是一个结构体或者数组, 需要递归的进行处理
        # 1.3 Data type是Structure的行, 若Base Type是基本类型, 则说明Signal是一个基本类型的值, 不需要递归的进行处理
        # 注意: 这里Element(Structure/Array/Value)相同的行, 可能会重复添加Signal, 需要使用set进行去重
        # 2.1 Data type是Array的行, 若Ease Type不是基本类型, 则说明这个数组的元素是一组结构体或者数组, 需要递归的进行处理
        # 2.2 Data type是Array的行, 若Base Type是基本类型, 则说明这个数组的元素是一组基本类型的值, 不需要递归的进行处理
        # 3.1 Date type是Value的行, Base Type只有可能是基本类型, 不需要递归的进行处理
        # 首先创建一个dataframe存储需要的列
        minimal_df = self.complete_df[
            [
                "Element(Structure/Array/Value)",
                "Data type",
                "Base Type",
                "Signal",
                "DLC",
                "Initial value",
            ]
        ]

        # 先建立所有Value、Array和Structure的框架
        for index, row in minimal_df.iterrows():
            element = row["Element(Structure/Array/Value)"]
            data_type = row["Data type"]
            if element not in self.definitions[data_type]:
                if (
                    data_type == "Value"
                ):  # Value类型的数据, Base Type只有可能是基本类型, 将其添加到Value字典中
                    self.definitions[data_type][element] = {
                        "type": row["Base Type"],
                        "initial_value": 0,
                        "is_value": True,
                        "is_array": False,
                        "is_structure": False,
                    }
                else:  # Array和Structure类型的数据, Base Type可能是基本类型, 也可能是数组或者结构体, 先将其添加到字典中, 然后再进行处理
                    self.definitions[data_type][element] = {
                        "type": data_type,
                        "base_type": None
                        if data_type == "Structure"
                        else row["Base Type"],
                        "is_value": False,
                        "is_array": True if data_type == "Array" else False,
                        "is_structure": True if data_type == "Structure" else False,
                        "members": {} if data_type == "Structure" else None,
                        "dlc": None if data_type == "Structure" else int(row["DLC"]),
                        "initial_value": 0,  # 这里暂时都是0
                    }

        # 然后填充结构体和数组内部的详细信息
        for index, row in minimal_df.iterrows():
            element = row["Element(Structure/Array/Value)"]
            data_type = row["Data type"]
            base_type = row["Base Type"]
            signal = row["Signal"]

            if data_type == "Structure":
                structure_dict = self.definitions[data_type][element]["members"]
                if signal not in structure_dict:  # 确保不重复添加
                    structure_dict[signal] = {
                        "base_type": base_type,
                        "type": base_type,
                        "is_value": base_type in self.basic_types,
                        "is_array": base_type in self.definitions["Array"],
                        "is_structure": base_type in self.definitions["Structure"],
                        "initial_value": 0,  # 这里暂时都是0
                    }
                elif data_type == "Array":
                    array_info = self.definitions[data_type][element]
                    is_base_type_basic = base_type in self.basic_types
                    is_base_type_array = (
                        base_type in self.definitions["Array"]
                        and not is_base_type_basic
                    )
                    is_base_type_structure = (
                        base_type in self.definitions["Structure"]
                        and not is_base_type_basic
                    )

                    array_info["base_type"] = base_type
                    array_info["is_value"] = is_base_type_basic
                    array_info["is_array"] = is_base_type_array
                    array_info["is_structure"] = is_base_type_structure
                    array_info["initial_value"] = 0  # Default initial value

                    # If the base type of the array is a structure, copy the members from the structure definition.
                    if is_base_type_structure:
                        struct_members = self.definitions["Structure"][base_type].get(
                            "members", {}
                        )
                        if isinstance(struct_members, set):
                            struct_members = {
                                member: self.definitions["Structure"][member]
                                for member in struct_members
                            }
                        array_info["members"] = struct_members
                        array_info["dlc"] = int(row["DLC"])

    def _extract_triggers(self) -> Dict[str, Set[str]]:
        """
        展开S_Trigger和R_Trigger, 并且将其添加到字典中
        """
        triggers = {}
        for _, row in self.df.iterrows():
            sender_ctap_name = f"CtAp_M_{row['Sender /Server']}"
            receiver_ctap_name = f"CtAp_M_{row['Receiver /Client']}"

            # Process S_Trigger column for the sender
            if pd.notna(row["S_Trigger"]):
                if sender_ctap_name not in triggers:
                    triggers[sender_ctap_name] = set()
                triggers[sender_ctap_name].add(str(row["S_Trigger"]).strip())

            # Process R_Trigger column for the receiver
            if pd.notna(row["R_Trigger"]):
                if receiver_ctap_name not in triggers:
                    triggers[receiver_ctap_name] = set()
                triggers[receiver_ctap_name].add(str(row["R_Trigger"]).strip())
        return triggers

    def _get_port_and_data_prototype_refs(
        self, trigger_interval: str, ctap_name: str
    ) -> Tuple[Optional[DataReceivePointByArguments], Optional[DataSendPoints]]:
        # TODO: 这里假设所有的Sender都是DataSendPoints, 所有的Receiver都是DataReceivePointByArguments
        # TODO: 还需要处理S_Trigger和R_Trigger的值为R_EVENT的情况, 所以这里暂时把trigger_interval的类型设置为str

        data_receive_points = None
        data_send_points = None

        # 筛选当前组件和触发器间隔的 dataframe 行
        sender_rows = self.df[
            (self.df["Sender /Server"] == ctap_name[7:])  # 去除 CtAp_M_ 前缀
            & (self.df["S_Trigger"] == trigger_interval)
        ]
        receiver_rows = self.df[
            (self.df["Receiver /Client"] == ctap_name[7:])  # 去除 CtAp_M_ 前缀
            & (self.df["R_Trigger"] == trigger_interval)
        ]

        # 处理发送者的 DataSendPoints
        if not sender_rows.empty:
            variable_access_list = []
            added_elements = set()  # 检查是否有重复的元素
            for _, row_data in sender_rows.iterrows():
                element_name = f'{row_data["Element(Structure/Array/Value)"]}'
                if element_name not in added_elements:
                    variable_access = VariableAccess(
                        short_name=f'DSP_M_{row_data["Element name"]}_0',  # DSP表示DataSendPoints FIX: 加上一个_M_用于区分 2023-12-15 15:30:51
                        accessed_variable=AccessedVariable(
                            autosar_variable_iref=AutosarVariableIref(
                                port_prototype_ref=PortPrototypeRef(
                                    dest="P-PORT-PROTOTYPE",
                                    value=f"/ComponentTypes/{ctap_name}/{row_data['Properties name']}",
                                ),
                                target_data_prototype_ref=TargetDataPrototypeRef(
                                    dest="VARIABLE-DATA-PROTOTYPE",
                                    value=f"/PortInterfaces/{row_data['Interface name']}/{row_data['Element name']}",
                                ),
                            )
                        ),
                    )
                    variable_access_list.append(variable_access)
                    added_elements.add(element_name)
            data_send_points = DataSendPoints(variable_access=variable_access_list)

        # 处理接收者的 DataReceivePointByArguments
        if not receiver_rows.empty:
            variable_access_list = []
            added_elements = set()  # 检查是否有重复的元素
            for _, row_data in receiver_rows.iterrows():
                element_name = f'{row_data["Element(Structure/Array/Value)"]}'
                if element_name not in added_elements:
                    variable_access = VariableAccess(
                        short_name=f'DRPA_M_{row_data["Element name"]}_0',  # DRPA表示DataReceivePointByArguments FIX: 加上一个_M_用于区分 2023-12-15 15:30:47
                        accessed_variable=AccessedVariable(
                            autosar_variable_iref=AutosarVariableIref(
                                port_prototype_ref=PortPrototypeRef(
                                    dest="R-PORT-PROTOTYPE",
                                    value=f"/ComponentTypes/{ctap_name}/{row_data['Properties name']}",
                                ),
                                target_data_prototype_ref=TargetDataPrototypeRef(
                                    dest="VARIABLE-DATA-PROTOTYPE",
                                    value=f"/PortInterfaces/{row_data['Interface name']}/{row_data['Element name']}",
                                ),
                            )
                        ),
                    )
                    variable_access_list.append(variable_access)
                    added_elements.add(element_name)
            data_receive_points = DataReceivePointByArguments(
                variable_access=variable_access_list
            )

        return data_receive_points, data_send_points

    def create_ctap_m_dict(self) -> Dict[str, Dict]:
        """创建所有唯一CtAp_M_XXXX命名的字典集合，包括pports和rports"""
        ctap_m_dict = {}

        # FIXME: 这里是否会存在Sender是空值的情况仍然被添加到字典中的情况?
        for _, row in self.df.iterrows():
            sender_key = f"CtAp_M_{row['Sender /Server']}"
            receiver_key = f"CtAp_M_{row['Receiver /Client']}"

            # Ensure that the sender and receiver components are present in the dictionary
            if sender_key not in ctap_m_dict:
                ctap_m_dict[sender_key] = {"pports": {}, "rports": {}}
            if receiver_key not in ctap_m_dict:
                ctap_m_dict[receiver_key] = {"pports": {}, "rports": {}}

            # Define a common structure to hold port data
            port_data = {
                "Sender /Server": row["Sender /Server"],
                "Receiver /Client": row["Receiver /Client"],
                "port_type": row["Port type"],  # "SR
                "interface_name": row["Interface name"],
                "element_name": row["Element name"],
                "properties_name": row["Properties name"],
                "data_name": row["Data name"],
                "element": row["Element(Structure/Array/Value)"],
                "signal": row["Signal"],
                "signal_description": row["Signal description"],
                "data_type": row["Data type"],
                "base_type": row.get("Base Type", ""),
                "dlc": row.get("DLC", None),  # Data Length Code or size
                "initial_value": row.get("Initial value", None),
                "runnable_name_sender": row.get("Sender/Client Runnable Name", None),
                "runnable_name_receiver": row.get(
                    "Receiver/Server Runnable Name", None
                ),
            }

            # 这里假设都是SR类型的端口, 之后可以扩展
            if row["Port type"] == "SR":  # Assuming SR indicates Sender-Receiver ports
                ctap_m_dict[sender_key]["pports"][row["Properties name"]] = port_data
                ctap_m_dict[receiver_key]["rports"][row["Properties name"]] = port_data

        return ctap_m_dict

    def create_numerical_value_specification(
        self, value=0
    ) -> NumericalValueSpecification:
        """Creates a NumericalValueSpecification with the provided value."""
        if pd.isna(value):
            value = 0
        return NumericalValueSpecification(value=value)

    def create_array_value_specification(self, element_def) -> ArrayValueSpecification:
        if element_def["base_type"] in self.basic_types:
            # Create an array of numerical values if the base type is basic.
            logger.info(
                f"[BASIC-TYPE-IN-ARRAY] {element_def['base_type']} is a basic type in an array."
            )
            logger.info(
                f"[BASIC-TYPE-IN-ARRAY] Creating {element_def['dlc']} numerical values."
            )
            return ArrayValueSpecification(
                elements=Elements(
                    numerical_value_specification=[
                        self.create_numerical_value_specification(0)
                        for _ in range(element_def["dlc"])
                    ]
                )
            )
        else:
            # If the base type is not basic, retrieve the full definition and process accordingly.
            full_def = self.get_definition(element_def["base_type"])
            if full_def["is_array"]:
                # Recursively create array specifications for nested arrays.
                logger.info(
                    f"[ARRAY-IN-ARRAY] {element_def['base_type']} is an array in an array."
                )
                logger.info(f"[ARRAY-IN-ARRAY] Creating {element_def['dlc']} arrays.")
                # logger.info(f"[ARRAY-IN-ARRAY] Full definition: {full_def}")
                return ArrayValueSpecification(
                    elements=Elements(
                        array_value_specification=[
                            self.create_array_value_specification(full_def)
                            for _ in range(element_def["dlc"])
                        ]
                    )
                )
            elif full_def["is_structure"]:
                # Recursively create record specifications for nested structures.
                logger.info(
                    f"[STRUCTURE-IN-ARRAY] {element_def['base_type']} is a structure in an array."
                )
                logger.info(
                    f"[STRUCTURE-IN-ARRAY] Creating {element_def['dlc']} records."
                )
                # logger.info(f"[STRUCTURE-IN-ARRAY] Full definition: {full_def}")
                return ArrayValueSpecification(
                    elements=Elements(
                        record_value_specification=[
                            self.create_record_value_specification(full_def)
                            for _ in range(element_def["dlc"])
                        ]
                    )
                )
            else:
                logger.error(
                    f"{element_def['base_type']} is neither an array nor a structure."
                )
                return ArrayValueSpecification(elements=Elements())

    def create_record_value_specification(
        self, element_def
    ) -> RecordValueSpecification:
        fields = Fields(
            numerical_value_specification=[],
            array_value_specification=[],
            record_value_specification=[],
        )

        if (
            element_def is None
            or "members" not in element_def
            or not element_def["members"]
        ):
            logger.error(
                f"Invalid element definition: {element_def} beacuse it has no members."
            )
            return RecordValueSpecification(fields=fields)

        for member_name, member_info in element_def["members"].items():
            # 如果是基本类型, 则直接添加数值
            if member_info["is_value"]:
                fields.numerical_value_specification.append(
                    self.create_numerical_value_specification(0)
                )
                continue

            full_member_def = self.get_definition(member_info["base_type"])

            if full_member_def["is_array"]:
                logger.info(
                    f"[ARRAY-IN-STRUCTURE] {member_info['base_type']} is an array in a structure."
                )
                logger.info(
                    f"[ARRAY-IN-STRUCTURE] Creating {full_member_def['dlc']} arrays."
                )
                # logger.info(f"[ARRAY-IN-STRUCTURE] Full definition: {full_member_def}")
                fields.array_value_specification.append(
                    self.create_array_value_specification(full_member_def)
                )
            elif full_member_def["is_structure"]:
                logger.info(
                    f"[STRUCTURE-IN-STRUCTURE] {member_info['base_type']} is a structure in a structure."
                )
                logger.info(
                    f"[STRUCTURE-IN-STRUCTURE] Creating a nested record: {member_name}."
                )
                # logger.info(f"[STRUCTURE-IN-STRUCTURE] Full definition: {full_member_def}")
                fields.record_value_specification.append(
                    self.create_record_value_specification(full_member_def)
                )

        return RecordValueSpecification(fields=fields)

    def create_init_value_specification(self, element_def):
        """Recursively creates an InitValue for the given element definition."""
        init_value = InitValue(
            numerical_value_specification=None,
            array_value_specification=None,
            record_value_specification=None,
        )

        # 对于不同的类型, 采用不同的方式进行处理
        if element_def["is_value"]:
            # 如果是基本类型, 则直接添加数值
            init_value.numerical_value_specification = (
                self.create_numerical_value_specification(element_def["initial_value"])
            )
        elif element_def["is_array"]:
            # 如果是数组, 则调用create_array_value_specification函数进行处理
            init_value.array_value_specification = (
                self.create_array_value_specification(element_def)
            )
        elif element_def["is_structure"]:
            # 如果是结构体, 则调用create_record_value_specification函数进行处理
            init_value.record_value_specification = (
                self.create_record_value_specification(element_def)
            )

        return init_value

    def get_definition(self, element_name):
        """Retrieves the definition for a given element name from self.definitions."""
        if element_name in self.definitions["Value"]:
            return self.definitions["Value"][element_name]
        elif element_name in self.definitions["Array"]:
            return self.definitions["Array"][element_name]
        elif element_name in self.definitions["Structure"]:
            return self.definitions["Structure"][element_name]
        else:
            raise ValueError(f"Definition for element '{element_name}' not found.")

    def create_component_type_list(
        self, result_dict: Dict[str, Dict]
    ) -> List[ComponentType]:
        """添加ComponentTypes到列表中"""
        component_type_list = []

        # 添加P-PORT-PROTOTYPEs和R-PORT-PROTOTYPEs
        for short_name, ports_data in result_dict.items():
            r_port_prototype_list = [
                RPortPrototype(
                    UUID=uuid.uuid4().hex.upper(),
                    short_name=str(rport),
                    required_interface_tref=RequiredInterfaceTref(
                        dest="SENDER-RECEIVER-INTERFACE",
                        value=f"/PortInterfaces/{port_info['interface_name']}",
                    ),
                    required_com_specs=RequiredComSpecs(
                        nonqueued_receiver_com_spec=NonQueuedReceiverComSpec(
                            uses_end_to_end_protection=False,  # 是否使用端到端保护, 默认为False
                            filter=Filter("ALWAYS"),  # 过滤器, 默认为ALWAYS
                        )
                    ),
                )
                for rport, port_info in ports_data.get("rports", []).items()
            ]

            p_port_prototype_list = [
                PPortPrototype(
                    UUID=uuid.uuid4().hex.upper(),
                    short_name=str(pport),
                    provided_interface_tref=ProvidedInterfaceTref(
                        dest="SENDER-RECEIVER-INTERFACE",
                        value=f"/PortInterfaces/{port_info['interface_name']}",
                    ),
                    provided_com_specs=ProvidedComSpecs(
                        nonqueued_sender_com_spec=NonQueuedSenderComSpec(
                            uses_end_to_end_protection=False,  # 是否使用端到端保护, 默认为False
                            init_value=self.create_init_value_specification(
                                self.get_definition(port_info["element"])
                            ),
                        )
                    ),
                )
                for pport, port_info in ports_data.get("pports", []).items()
            ]

            ports_object = Ports(
                r_port_prototype=r_port_prototype_list,
                p_port_prototype=p_port_prototype_list,
            )

            # TODO 添加InternalBehaviors, 从Excel中读取并且生成, 还需要分析对应的Events和Runnables的内容
            triggers = self._extract_triggers()
            runnables_list: List[RunnableEntity] = []
            timing_events = []
            trigger_intervals = triggers.get(short_name, set())

            # FIX: 2023-12-21 17:39:18 处理R_EVENT的情况
            dataReceivedEvents = []

            # FIX: 在遍历开始之前先添加一个InitEvent, 再添加一个R_M_XX_Init的Runnable 2023-12-15 15:33:07
            initEvent = InitEvent(
                UUID=uuid.uuid4().hex.upper(),
                short_name=f"TMT_R_M_{short_name[7:]}_InitEvent",
                start_on_event_ref=f"/ComponentTypes/{short_name}/{short_name}_InternalBehavior/R_M_{short_name[7:]}_Init",
                dest="RUNNABLE-ENTITY",
            )
            
            runnables_list.append(
                RunnableEntity(
                    UUID=uuid.uuid4().hex.upper(),
                    short_name=f"R_M_{short_name[7:]}_Init",
                    minimum_start_interval=0.0,
                    can_be_invoked_concurrently=False,
                    symbol=f"R_M_{short_name[7:]}_Init",
                )
            )
            
            runnables = Runnables(runnable_entity=[])

            for interval in trigger_intervals:
                # interval可能不是"xxms"格式, 直接continue (可能是R_EVENT)
                res = interval.split("ms") # 暂时用于判断是xxms还是其他情况
                if len(res) == 2:
                    sanitized_interval = interval.replace(" ", "")
                    short_name_without_ctap = short_name[7:]  # 去除 CtAp_M_ 前缀
                    runnable_name = f"R_M_{short_name_without_ctap}_{sanitized_interval}"
                    timing_event_name = (
                        f"TMT_R_M_{short_name_without_ctap}_{sanitized_interval}"
                    )
                    timing_event_start_on_event_ref = f"/ComponentTypes/{short_name}/{short_name}_InternalBehavior/R_M_{short_name_without_ctap}_{sanitized_interval}"

                    (
                        data_receive_points,
                        data_send_points,
                    ) = self._get_port_and_data_prototype_refs(interval, short_name)
                    

                    runnables_list.append(
                        RunnableEntity(
                            UUID=uuid.uuid4().hex.upper(),
                            short_name=runnable_name,
                            minimum_start_interval=0.0,
                            can_be_invoked_concurrently=False,
                            # TODO: 重新修改_get_port_and_data_prototype_refs函数, 使其正确的匹配上引用ports的结果
                            data_receive_point_by_arguments=data_receive_points,
                            data_send_points=data_send_points,
                            symbol=runnable_name,
                        )
                    )
                    
                    for runnable in runnables_list:
                        runnables.runnable_entity.append(runnable)

                    timing_events.append(
                        TimingEvent(
                            UUID=uuid.uuid4().hex.upper(),
                            short_name=timing_event_name,
                            period=float(interval.split("ms")[0]) / 1000,
                            start_on_event_ref=timing_event_start_on_event_ref,
                            dest="RUNNABLE-ENTITY",
                        )
                    )
                else:
                    # TODO 在这里处理R_EVENT的情况, 假设除了xxms之外的情况都是R_EVENT
                    sanitized_interval = interval.replace(" ", "")
                    short_name_without_ctap = short_name[7:]  # 去除 CtAp_M_ 前缀
                    runnable_name = f"R_M_{short_name_without_ctap}_{sanitized_interval}"
                    data_received_event_name = (
                        f"TMT_R_M_{short_name_without_ctap}_{sanitized_interval}"
                    ) # 应该是TMT_R_M_XXXX_R_EVENT
                    data_received_event_start_on_event_ref = f"/ComponentTypes/{short_name}/{short_name}_InternalBehavior/R_M_{short_name_without_ctap}_{sanitized_interval}"
                    
                    # TODO 获取下面两个变量的值
                    context_r_port_ref = ''
                    target_data_element_ref = ''

                    # TODO 从df中检索
                    # 1. 获取context_r_port_ref
                    # 2. 获取target_data_element_ref
                    row = self.df[
                        (self.df["Receiver /Client"] == short_name_without_ctap)
                        & (self.df["R_Trigger"] == interval)
                    ]
                    # 对row进行去重, 对于row(Element(Structure/Array/Value))相同的行, 只保留第一行
                    row = row.drop_duplicates(subset=["Element(Structure/Array/Value)"], keep='first')

                    # 计数, 创建的Event名称不能相同
                    count = 0
                    if not row.empty:
                        for _, row_data in row.iterrows():
                            count += 1
                            context_r_port_ref = row_data["Properties name"]
                            target_data_element_ref = row_data["Element name"]
                            # 添加DataReceivedEvent
                            dataReceivedEvents.append(
                                DataReceivedEvent(
                                    UUID=uuid.uuid4().hex.upper(),
                                    short_name=f'{data_received_event_name}_{count}',
                                    start_on_event_ref=data_received_event_start_on_event_ref,
                                    data_iref=DataIref(
                                        context_r_port_ref=context_r_port_ref,
                                        target_data_element_ref=target_data_element_ref,
                                    )
                                )
                            )
                    else:
                        logger.error(f"R_EVENT: {short_name_without_ctap} {interval} not found in df")
                        continue


                    # 获取DataReceivePointByArguments和DataSendPoints
                    (
                        data_receive_points,
                        data_send_points,
                    ) = self._get_port_and_data_prototype_refs(interval, short_name)

                    # 创建RunnableEntity
                    runnables.runnable_entity.append(
                        RunnableEntity(
                            UUID=uuid.uuid4().hex.upper(),
                            short_name=runnable_name,
                            minimum_start_interval=0.0,
                            can_be_invoked_concurrently=False,
                            symbol=runnable_name,
                            data_receive_point_by_arguments=data_receive_points,
                            data_send_points=data_send_points,
                        )
                    )
                    

            # 创建一个Events对象, 包含timing_events和initEvent FIX: 2023-12-15 15:25:44
            timing_events_with_init = Events(
                timing_event=timing_events,
                init_event=initEvent,
                data_received_event=dataReceivedEvents,
            )

            internal_behaviors = InternalBehaviors(
                swc_internal_behavior=SwcInternalBehavior(
                    UUID=uuid.uuid4().hex.upper(),
                    short_name=f"{short_name}_InternalBehavior",
                    events=timing_events_with_init,
                    runnables=runnables,
                    data_type_mapping_refs=None,
                )
            )

            component_type_list.append(
                ComponentType(
                    UUID=uuid.uuid4().hex.upper(),
                    short_name=short_name,
                    ports=ports_object,
                    internal_behaviors=internal_behaviors,
                )
            )

        return component_type_list

    @staticmethod
    def generate_xml(component_type_list: List[ComponentType], output_file: str):
        """生成XML文件, 并写入output_file"""
        elements = etree.Element("ELEMENTS")

        for component_type in component_type_list:
            application_sw_component_type = etree.SubElement(
                elements, "APPLICATION-SW-COMPONENT-TYPE"
            )
            application_sw_component_type.attrib["UUID"] = component_type.UUID

            short_name_el = etree.SubElement(
                application_sw_component_type, "SHORT-NAME"
            )
            short_name_el.text = component_type.short_name

            # FIXME: 暂时不需要admin_data
            # admin_data = etree.SubElement(application_sw_component_type, "ADMIN-DATA")
            # sdgs = etree.SubElement(admin_data, "SDGS")
            # sdg = etree.SubElement(sdgs, "SDG")
            # sdg.set("GID", "UNKNOWN")
            # sd = etree.SubElement(sdg, "SD")
            # sd.text = str(True).lower()

            create_ports_xml(
                component_type.ports.p_port_prototype,
                component_type.ports.r_port_prototype,
                application_sw_component_type,
            )

            create_internal_behaviors_xml(
                component_type.internal_behaviors, application_sw_component_type
            )

        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse("document.arxml", parser)
        root = tree.getroot()

        # 添加新的ComponentTypes
        component_types = root.find(".//{*}AR-PACKAGE[{*}SHORT-NAME='ComponentTypes']")
        component_types.append(elements)

        with open(output_file, "wb") as f:
            tree.write(f, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    @staticmethod
    def count_and_print_stats(result_dict: Dict[str, Dict], output_file: str):
        """统计并打印信息"""
        ctap_m_count = len(result_dict)
        ports_count = sum(
            len(ports_data["pports"]) + len(ports_data["rports"])
            for ports_data in result_dict.values()
        )

        print(f"Total CtAp_M_XXXX entities created: {ctap_m_count}")
        print(f"Total ports created: {ports_count}")

        with open(output_file, "r") as f:
            lines = f.readlines()
            print(f"Total lines in the generated XML: {len(lines)}")

        print(
            f"The arxml file is generated successfully and saved to {os.path.abspath(output_file)}"
        )

    @staticmethod
    def cleanup_files(*files):
        """清理中间文件"""
        for file in files:
            if os.path.exists(file):
                os.remove(file)


# 使用新的CtApManager类和相关函数
if __name__ == "__main__":
    manager = CtApManager("../../2.Maf_InterfaceExcel/swc.xlsx")
    ctap_m_dict = manager.create_ctap_m_dict()
    component_type_list = manager.create_component_type_list(ctap_m_dict)

    # 生成XML文件名
    output_xml_file = "../../3.Maf_Arxml/result_component_new.arxml"

    CtApManager.generate_xml(component_type_list, output_xml_file)
    CtApManager.count_and_print_stats(ctap_m_dict, output_xml_file)

    # 删除中间文件, 如果存在
    CtApManager.cleanup_files("document.arxml")
