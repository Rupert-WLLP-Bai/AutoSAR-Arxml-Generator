# file: ports_creator.py
# author: JunhaoBai
# date: 2023-11-30 10:34:02
# last modified: 2024-1-15 16:18:23

from lxml import etree
from .component_types import ComponentType
from .internal_behaviors import *
from .admin_data import *
from .pr_ports import *


# TODO: 对于NONQUEUED-RECEIVER-COM-SPEC和NONQUEUED-SENDER-COM-SPEC中的INIT-VALUE
# 其中的ARRAY-VALUE-SPECIFICATION和RECORD-VALUE-SPECIFICATION之中还可能嵌套其他的ARRAY-VALUE-SPECIFICATION和RECORD-VALUE-SPECIFICATION，需要进一步处理
# 使用递归的方式处理
def create_numerical_value_specification(parent_element, numerical_value_spec):
    nvs_element = etree.SubElement(parent_element, "NUMERICAL-VALUE-SPECIFICATION")
    if numerical_value_spec.short_label:
        short_label_element = etree.SubElement(nvs_element, "SHORT-LABEL")
        short_label_element.text = numerical_value_spec.short_label
    value_element = etree.SubElement(nvs_element, "VALUE")
    value_element.text = str(numerical_value_spec.value)


def create_array_value_specification(parent_element, array_value_spec):
    avs_element = etree.SubElement(parent_element, "ARRAY-VALUE-SPECIFICATION")
    elements_element = etree.SubElement(avs_element, "ELEMENTS")
    if array_value_spec.elements.numerical_value_specification:
        for (
            numerical_value_specification
        ) in array_value_spec.elements.numerical_value_specification:
            numerical_value_specification_element = etree.SubElement(
                elements_element, "NUMERICAL-VALUE-SPECIFICATION"
            )
            value_element = etree.SubElement(
                numerical_value_specification_element, "VALUE"
            )
            value_element.text = str(numerical_value_specification.value)
    if array_value_spec.elements.array_value_specification:
        for (
            array_value_specification
        ) in array_value_spec.elements.array_value_specification:
            create_array_value_specification(
                elements_element, array_value_specification
            )
    if array_value_spec.elements.record_value_specification:
        for (
            record_value_specification
        ) in array_value_spec.elements.record_value_specification:
            create_record_value_specification(
                elements_element, record_value_specification
            )


def create_record_value_specification(parent_element, record_value_spec):
    rvs_element = etree.SubElement(parent_element, "RECORD-VALUE-SPECIFICATION")
    fields_element = etree.SubElement(rvs_element, "FIELDS")
    if record_value_spec.fields.numerical_value_specification:
        for (
            numerical_value_specification
        ) in record_value_spec.fields.numerical_value_specification:
            numerical_value_specification_element = etree.SubElement(
                fields_element, "NUMERICAL-VALUE-SPECIFICATION"
            )
            value_element = etree.SubElement(
                numerical_value_specification_element, "VALUE"
            )
            value_element.text = str(numerical_value_specification.value)
    if record_value_spec.fields.array_value_specification:
        for (
            array_value_specification
        ) in record_value_spec.fields.array_value_specification:
            create_array_value_specification(fields_element, array_value_specification)
    if record_value_spec.fields.record_value_specification:
        for (
            record_value_specification
        ) in record_value_spec.fields.record_value_specification:
            create_record_value_specification(
                fields_element, record_value_specification
            )


def create_init_value_element(init_value, parent_element):
    init_value_element = etree.SubElement(parent_element, "INIT-VALUE")
    if init_value.numerical_value_specification:
        create_numerical_value_specification(
            init_value_element, init_value.numerical_value_specification
        )
    if init_value.record_value_specification:
        create_record_value_specification(
            init_value_element, init_value.record_value_specification
        )
    if init_value.array_value_specification:
        create_array_value_specification(
            init_value_element, init_value.array_value_specification
        )


