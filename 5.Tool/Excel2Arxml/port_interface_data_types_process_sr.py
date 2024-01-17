# 目前DataType都能处理
# 对于C/S 类型的port interface, 由于其结构比较复杂, 于另外一个脚本处理
# 2024-1-8 14:53:31

import os
from autosar.xml import Reader  # https://github.com/cogu/autosar
import autosar.xml.enumeration as enum
import autosar.xml.element as ar_element
from autosar.xml import Document, Writer
import pandas as pd
import numpy as np

#########################   STEP 1 提取csv信息 #########################
excel_path = "../../2.Maf_InterfaceExcel/swc.xlsx"
df = pd.read_excel(excel_path)

# 这里可以对df进行筛选再赋值给df_all

df_all = df.copy()
df_all.drop_duplicates(keep="first", inplace=True)

# 构建被引用数据类型的集合
referenced_types = set()

# 找到所有第一列为空值，且"Element(Structure/Array/Value)"列有值的行
# 这些行代表的element是被其他地方引用的
for index, row in df.iterrows():
    if pd.isna(row["Sender /Server"]) and not pd.isna(
        row["Element(Structure/Array/Value)"]
    ):
        referenced_type = row["Element(Structure/Array/Value)"].strip()
        referenced_types.add(referenced_type)


# 在构建ARXML的过程中，使用此集合来确定是否为被引用的类型
def is_referenced(base_type):
    return base_type in referenced_types


class Rocky_idt_data:
    def __init__(
        self,
        data_name,
        data_type,
        arr_size=None,
        base_type=None,
        struct_ele_name=None,
        struct_ele_size=None,
        struct_ele_type=None,
    ) -> None:
        self.data_name = data_name
        self.data_type = data_type
        self.base_type = base_type

        if data_type == "Array":
            self.arr_size = arr_size
        if data_type == "Structure":
            self.struct_ele_name = struct_ele_name
            self.struct_ele_type = struct_ele_type
            self.struct_ele_size = struct_ele_size


rocky_data = []
rocky_port = []
pi_names_set = set()

# 使用DataFrame的groupby函数将DataFrame按照 'Data name' 列的值进行分组
grouped_by_data_name = df_all.groupby("Data name", dropna=False)

for data_name, group in grouped_by_data_name:
    if pd.isna(data_name):
        # 如果 'Data name' 是 NaN，则表示这些行属于上一个非NaN 'Data name' 的子结构体/数组
        continue

    # 提取基本信息
    data_type_i = group.iloc[0]["Data type"].strip()
    base_type_i = group.iloc[0]["Base Type"].strip()
    DLC_i = group.iloc[0]["DLC"]

    # 处理Structure和Structure&Array类型
    if data_type_i in ["Structure"]:
        struct_ele_name = []
        struct_ele_type = []
        struct_ele_size = []

        for _, row in group.iterrows():
            signal_i = str(row["Signal"]).strip() if pd.notna(row["Signal"]) else ""
            current_base_type = (
                row["Base Type"].strip() if pd.notna(row["Base Type"]) else None
            )

            struct_ele_name.append(signal_i)
            struct_ele_type.append(current_base_type)
            struct_ele_size.append(DLC_i)

        rocky_data.append(
            Rocky_idt_data(
                data_name,
                data_type_i,
                DLC_i,
                base_type_i,
                struct_ele_name,
                struct_ele_size,
                struct_ele_type,
            )
        )
    else:
        # 处理非结构体类型
        signal_i = (
            str(group.iloc[0]["Signal"]).strip()
            if pd.notna(group.iloc[0]["Signal"])
            else ""
        )
        rocky_data.append(
            Rocky_idt_data(
                data_name,
                data_type_i,
                DLC_i,
                base_type_i,
                [signal_i],
                [DLC_i],
                [base_type_i],
            )
        )

    # 处理Port Interface
    for _, row in group.iterrows():
        if pd.isna(row["Sender /Server"]):
            # 表示这是一个嵌套结构体或者数组，不作为 Port interface
            continue

        sender = row["Sender /Server"].strip()
        receiver = row["Receiver /Client"].strip()
        element_name_i = row["Element name"].strip()
        pi_name_i = f"Pi_M_{element_name_i}"

        if pi_name_i not in pi_names_set:
            rocky_port.append({"pi_name": pi_name_i, "data_name": element_name_i})
            pi_names_set.add(pi_name_i)

# 记录一下总共有多少个port interface和data
total_interface = len(rocky_port)
total_data = len(rocky_data)
##########################  STEP 2 生成Arxml   ##########################
file_path = "../../3.Maf_Arxml/GmMomentaComposition_swc.arxml"
reader = Reader()
document = reader.read_file(file_path)

"""
for package in document.packages:
    print(package.name)
"""

ImplementationDataTypes = document.packages[1].packages[0]  # 'ImplementationDataTypes'
PortInterfaces = document.packages[2]


