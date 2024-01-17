from dataclasses import dataclass
from typing import List
from lxml import etree


@dataclass
class CLIENT_SERVER_INTERFACE:
    SHORT_NAME: str
    IS_SERVICE: bool
    OPERATIONS: List["CLIENT_SERVER_OPERATION"]
    POSSIBLE_ERRORS: List["APPLICATION_ERROR"]


@dataclass
class CLIENT_SERVER_OPERATION:
    SHORT_NAME: str
    ARGUMENTS: List["ARGUMENT_DATA_PROTOTYPE"]
    POSSIBLE_ERROR_REFS: List["POSSIBLE_ERROR_REF"]


@dataclass
class ARGUMENT_DATA_PROTOTYPE:
    SHORT_NAME: str
    TYPE_TREF_DEST: str
    DIRECTION: str
    SERVER_ARGUMENT_IMPL_POLICY: str


@dataclass
class POSSIBLE_ERROR_REF:
    DEST: str


@dataclass
class APPLICATION_ERROR:
    SHORT_NAME: str
    ERROR_CODE: int


def serialize_to_xml(data: CLIENT_SERVER_INTERFACE) -> etree._Element:
    root = etree.Element("CLIENT-SERVER-INTERFACE")

    short_name = etree.SubElement(root, "SHORT-NAME")
    short_name.text = data.SHORT_NAME

    is_service = etree.SubElement(root, "IS-SERVICE")
    is_service.text = str(data.IS_SERVICE)

    operations = etree.SubElement(root, "OPERATIONS")
    for operation in data.OPERATIONS:
        operation_elem = etree.SubElement(operations, "CLIENT-SERVER-OPERATION")

        short_name = etree.SubElement(operation_elem, "SHORT-NAME")
        short_name.text = operation.SHORT_NAME

        arguments = etree.SubElement(operation_elem, "ARGUMENTS")
        for argument in operation.ARGUMENTS:
            argument_elem = etree.SubElement(arguments, "ARGUMENT-DATA-PROTOTYPE")

            short_name = etree.SubElement(argument_elem, "SHORT-NAME")
            short_name.text = argument.SHORT_NAME

            type_tref_dest = etree.SubElement(argument_elem, "TYPE-TREF")
            type_tref_dest.text = argument.TYPE_TREF_DEST
            type_tref_dest.attrib["DEST"] = argument.TYPE_TREF_DEST

            direction = etree.SubElement(argument_elem, "DIRECTION")
            direction.text = argument.DIRECTION

            server_argument_impl_policy = etree.SubElement(
                argument_elem, "SERVER-ARGUMENT-IMPL-POLICY"
            )
            server_argument_impl_policy.text = argument.SERVER_ARGUMENT_IMPL_POLICY

        possible_error_refs = etree.SubElement(operation_elem, "POSSIBLE-ERROR-REFS")
        for error_ref in operation.POSSIBLE_ERROR_REFS:
            error_ref_elem = etree.SubElement(possible_error_refs, "POSSIBLE-ERROR-REF")
            error_ref_elem.text = error_ref.DEST
            error_ref_elem.attrib["DEST"] = error_ref.DEST

    possible_errors = etree.SubElement(root, "POSSIBLE-ERRORS")
    for error in data.POSSIBLE_ERRORS:
        error_elem = etree.SubElement(possible_errors, "APPLICATION-ERROR")

        short_name = etree.SubElement(error_elem, "SHORT-NAME")
        short_name.text = error.SHORT_NAME

        error_code = etree.SubElement(error_elem, "ERROR-CODE")
        error_code.text = str(error.ERROR_CODE)

    return root


# Define the nested structure
test_instance = CLIENT_SERVER_INTERFACE(
    SHORT_NAME="CS_TimeOT",  # Interface name
    IS_SERVICE=False,
    OPERATIONS=[
        CLIENT_SERVER_OPERATION(
            SHORT_NAME="TimeOT",  # Element name
            ARGUMENTS=[
                ARGUMENT_DATA_PROTOTYPE(
                    SHORT_NAME="timeStamp",  # Data name
                    TYPE_TREF_DEST="/DataTypes/ImplementationDataTypes/IdtM_TimeOT",  # Data name
                    DIRECTION="OUT",  # 暂时是OUT
                    SERVER_ARGUMENT_IMPL_POLICY="USE-ARGUMENT-TYPE",
                )
            ],
            POSSIBLE_ERROR_REFS=[
                POSSIBLE_ERROR_REF(
                    DEST="/AUTOSAR_EcuM/PortInterfaces/EcuM_BootTarget/E_NOT_OK"
                ),
                POSSIBLE_ERROR_REF(
                    DEST="/AUTOSAR_Dcm/PortInterfaces/DataServices_DID_DA05_MFOPExhaustPneumaticFailure_15_0/E_OK"
                ),
            ],
        )
    ],
    POSSIBLE_ERRORS=[
        APPLICATION_ERROR(SHORT_NAME="E_OK", ERROR_CODE=0),
        APPLICATION_ERROR(SHORT_NAME="E_NOT_OK", ERROR_CODE=1),
    ],
)
