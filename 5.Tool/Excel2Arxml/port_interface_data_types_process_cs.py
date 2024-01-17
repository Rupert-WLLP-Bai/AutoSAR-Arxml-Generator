from client_server_process.client_server_interface import *
from typing import List
import pandas as pd
from lxml import etree

excel_path = "../../2.Maf_InterfaceExcel/swc.xlsx"
df = pd.read_excel(excel_path)
df_all = df[df["Port type"] == "CS"].copy()
# 按照Interface name进行去重
df_all.drop_duplicates(subset=["Interface name"], keep="first", inplace=True)

# print(df_all)

# 生成ARXML, 首先找到原有的arxml中的节点
# <AR-PACKAGE>
#       <SHORT-NAME>PortInterfaces</SHORT-NAME>
#       <ELEMENTS>
#       </ELEMENTS>
# </AR-PACKAGE>
result_arxml_path = "document.arxml"

tree = etree.parse(result_arxml_path)
root = tree.getroot()
port_interfaces_node = root.find(".//{*}AR-PACKAGE[{*}SHORT-NAME='PortInterfaces']")
elements_node = port_interfaces_node.find("{*}ELEMENTS")

instance: List[CLIENT_SERVER_INTERFACE] = []
# 对每一行 生成一个CLIENT_SERVER_INTERFACE
for index, row in df_all.iterrows():
    interface_name = row["Interface name"]
    element_name = row["Element name"]
    data_name = row["Data name"]
    instance.append(
        CLIENT_SERVER_INTERFACE(
            SHORT_NAME=interface_name,
            IS_SERVICE=False,
            OPERATIONS=[
                CLIENT_SERVER_OPERATION(
                    SHORT_NAME=element_name,
                    ARGUMENTS=[
                        ARGUMENT_DATA_PROTOTYPE(
                            SHORT_NAME=data_name,
                            TYPE_TREF_DEST=f"DataTypes/ImplementationDataTypes/{data_name}",
                            DIRECTION="OUT",
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
    )

for interface in instance:
    if elements_node is None:
        raise Exception("elements_node is None")
    new_node = serialize_to_xml(interface)
    elements_node.append(new_node)

print("Total C/S Port Interface: ", len(instance))

with open(result_arxml_path, "w") as f:
    f.write(etree.tostring(root, pretty_print=True, encoding="utf-8").decode("utf-8"))