def add_array_element(package, arr_name, array_size, base_type):
    # array也有可能是引用的
    if is_referenced(base_type):
        arr_sw_data_def_props = ar_element.SwDataDefPropsConditional(
            impl_data_type_ref="/DataTypes/ImplementationDataTypes/IdtM_" + base_type
        )
    else:
        arr_sw_data_def_props = ar_element.SwDataDefPropsConditional(
            impl_data_type_ref="/AUTOSAR_Platform/ImplementationDataTypes/" + base_type
        )
    array_sub_element = ar_element.ImplementationDataTypeElement(
        "ImplementationDataTypeElement_0",
        category="TYPE_REFERENCE",
        array_size=int(array_size),
        array_size_semantics=enum.ArraySizeSemantics(0),
        sw_data_def_props=arr_sw_data_def_props,
    )
    impl_dt = ar_element.ImplementationDataType(
        arr_name, category="ARRAY", sub_elements=[array_sub_element]
    )
    try:
        package.append(impl_dt)
    except:
        # print(f"{impl_dt.name} already exists")
        global total_data
        total_data -= 1
        pass
    return


def add_value_element(package, value_name, base_type):
    value_sw_data_def_props = ar_element.SwDataDefPropsConditional(
        impl_data_type_ref="/AUTOSAR_Platform/ImplementationDataTypes/" + base_type
    )
    impl_dt = ar_element.ImplementationDataType(
        value_name, category="TYPE_REFERENCE", sw_data_def_props=value_sw_data_def_props
    )
    try:
        package.append(impl_dt)
    except:
        # print(f"{impl_dt.name} already exists")
        global total_data
        total_data -= 1
        pass
    return


def add_struct_element(
    package, struct_name, short_name_info, arr_size_info, base_type_info
):
    # 首先检查当前结构元素是否已经被添加
    if any(element.name == struct_name for element in package.elements):
        # print(f"{struct_name} already exists")
        global total_data
        total_data -= 1
        return

    struct_sw_data_def_props = ar_element.SwDataDefPropsConditional()
    struct_sub_elements = []
    existing_sub_names = set()  # 维护已存在子元素名称的集合

    for i in range(len(short_name_info)):
        short_name_i = short_name_info[i]
        base_type_i = base_type_info[i]

        # 检查子元素short_name是否已在当前结构中存在
        if short_name_i not in existing_sub_names:
            existing_sub_names.add(short_name_i)  # 将子元素名称添加到集合中

            if is_referenced(base_type_i):
                impl_data_type_ref = (
                    "/DataTypes/ImplementationDataTypes/IdtM_" + base_type_i
                )
            else:
                impl_data_type_ref = (
                    "/AUTOSAR_Platform/ImplementationDataTypes/" + base_type_i
                )

            try:
                arr_size = int(arr_size_info[i])
            except ValueError:
                arr_size = None

            sw_data_def_props_i = ar_element.SwDataDefPropsConditional(
                impl_data_type_ref=impl_data_type_ref
            )

            struct_sub_element = ar_element.ImplementationDataTypeElement(
                short_name_i,
                category="TYPE_REFERENCE",
                array_size=arr_size,
                array_size_semantics=enum.ArraySizeSemantics(0)
                if arr_size is not None
                else None,
                sw_data_def_props=sw_data_def_props_i,
            )
            struct_sub_elements.append(struct_sub_element)
        else:
            # print(f'Sub-element {short_name_i} named as "{struct_name}" already exists and will not be added again.')
            pass

    impl_dt = ar_element.ImplementationDataType(
        struct_name,
        category="STRUCTURE",
        sw_data_def_props=struct_sw_data_def_props,
        sub_elements=struct_sub_elements,
    )

    package.append(impl_dt)


# add port interface
def add_port_interface(package, port):
    pi_name = port["pi_name"]
    data_name = port["data_name"]
    port_interface = ar_element.SenderReceiverInterface(pi_name)
    port_interface.data_name = data_name
    port_interface.Idt_name = "/DataTypes/ImplementationDataTypes/IdtM_" + data_name
    package.append(port_interface)
    # 修改了源码文件writer.py中的Writer Class 并新增了 _write_sender_receiver_interface函数


for port in rocky_port:
    add_port_interface(PortInterfaces, port)


# add implementation data
def add_data(package, data):
    if data.data_type == "Array":
        add_array_element(package, data.data_name, data.arr_size, data.base_type)
    if data.data_type == "Value":
        add_value_element(package, data.data_name, data.base_type)
    if data.data_type == "Structure":
        add_struct_element(
            package,
            data.data_name,
            data.struct_ele_name,
            data.struct_ele_size,
            data.struct_ele_type,
        )
    """
    except:
        print("wrong data:",data.data_name)"""


for data in rocky_data:
    add_data(ImplementationDataTypes, data)


# save file
writer = Writer()
writer.write_file(document, "document.arxml")
# print(f"P/R Port Interface arxml saved to {os.path.abspath('document.arxml')}")

# print statistics
print(f"Total P/R Port Interface:  {total_interface}")
print(f"Total Implementation Data: {total_data}")