# 分别遍历P/R, 没有则不添加标签
def create_r_ports_xml(r_port_prototypes: List[RPortPrototype], ports):
    # 处理R-PORT-PROTOTYPEs~
    for r_port_prototype in r_port_prototypes:
        r_port_prototype_element = etree.SubElement(ports, "R-PORT-PROTOTYPE")
        r_port_prototype_element.attrib["UUID"] = r_port_prototype.UUID

        # 添加SHORT-NAME元素
        short_name_element = etree.SubElement(r_port_prototype_element, "SHORT-NAME")
        short_name_element.text = r_port_prototype.short_name

        # 如果存在REQUIRED-COM-SPECS，添加该元素及其子元素
        if r_port_prototype.required_com_specs:
            required_com_specs_element = etree.SubElement(
                r_port_prototype_element, "REQUIRED-COM-SPECS"
            )

            # 针对NONQUEUED-RECEIVER-COM-SPEC
            if r_port_prototype.required_com_specs.nonqueued_receiver_com_spec:
                nonqueued_receiver_com_spec_element = etree.SubElement(
                    required_com_specs_element, "NONQUEUED-RECEIVER-COM-SPEC"
                )
                # 添加DATA-ELEMENT-REF元素
                # 如果存在DATA-ELEMENT-REF，添加该元素及其子元素
                if (
                    r_port_prototype.required_com_specs.nonqueued_receiver_com_spec.data_element_ref
                ):
                    data_element_ref_element = etree.SubElement(
                        nonqueued_receiver_com_spec_element, "DATA-ELEMENT-REF"
                    )
                    data_element_ref_element.attrib[
                        "DEST"
                    ] = (
                        r_port_prototype.required_com_specs.nonqueued_receiver_com_spec.data_element_ref.dest
                    )
                    data_element_ref_element.text = (
                        r_port_prototype.required_com_specs.nonqueued_receiver_com_spec.data_element_ref.value
                    )

                # 添加USES-END-TO-END-PROTECTION元素
                uses_e2e_protection_element = etree.SubElement(
                    nonqueued_receiver_com_spec_element, "USES-END-TO-END-PROTECTION"
                )
                uses_e2e_protection_element.text = str(
                    r_port_prototype.required_com_specs.nonqueued_receiver_com_spec.uses_end_to_end_protection
                ).lower()

                # 添加ALIVE-TIMEOUT元素
                if (
                    r_port_prototype.required_com_specs.nonqueued_receiver_com_spec.alive_timeout
                ):
                    alive_timeout_element = etree.SubElement(
                        nonqueued_receiver_com_spec_element, "ALIVE-TIMEOUT"
                    )
                    alive_timeout_element.text = str(
                        r_port_prototype.required_com_specs.nonqueued_receiver_com_spec.alive_timeout
                    )

                # 添加ENABLE-UPDATE元素
                if (
                    r_port_prototype.required_com_specs.nonqueued_receiver_com_spec.enable_update
                ):
                    enable_update_element = etree.SubElement(
                        nonqueued_receiver_com_spec_element, "ENABLE-UPDATE"
                    )
                    enable_update_element.text = str(
                        r_port_prototype.required_com_specs.nonqueued_receiver_com_spec.enable_update
                    ).lower()

                # 添加FILTER元素
                if (
                    r_port_prototype.required_com_specs.nonqueued_receiver_com_spec.filter
                ):
                    filter_element = etree.SubElement(
                        nonqueued_receiver_com_spec_element, "FILTER"
                    )
                    data_filter_type_element = etree.SubElement(
                        filter_element, "DATA-FILTER-TYPE"
                    )
                    data_filter_type_element.text = (
                        r_port_prototype.required_com_specs.nonqueued_receiver_com_spec.filter.data_filter_type
                    )

                # 添加HANDLE-NEVER-RECEIVED元素
                if (
                    r_port_prototype.required_com_specs.nonqueued_receiver_com_spec.handle_never_received
                ):
                    handle_never_received_element = etree.SubElement(
                        nonqueued_receiver_com_spec_element, "HANDLE-NEVER-RECEIVED"
                    )
                    handle_never_received_element.text = str(
                        r_port_prototype.required_com_specs.nonqueued_receiver_com_spec.handle_never_received
                    ).lower()

        # 添加REQUIRED-INTERFACE-TREF元素 FIX: 2024-1-15 14:07:37 这个逻辑独立于NONQUEUED-RECEIVER-COM-SPEC
        required_interface_tref_element = etree.SubElement(
            r_port_prototype_element, "REQUIRED-INTERFACE-TREF"
        )
        required_interface_tref_element.attrib[
            "DEST"
        ] = r_port_prototype.required_interface_tref.dest
        required_interface_tref_element.text = (
            r_port_prototype.required_interface_tref.value
        )


