# author: Junhao Bai
# date: 2024-1-15 16:18:31
# version: 1.1
# description: This script is used to convert markdown and yaml files to excel files.
# change log:
# 1.0.1: 2023/11/21 更改了excel中嵌套结构体的表示方式，重构了traverse_array和traverse_value为traverse函数
# 1.0.1 - fix1 2023/11/22 拼接Signal列的时候，如果Signal列的值为空字符串，则不拼接，解决Signal重复时生成ARXML文件失败的问题
# 1.0.1 - fix2 2023/11/30 修改了global variables中md和yaml文件的路径
# 1.0.2 2023/12/01 实现了Array引用Structure的功能，优化了递归遍历函数的写法
# 1.0.2 - fix1 2023/12/01 完全重构了代码, 将不同的功能分别封装成类和函数，使得代码更加清晰易读
# 1.1 2024/01/15 实现了CS类型Port的Queued列的功能

# install the required packages
# pip install pandas
# pip install pyyaml

import pandas as pd
import yaml
import re
import os


class MarkdownTableProcessor:
    def parse_table(self, markdown_str):
        sections = re.split(r"# (.*)", markdown_str)[1:]
        _dataframes = []
        for i in range(0, len(sections), 2):
            table_name = sections[i].strip()
            rows = [
                re.split(r"\s*\|\s*", row.strip())
                for row in sections[i + 1].split("\n")
                if row.strip()
            ]
            rows.pop(1)
            df = pd.DataFrame(rows[1:], columns=[col.strip() for col in rows[0]])
            _dataframes.append([table_name, df])
        return _dataframes

    def read_markdown_file(self, file_name):
        with open(file_name, "r") as f:
            markdown_string = f.read()
        return self.parse_table(markdown_string)

    def detect_duplicates(self, _dataframes):
        unique_dict = {}
        for table_name, df in _dataframes:
            unique_elements = set(df["Element(Structure/Array/Value)"])
            unique_dict[table_name] = unique_elements

        _duplicates = []
        table_names = list(unique_dict.keys())
        for i in range(len(table_names)):
            for j in range(i + 1, len(table_names)):
                intersection = unique_dict[table_names[i]].intersection(
                    unique_dict[table_names[j]]
                )
                if intersection:
                    _duplicates.append(
                        [table_names[i], table_names[j], list(intersection)]
                    )
        return _duplicates

    def create_duplicate_indexed_dataframe(self, duplicates):
        duplicate_dict = {}
        for duplicate in duplicates:
            for element in duplicate[2]:
                if element not in duplicate_dict:
                    duplicate_dict[element] = [duplicate[0], duplicate[1]]
                else:
                    duplicate_dict[element].extend([duplicate[0], duplicate[1]])

        duplicate_df = pd.DataFrame(
            {
                "Element": duplicate_dict.keys(),
                "Columns": [list(set(columns)) for columns in duplicate_dict.values()],
            }
        )
        return duplicate_df

    def check_markdown_file(self, file_name):
        dataframes = self.read_markdown_file(file_name)
        duplicates = self.detect_duplicates(dataframes)
        duplicated_indexed_dataframe = self.create_duplicate_indexed_dataframe(
            duplicates
        )
        return duplicated_indexed_dataframe


class YamlProcessor:
    def read_yaml_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            yaml_dict = yaml.load(f, Loader=yaml.FullLoader)
        return yaml_dict