def create_p_ports_xml(p_port_prototypes: List[PPortPrototype], ports):
    # 处理P-PORT-PROTOTYPEs
    for p_port_prototype in p_port_prototypes:
        p_port_prototype_element = etree.SubElement(ports, "P-PORT-PROTOTYPE")
        p_port_prototype_element.attrib["UUID"] = p_port_prototype.UUID

        # 添加SHORT-NAME元素
        short_name_element = etree.SubElement(p_port_prototype_element, "SHORT-NAME")
        short_name_element.text = p_port_prototype.short_name

        # 如果存在PROVIDED-COM-SPECS，添加该元素及其子元素
        if p_port_prototype.provided_com_specs:
            provided_com_specs_element = etree.SubElement(
                p_port_prototype_element, "PROVIDED-COM-SPECS"
            )

            # 针对NONQUEUED-SENDER-COM-SPEC
            if p_port_prototype.provided_com_specs.nonqueued_sender_com_spec:
                nonqueued_sender_com_spec_element = etree.SubElement(
                    provided_com_specs_element, "NONQUEUED-SENDER-COM-SPEC"
                )
                # 添加DATA-ELEMENT-REF元素
                if (
                    p_port_prototype.provided_com_specs.nonqueued_sender_com_spec.data_element_ref
                ):
                    data_element_ref_element = etree.SubElement(
                        nonqueued_sender_com_spec_element, "DATA-ELEMENT-REF"
                    )
                    data_element_ref_element.attrib[
                        "DEST"
                    ] = (
                        p_port_prototype.provided_com_specs.nonqueued_sender_com_spec.data_element_ref.dest
                    )
                    data_element_ref_element.text = (
                        p_port_prototype.provided_com_specs.nonqueued_sender_com_spec.data_element_ref.value
                    )

                # 添加USES-END-TO-END-PROTECTION元素
                uses_e2e_protection_element = etree.SubElement(
                    nonqueued_sender_com_spec_element, "USES-END-TO-END-PROTECTION"
                )
                uses_e2e_protection_element.text = str(
                    p_port_prototype.provided_com_specs.nonqueued_sender_com_spec.uses_end_to_end_protection
                ).lower()

                if (
                    p_port_prototype.provided_com_specs.nonqueued_sender_com_spec.init_value
                ):
                    # 添加INIT-VALUE元素 TODO: 需要进行递归处理
                    create_init_value_element(
                        p_port_prototype.provided_com_specs.nonqueued_sender_com_spec.init_value,
                        nonqueued_sender_com_spec_element,
                    )

            # 针对SERVER-COM-SPEC
            if p_port_prototype.provided_com_specs.server_com_spec:
                server_com_spec_element = etree.SubElement(
                    provided_com_specs_element, "SERVER-COM-SPEC"
                )
                # 添加OPERATION-REF元素
                operation_ref_element = etree.SubElement(
                    server_com_spec_element, "OPERATION-REF"
                )
                operation_ref_element.attrib[
                    "DEST"
                ] = (
                    p_port_prototype.provided_com_specs.server_com_spec.operation_ref.dest
                )
                operation_ref_element.text = (
                    p_port_prototype.provided_com_specs.server_com_spec.operation_ref.value
                )

                # 添加QUEUE-LENGTH元素
                queue_length_element = etree.SubElement(
                    server_com_spec_element, "QUEUE-LENGTH"
                )
                queue_length_element.text = str(
                    p_port_prototype.provided_com_specs.server_com_spec.queue_length
                )

        # 添加PROVIDED-INTERFACE-TREF元素 FIX: 2024-1-15 14:08:37 这个逻辑独立于NONQUEUED-SENDER-COM-SPEC
        provided_interface_tref_element = etree.SubElement(
            p_port_prototype_element, "PROVIDED-INTERFACE-TREF"
        )
        provided_interface_tref_element.attrib[
            "DEST"
        ] = p_port_prototype.provided_interface_tref.dest
        provided_interface_tref_element.text = (
            p_port_prototype.provided_interface_tref.value
        )


def create_ports_xml(
    p_port_prototypes: List[PPortPrototype],
    r_port_prototypes: List[RPortPrototype],
    application_sw_component_type,
):
    # PORTS
    ports = etree.SubElement(application_sw_component_type, "PORTS")
    create_p_ports_xml(p_port_prototypes, ports=ports)
    create_r_ports_xml(r_port_prototypes, ports=ports)
    return ports