class ExcelConverter:
    def __init__(self):
        self.result = pd.DataFrame()

    def add_underscore_if_startswith_digit(self, element):
        return "_" + element if element[0].isdigit() else element

    def preprocess_dataframes_part_struct(self, dataframes_part_struct):
        for df in dataframes_part_struct:
            df.loc[:, "Element(Structure/Array/Value)"] = df[
                "Element(Structure/Array/Value)"
            ].apply(self.add_underscore_if_startswith_digit)

        return dataframes_part_struct

    def traverse_value(self, dataframes_part_value, yaml_dict_values):
        all_rows = []
        # 如果yaml_dict_values为空，则不需要遍历
        if not yaml_dict_values:
            return pd.DataFrame(all_rows)

        for df in dataframes_part_value:
            for i, row in df.iterrows():
                element = row["Element(Structure/Array/Value)"]
                if element in yaml_dict_values.keys():
                    info = yaml_dict_values[element]
                    new_row = {
                        "Sender /Server": row["Sender /Server"],
                        "Receiver /Client": row["Receiver /Client"],
                        "S_Trigger": row["S_Trigger"],
                        "R_Trigger": row["R_Trigger"],
                        "Port type": row["Port type"],
                        "Element(Structure/Array/Value)": element,
                        "Signal description": info.get("description", ""),
                        "Data type": "Value",
                        "Signal": "",
                        "Base Type": info.get("type", ""),
                        "DLC": "",
                        "Initial value": str(info.get("value", "")),
                    }
                    # 如果存在Queued列，则将其加入到new_row中, 不存在则设置为0
                    if "Queued" in row:
                        new_row["Queued"] = row["Queued"]
                    else:
                        new_row["Queued"] = 0

                    all_rows.append(new_row)
        return pd.DataFrame(all_rows)

    def expand_element(
        self,
        element,
        row,
        yaml_dict_structs,
        yaml_dict_arrays,
        all_rows,
        is_referenced=False,
    ):
        if element in yaml_dict_structs:
            # If the element is a structure, recursively expand it
            self.expand_struct(
                element,
                row,
                yaml_dict_structs,
                yaml_dict_arrays,
                all_rows,
                is_referenced,
            )
        elif element in yaml_dict_arrays:
            # If the element is an array, recurse into expand_array
            self.expand_array(
                element,
                row,
                yaml_dict_arrays,
                yaml_dict_structs,
                all_rows,
                is_referenced,
            )

    def expand_struct(
        self,
        struct_name,
        row,
        yaml_dict_structs,
        yaml_dict_arrays,
        all_rows,
        is_referenced=False,
    ):
        struct_info = yaml_dict_structs[struct_name]

        for signal, info in struct_info.items():
            ref = info.get("ref", "")

            sender_server = "" if is_referenced else row["Sender /Server"]
            receiver_client = "" if is_referenced else row["Receiver /Client"]
            s_trigger = "" if is_referenced else row["S_Trigger"]
            r_trigger = "" if is_referenced else row["R_Trigger"]
            port_type = row["Port type"]

            new_row = {
                "Sender /Server": sender_server,
                "Receiver /Client": receiver_client,
                "S_Trigger": s_trigger,
                "R_Trigger": r_trigger,
                "Port type": port_type,
                "Element(Structure/Array/Value)": struct_name,
                "Signal": signal,
                "Data type": "Structure",
                "Signal description": info.get("description", ""),
                "Base Type": info.get("type", ref),
                "DLC": info.get("size", ""),
                "Initial value": str(info.get("value", "")),
            }

            # 如果存在Queued列，则将其加入到new_row中, 不存在则设置为0
            if "Queued" in row:
                new_row["Queued"] = row["Queued"]
            else:
                new_row["Queued"] = 0
            if ref:
                # If there's a reference, expand that element (structure or array)
                self.expand_element(
                    ref,
                    new_row,
                    yaml_dict_structs,
                    yaml_dict_arrays,
                    all_rows,
                    True,
                )

            all_rows.append(new_row)

    def expand_array(
        self,
        array_name,
        row,
        yaml_dict_arrays,
        yaml_dict_structs,
        all_rows,
        is_referenced=False,
    ):
        array_info = yaml_dict_arrays[array_name]
        ref = array_info.get("ref", "")
        size = array_info.get("size", "")

        sender_server = "" if is_referenced else row["Sender /Server"]
        receiver_client = "" if is_referenced else row["Receiver /Client"]
        s_trigger = "" if is_referenced else row["S_Trigger"]
        r_trigger = "" if is_referenced else row["R_Trigger"]
        port_type = row["Port type"]

        base_type = array_info.get("type", "")  # Default base type from array_info
        # 如果Array引用了Struct，则base_type应该是Struct的类型名
        if ref and ref in yaml_dict_structs:
            struct_type_name = ref  # 此处设置Struct的类型名，假设yaml文件中struct的key就是其类型名
            base_type = struct_type_name

        # 如果Array引用了Array，则base_type应该是Array的类型名 FIX:2023-12-11 14:30:05
        if ref and ref in yaml_dict_arrays:
            array_type_name = ref
            base_type = array_type_name

        # Create a row for the array itself
        new_row = {
            "Sender /Server": sender_server,
            "Receiver /Client": receiver_client,
            "S_Trigger": s_trigger,
            "R_Trigger": r_trigger,
            "Port type": port_type,
            "Element(Structure/Array/Value)": array_name,
            "Signal": "",
            "Data type": "Array",
            "Signal description": array_info.get("description", ""),
            "Base Type": base_type,
            "DLC": size,
            "Initial value": str(array_info.get("value", "")),
        }

        # 如果存在Queued列，则将其加入到new_row中, 不存在则设置为0
        if "Queued" in row:
            new_row["Queued"] = row["Queued"]
        else:
            new_row["Queued"] = 0

        all_rows.append(new_row)

        if ref:
            # If the array references another structure or array, expand that element
            self.expand_element(
                ref,
                new_row,
                yaml_dict_structs,
                yaml_dict_arrays,
                all_rows,
                True,
            )

    def traverse_array_and_struct(
        self, dataframes_part, yaml_dict_structs, yaml_dict_arrays
    ):
        all_rows = []
        for df in dataframes_part:
            for i, row in df.iterrows():
                element = row["Element(Structure/Array/Value)"]
                if row["Data type"] == "Array":
                    self.expand_array(
                        element, row, yaml_dict_arrays, yaml_dict_structs, all_rows
                    )
                elif row["Data type"] == "Structure":
                    self.expand_struct(
                        element, row, yaml_dict_structs, yaml_dict_arrays, all_rows
                    )
        return pd.DataFrame(all_rows)

    def generate_excel(
        self, markdown_processor, yaml_processor, markdown_file, yaml_file, output_file
    ):
        yaml_dict = yaml_processor.read_yaml_file(yaml_file)
        yaml_dict_values = yaml_dict.get("Values", {})  # 防止yaml_dict中没有Values这个key
        yaml_dict_arrays = yaml_dict.get("Arrays", {})
        yaml_dict_structs = yaml_dict.get("Structs", {})
        if not yaml_dict_values:
            yaml_dict_values = {}
        if not yaml_dict_arrays:
            yaml_dict_arrays = {}
        if not yaml_dict_structs:
            yaml_dict_structs = {}

        dataframes = markdown_processor.read_markdown_file(markdown_file)
        dataframes_part = [df[1] for df in dataframes]
        dataframes_part_value = [
            df[df["Data type"] == "Value"] for df in dataframes_part
        ]
        dataframes_part_array = [
            df[df["Data type"] == "Array"] for df in dataframes_part
        ]
        dataframes_part_struct = [
            df[df["Data type"] == "Structure"] for df in dataframes_part
        ]

        dataframes_part_struct = self.preprocess_dataframes_part_struct(
            dataframes_part_struct
        )

        value_result = self.traverse_value(dataframes_part_value, yaml_dict_values)
        dataframes_part_combined = dataframes_part_array + dataframes_part_struct
        array_and_struct_result = self.traverse_array_and_struct(
            dataframes_part_combined, yaml_dict_structs, yaml_dict_arrays
        )

        final_result = pd.concat(
            [value_result, array_and_struct_result], ignore_index=True
        )
        rows_with_empty_first_column = final_result[
            final_result["Sender /Server"].isnull()
            | (final_result["Sender /Server"] == "")
        ]
        rows_with_nonempty_first_column = final_result.drop(
            rows_with_empty_first_column.index
        )

        self.result = pd.concat(
            [rows_with_nonempty_first_column, rows_with_empty_first_column],
            ignore_index=True,
        )
        self.generate_additional_columns()
        self.clean_up_rows_with_empty_first_column()
        self.rearrange_columns()

        self.result.to_excel(output_file, index=False)

    def generate_additional_columns(self):
        # Remove leading underscores from the "Element(Structure/Array/Value)" column
        self.result.loc[
            self.result["Element(Structure/Array/Value)"].str.startswith("_"),
            "Element(Structure/Array/Value)",
        ] = self.result.loc[
            self.result["Element(Structure/Array/Value)"].str.startswith("_"),
            "Element(Structure/Array/Value)",
        ].str[
            1:
        ]

        # Define lambda functions for reuse in generating column values based on conditions
        def generate_properties_name(row):
            if row["Sender /Server"] == "":
                return ""
            return "Pp_{}2{}_{}".format(
                row["Sender /Server"],
                row["Receiver /Client"],
                row["Element(Structure/Array/Value)"],
            )

        def generate_interface_name(row):
            if row["Sender /Server"] == "":
                return ""
            return "Pi_M_{}".format(row["Element(Structure/Array/Value)"])

        def generate_element_name(row):
            return "{}".format(row["Element(Structure/Array/Value)"])

        def generate_data_name(row):
            return "IdtM_{}".format(row["Element(Structure/Array/Value)"])

        def generate_sender_client_runnable_name(row):
            if row["Sender /Server"] == "":
                return ""
            return "R_M_{}_{}".format(row["Sender /Server"], row["S_Trigger"])

        def generate_receiver_server_runnable_name(row):
            if row["Receiver /Client"] == "":
                return ""
            return "R_M_{}_{}".format(row["Receiver /Client"], row["R_Trigger"])

        self.result["Properties name"] = self.result.apply(
            generate_properties_name, axis=1
        )
        self.result["Interface name"] = self.result.apply(
            generate_interface_name, axis=1
        )
        self.result["Element name"] = self.result.apply(generate_element_name, axis=1)
        self.result["Data name"] = self.result.apply(generate_data_name, axis=1)
        self.result["Sender/Client Runnable Name"] = self.result.apply(
            generate_sender_client_runnable_name, axis=1
        )
        self.result["Receiver/Server Runnable Name"] = self.result.apply(
            generate_receiver_server_runnable_name, axis=1
        )

        # TODO: 实现以下功能 2023-12-14 14:23:30
        # 实现一个函数, 扫描当前的Properties name列, 如果发送方相同, 接收方不同,
        # 且发送的Element(Structure/Array/Value)相同,
        # 则将名称改为Pp_{Sender /Server}2{GeneralSwC}_{Element(Structure/Array/Value)}
        def update_properties_name(self):
            # Group by 'Sender /Server' and 'Element(Structure/Array/Value)' and filter groups with more than one unique 'Receiver /Client'
            grouped = self.result.groupby(
                ["Sender /Server", "Element(Structure/Array/Value)"]
            )
            for (sender, element), group in grouped:
                if len(group["Receiver /Client"].unique()) > 1:
                    for index in group.index:
                        self.result.at[
                            index, "Properties name"
                        ] = f"Pp_{sender}2GeneralSwC_{element}"

        update_properties_name(self)

    def clean_up_rows_with_empty_first_column(self):
        self.result.fillna({"Sender /Server": "", "Receiver /Client": ""}, inplace=True)

        # 再对这些第一列为空字符串的行进行去重
        result_with_empty_first_column = self.result[
            self.result["Sender /Server"] == ""
        ]
        result_with_nonempty_first_column = self.result[
            self.result["Sender /Server"] != ""
        ]
        self.result = pd.concat(
            [
                result_with_nonempty_first_column,
                result_with_empty_first_column.drop_duplicates(),
            ],
            ignore_index=True,
        )

    def rearrange_columns(self):
        columns_order = [
            "Sender /Server",
            "Receiver /Client",
            "S_Trigger",
            "R_Trigger",
            "Port type",
            "Queued",  # FIX: 2024-1-15 15:23:43
            "Element(Structure/Array/Value)",
            "Signal description",
            "Data type",
            "Signal",
            "Base Type",
            "DLC",
            "Initial value",
            "Properties name",
            "Interface name",
            "Element name",
            "Data name",
            "Sender/Client Runnable Name",
            "Receiver/Server Runnable Name",
        ]
        self.result = self.result[columns_order]

    def print_excel_info(self):
        print("The following information has been written to the Excel file:")
        print(f"Number of rows:    {len(self.result)}")
        print(f"Number of columns: {len(self.result.columns)}")
        value_shape = (
            self.result[self.result["Data type"] == "Value"][
                "Element(Structure/Array/Value)"
            ]
            .unique()
            .shape[0]
        )
        array_shape = (
            self.result[self.result["Data type"] == "Array"][
                "Element(Structure/Array/Value)"
            ]
            .unique()
            .shape[0]
        )
        struct_shape = (
            self.result[self.result["Data type"] == "Structure"][
                "Element(Structure/Array/Value)"
            ]
            .unique()
            .shape[0]
        )
        print(f"Number of values:  {value_shape}")
        print(f"Number of arrays:  {array_shape}")
        print(f"Number of structs: {struct_shape}")
        print(
            f"Number of implementation data types: {value_shape + array_shape + struct_shape}"
        )


class Application:  #
    @staticmethod
    def run(wait_for_input=True):
        markdown_processor = MarkdownTableProcessor()
        yaml_processor = YamlProcessor()
        excel_converter = ExcelConverter()

        # Global variables defined here
        markdown_file = "../../1.Mf_Maf/Mf_CP_Graph.md"
        yaml_file = "../../1.Mf_Maf/Maf_CP_interface.yaml"
        output_file = "../../2.Maf_InterfaceExcel/swc.xlsx"

        # check if directory exists, if not, create it
        if not os.path.exists(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))

        excel_converter.generate_excel(
            markdown_processor, yaml_processor, markdown_file, yaml_file, output_file
        )
        excel_converter.print_excel_info()

        if wait_for_input:
            input(
                "Excel file has been generated and saved to {}, press any key to exit...".format(
                    output_file
                )
            )


# Run the application with a boolean indicating whether to wait for user input
Application.run(wait_for_input=True)
