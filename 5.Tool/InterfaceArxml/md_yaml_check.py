# author: Junhao Bai
# date: 2023-11-30 17:19:34
# version: 1.0.2
# change log:
# 1.0.1: refractor the code by group the functions into classes
# 1.0.1 - fix 2023/11/30 修改了global variables中md和yaml文件的路径
# 1.0.2 2023/11/30 检查了数组引用结构体的情况, 将这些结果从结果列表中移除

# required packages
# pyyaml: pip install pyyaml
# pandas: pip install pandas

import re
import sys
import pandas as pd
import yaml
from typing import List, Dict, Tuple, Any

# global variables:
markdown_file = "../../1.Mf_Maf/Mf_CP_Graph.md"
yaml_file = "../../1.Mf_Maf/Maf_CP_interface.yaml"
basic_types = [
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


# define the class of processing the markdown file
class MarkdownChecker:
    """
    This class is used to check the markdown file
    """

    def __init__(self, file_path):
        """
        Constructor of the class
        """
        self.file_path = file_path
        self.dataframes = self._read_markdown_file(file_path)
        self.dataframes_part = [df[1] for df in self.dataframes]
        self.dataframes_part = [
            df[["Element(Structure/Array/Value)", "Data type"]]
            for df in self.dataframes_part
        ]
        self.dataframes_part_value = [
            df[df["Data type"] == "Value"] for df in self.dataframes_part
        ]
        self.dataframes_part_array = [
            df[df["Data type"] == "Array"] for df in self.dataframes_part
        ]
        self.dataframes_part_struct = [
            df[df["Data type"] == "Structure"] for df in self.dataframes_part
        ]

        self.valid = True

    def _parse_table(self, markdown_str: str) -> List[Tuple[str, pd.DataFrame]]:
        """
        Parse the markdown string to dataframe
        """
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
            df = pd.DataFrame(rows[1:], columns=rows[0])
            _dataframes.append([table_name, df])
        return _dataframes

    def count_table_rows(self) -> int:
        """
        统计markdown文件中的总行数, 表示之后会生成多少个Port Interface
        """
        total_rows = 0
        for _, df in self.dataframes:
            total_rows += len(df)
        return total_rows

    def _read_markdown_file(self, file_path: str) -> List[Tuple[str, pd.DataFrame]]:
        """
        Read the markdown file
        """
        with open(file_path, "r", encoding="utf-8") as f:
            markdown_str = f.read()
        return self._parse_table(markdown_str)

    def _find_duplicates(self) -> List[List[str]]:
        """
        Find the duplicated elements in the markdown file
        """
        unique_dict = {}
        for table_name, df in self.dataframes:
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

    def _create_dataframe(self, duplicates: List[List[str]]) -> pd.DataFrame:
        # Create an empty dictionary to store the elements and their corresponding columns
        duplicate_dict = {}

        for duplicate in duplicates:
            # For each entry in duplicates, iterate over the duplicate elements
            for element in duplicate[2]:
                if element not in duplicate_dict:
                    # If this is the first occurrence of the element, add it to the dictionary with its corresponding columns
                    duplicate_dict[element] = [duplicate[0], duplicate[1]]
                else:
                    # If the element already exists in the dictionary, append the new columns to the existing list
                    duplicate_dict[element].extend([duplicate[0], duplicate[1]])

        # Remove duplicates from each list under 'Columns' and convert dictionary to a DataFrame
        duplicate_df = pd.DataFrame(
            {
                "Element": duplicate_dict.keys(),
                "Columns": [list(set(columns)) for columns in duplicate_dict.values()],
            }
        )

        return duplicate_df

    def _check_duplicates(self) -> pd.DataFrame:
        """
        Check the duplicates in the markdown file
        """
        duplicates = self._find_duplicates()
        duplicated_df = self._create_dataframe(duplicates)
        # Markdown中的重复不影响, 只报Warning
        return duplicated_df

    def generate_report(self) -> None:
        """
        Generate the report of the markdown file
        """
        print(
            "*********************** PART 1: CHECK DUPLICATED ELEMENTS IN MARKDOWN FILE ***********************"
        )
        duplicated_df = self._check_duplicates()
        if len(duplicated_df) == 0:
            print(
                "[SUCCESS] markdown file check passed, no duplicated elements in different tables"
            )
        else:
            print("[WARNING] some elements are duplicated in different tables ")
            print(duplicated_df)
        print(
            "***************************************** END OF PART 1 *****************************************"
        )
        print("\n")


class YamlChecker:
    """
    This class is used to check the yaml file
    """

    def __init__(self, file_path: str):
        """
        Constructor of the class
        """
        self.file_path = file_path
        self.yaml_content = self._read_yaml_file(file_path)
        self.yaml_dict_values = self.yaml_content["Values"]
        self.yaml_dict_arrays = self.yaml_content["Arrays"]
        self.yaml_dict_structs = self.yaml_content["Structs"]
        self.valid = True

    def count_yaml_data_types(yaml_checker) -> Tuple[int, int, int, int]:
        """
        Count the number of data types in the YAML file
        """
        num_values = 0
        num_arrays = 0
        num_structs = 0
        # 如果yaml_dict_values为None, 则直接返回0
        if yaml_checker.yaml_dict_values is None:
            num_values = 0
        else:
            num_values = len(yaml_checker.yaml_dict_values)
        if yaml_checker.yaml_dict_arrays is None:
            num_arrays = 0
        else:
            num_arrays = len(yaml_checker.yaml_dict_arrays)
        if yaml_checker.yaml_dict_structs is None:
            num_structs = 0
        else:
            num_structs = len(yaml_checker.yaml_dict_structs)
        total = num_values + num_arrays + num_structs
        return num_values, num_arrays, num_structs, total

    def _read_yaml_file(self, file_path: str) -> Dict[str, Any]:
        """
        Read the yaml file
        """
        with open(file_path, "r", encoding="utf-8") as f:
            yaml_dict = yaml.load(f, Loader=yaml.FullLoader)
        return yaml_dict

    def _check_yaml_refs(self) -> List[str]:
        # 创建一个包含所有structs和arrays的键的集合
        defined_keys = set()
        # 首先判断yaml_dict_structs和yaml_dict_arrays是否为None
        if self.yaml_dict_structs is None:
            if self.yaml_dict_arrays is None:
                return []
            else:
                defined_keys = set(self.yaml_dict_arrays.keys())
        elif self.yaml_dict_arrays is None:
            defined_keys = set(self.yaml_dict_structs.keys())
        else:
            defined_keys = set(self.yaml_dict_structs.keys()).union(
                set(self.yaml_dict_arrays.keys())
            )

        errors = []
        # 遍历每个struct中的每个value
        for struct_name, struct in self.yaml_dict_structs.items():
            for value in struct.values():
                # 如果存在'ref'并且它指向的key未被定义，那么记录错误
                if "ref" in value and value["ref"] not in defined_keys:
                    # 输出错误的ref和struct的名称
                    errors.append(
                        f"Undefined ref {value['ref']} in struct {struct_name}"
                    )
        return errors

    def _check_value_type(self) -> List[str]:
        # 错误信息列表
        errors = []
        # 遍历每个value

        # 遍历之前先判断yaml_dict_values是否为None
        if self.yaml_dict_values is None:
            return errors

        for key, value in self.yaml_dict_values.items():
            # 首先检查type是否存在
            if "type" not in value.keys():
                errors.append(f"Type is not defined for variable {key}")
            if value["type"] not in basic_types:
                errors.append(f"Invalid type {value['type']} for variable {key}")
        return errors

    def _check_array_type(self) -> List[str]:
        # 错误信息列表
        errors = []

        # 遍历之前先判断yaml_dict_arrays是否为None
        if self.yaml_dict_arrays is None:
            return errors

        # 遍历每个array
        for key, value in self.yaml_dict_arrays.items():
            # 可能不存在type，所以需要判断一下
            if "type" not in value.keys() and "ref" not in value.keys():
                errors.append(
                    f"Type is not defined for array {key}, and ref is not defined"
                )
                continue
            # 可能不存在size，所以需要判断一下
            if "size" not in value.keys():
                errors.append(f"Size is not defined for array {key}")
                continue
            # 如果存在size, size必须为1~2000之间的整数, 且不能为NoneType
            elif value["size"] is None:
                errors.append(f"Size is not defined for array {key}")
            elif not isinstance(value["size"], int):
                errors.append(
                    f"Invalid size {value['size']} for array {key}, size must be an integer between 1 and 2000"
                )
            elif value["size"] is not None and (
                value["size"] < 1 or value["size"] > 2000
            ):
                errors.append(
                    f"Invalid size {value['size']} for array {key}, size must be between 1 and 2000"
                )
            # If the array has a 'type', check it's a basic type or a valid ref
            if "type" in value and value["type"] not in basic_types:
                # Here's the new logic: if it's not a basic type, it might be a ref.
                if "ref" in value and value["ref"] in self.yaml_dict_structs.keys():
                    # If it's a valid ref, everything is fine.
                    continue
                else:
                    # If it's neither a basic type nor a valid ref, it's an error.
                    errors.append(f"Invalid type {value['type']} for array {key}")

            # Check if the array has a 'ref' that doesn't correspond to a defined struct or array
            if (
                "ref" in value
                and value["ref"] not in self.yaml_dict_structs.keys()
                and value["ref"] not in self.yaml_dict_arrays.keys()
            ):
                errors.append(f"Array {key} has undefined ref {value['ref']}")
        return errors

    def _check_struct_type(self) -> List[str]:
        # 错误信息列表
        errors = []

        # 遍历之前先判断yaml_dict_structs是否为None
        if self.yaml_dict_structs is None:
            return errors

        # 遍历每个struct
        for key, value in self.yaml_dict_structs.items():
            for k, v in value.items():
                # 如果v为None，输出key和value, raise error
                if v == None:
                    print("key: ", key)
                    print("value: ", value)
                    raise Exception("Value of {} is None".format(key))
                # 如果v['type']不存在(可能直接key error)，则检查v['ref']是否存在, 如果v['ref']不存在, 记录错误
                if "type" not in v.keys():
                    if "ref" not in v.keys():
                        errors.append(
                            f"Type is not defined for element {k} in struct {key}"
                        )
                    # 如果ref存在，则跳过这个循环
                    continue
                # 如果v['type']不为None，检查v['type']是否在basic_types中
                if v is not None and v["type"] not in basic_types:
                    errors.append(
                        f"Invalid type {v['type']} for element {k} in struct {key}"
                    )
        return errors

    def generate_report(self) -> None:
        self.check_types()

    def check_types(self) -> None:
        """
        Check the types in the yaml file
        """
        print(
            "******************************** PART 2 CHECK Types in YAML FILE ********************************"
        )
        print(
            "************************** PART 2.1: CHECK Type of Values in YAML FILE **************************"
        )
        value_errors = self._check_value_type()
        if len(value_errors) == 0:
            print("[SUCCESS] yaml file check passed, all values are valid")
        else:
            print("[ ERROR ] yaml file check failed, some values are invalid")
            print(value_errors)
            self.valid = False
        print(
            "**************************************** END OF PART 2.1 ****************************************"
        )
        print("\n")
        print(
            "************************** PART 2.2: CHECK Type of Arrays in YAML FILE **************************"
        )
        array_errors = self._check_array_type()
        if len(array_errors) == 0:
            print("[SUCCESS] yaml file check passed, all arrays are valid")
        else:
            print("[ ERROR ] yaml file check failed, some arrays are invalid")
            print(array_errors)
            self.valid = False
        print(
            "**************************************** END OF PART 2.2 ****************************************"
        )
        print("\n")
        print(
            "************************* PART 2.3: CHECK Type of Structs in YAML FILE **************************"
        )
        struct_errors = self._check_struct_type()
        if len(struct_errors) == 0:
            print("[SUCCESS] yaml file check passed, all structs are valid")
        else:
            print("[ ERROR ] yaml file check failed, some structs are invalid")
            print(struct_errors)
            self.valid = False
        print(
            "*************************************** END OF PART 2.3 ***************************************"
        )
        print("\n")
        print(
            "************************* PART 2.4: CHECK Refs of Structs in YAML FILE **************************"
        )
        struct_ref_errors = self._check_yaml_refs()
        if len(struct_ref_errors) == 0:
            print("[SUCCESS] yaml file check passed, all refs are valid")
        else:
            print("[ ERROR ] yaml file check failed, some refs are invalid")
            print(struct_ref_errors)
            self.valid = False
        print(
            "*************************************** END OF PART 2.4 ***************************************"
        )
        print(
            "**************************************** END OF PART 2 ****************************************"
        )
        print("\n")


class YamlMarkdownChecker:
    def __init__(self, markdown_checker: MarkdownChecker, yaml_checker: YamlChecker):
        self.markdown_checker = markdown_checker
        self.yaml_checker = yaml_checker
        self.valid = True

    # 检查Markdown中出现但在YAML值字典中未出现的元素
    def _check_value(self) -> List[str]:
        not_in_yaml_dict_values = []
        for df in self.markdown_checker.dataframes_part_value:
            for element in df["Element(Structure/Array/Value)"]:
                # 首先检查yaml_dict_values是否为None
                if self.yaml_checker.yaml_dict_values is None:
                    break
                if element not in self.yaml_checker.yaml_dict_values.keys():
                    not_in_yaml_dict_values.append(element)
        return not_in_yaml_dict_values

    # 检查Markdown中出现但在YAML数组字典中未出现的元素
    def _check_array(self) -> List[str]:
        not_in_yaml_dict_arrays = []
        for df in self.markdown_checker.dataframes_part_array:
            for element in df["Element(Structure/Array/Value)"]:
                # 首先检查yaml_dict_arrays是否为None
                if self.yaml_checker.yaml_dict_arrays is None:
                    break
                if element not in self.yaml_checker.yaml_dict_arrays.keys():
                    not_in_yaml_dict_arrays.append(element)
        return not_in_yaml_dict_arrays

    # 检查Markdown中出现但在YAML结构体字典中未出现的元素
    def _check_struct(self) -> List[str]:
        not_in_yaml_dict_structs = []
        for df in self.markdown_checker.dataframes_part_struct:
            for element in df["Element(Structure/Array/Value)"]:
                # 首先检查yaml_dict_structs是否为None
                if self.yaml_checker.yaml_dict_structs is None:
                    break
                if element not in self.yaml_checker.yaml_dict_structs.keys():
                    not_in_yaml_dict_structs.append(element)
        return not_in_yaml_dict_structs

    # 检查YAML值字典中出现但在Markdown数据帧中未出现的元素
    def _check_yaml_value(self) -> List[str]:
        not_in_dataframes_part_value = []
        elements_set = {
            element
            for df in self.markdown_checker.dataframes_part_value
            for element in df["Element(Structure/Array/Value)"]
        }

        # 遍历之前先判断yaml_dict_values是否为None
        if self.yaml_checker.yaml_dict_values is None:
            return not_in_dataframes_part_value

        # 遍历yaml_dict_values中的每个key
        for key in self.yaml_checker.yaml_dict_values.keys():
            if key not in elements_set:
                not_in_dataframes_part_value.append(key)

        return not_in_dataframes_part_value

    # 检查YAML数组字典中出现但在Markdown数据帧中未出现的元素
    def _check_yaml_array(self) -> List[str]:
        not_in_dataframes_part_array = []
        elements_set = {
            element
            for df in self.markdown_checker.dataframes_part_array
            for element in df["Element(Structure/Array/Value)"]
        }

        # 遍历之前先判断yaml_dict_arrays是否为None
        if self.yaml_checker.yaml_dict_arrays is None:
            return not_in_dataframes_part_array

        for key in self.yaml_checker.yaml_dict_arrays:
            if key not in elements_set:
                not_in_dataframes_part_array.append(key)

        # 检查结构体中是否有引用数组，如果有则从结果列表中移除
        for key, value in self.yaml_checker.yaml_dict_structs.items():
            for k, v in value.items():
                if (
                    v is not None
                    and "ref" in v
                    and v["ref"] in not_in_dataframes_part_array
                ):
                    not_in_dataframes_part_array.remove(v["ref"])

        # 检查数组中是否有引用其他数组，如果有则从结果列表中移除 FIX: 2023-12-11 14:22:10
        for key, value in self.yaml_checker.yaml_dict_arrays.items():
            if "ref" in value and value["ref"] in not_in_dataframes_part_array:
                not_in_dataframes_part_array.remove(value["ref"])

        return not_in_dataframes_part_array

    # 检查YAML结构体字典中出现但在Markdown数据帧中未出现的元素
    def _check_yaml_struct(self) -> List[str]:
        not_in_dataframes_part_struct = []
        elements_set = {
            element
            for df in self.markdown_checker.dataframes_part_struct
            for element in df["Element(Structure/Array/Value)"]
        }

        # 遍历之前先判断yaml_dict_structs是否为None
        if self.yaml_checker.yaml_dict_structs is None:
            return not_in_dataframes_part_struct

        for key in self.yaml_checker.yaml_dict_structs.keys():
            if key not in elements_set:
                not_in_dataframes_part_struct.append(key)

        # 检查结构体中是否有引用其他结构体，如果有则从结果列表中移除
        for key, value in self.yaml_checker.yaml_dict_structs.items():
            for k, v in value.items():
                if (
                    v is not None
                    and "ref" in v
                    and v["ref"] in not_in_dataframes_part_struct
                ):
                    not_in_dataframes_part_struct.remove(v["ref"])

        # 检查yaml_dict_arrays是否为None
        if self.yaml_checker.yaml_dict_arrays is None:
            return not_in_dataframes_part_struct

        # 检查数组中是否有引用结构体，如果有则从结果列表中移除  FIX: 2023-11-30 17:19:19
        for key, value in self.yaml_checker.yaml_dict_arrays.items():
            if "ref" in value and value["ref"] in not_in_dataframes_part_struct:
                not_in_dataframes_part_struct.remove(value["ref"])

        return not_in_dataframes_part_struct

    def generate_report(self) -> None:
        print(
            "******************** PART 3: CHECK ELEMENTS IN YAML FILE AND MARKDOWN FILE ********************"
        )
        print(
            "****************** PART 3.1: CHECK ELEMENTS IN YAML FILE BUT NOT IN MARKDOWN FILE *************"
        )
        not_in_dataframes_part_value = self._check_yaml_value()
        not_in_dataframes_part_array = self._check_yaml_array()
        not_in_dataframes_part_struct = self._check_yaml_struct()
        if (
            len(not_in_dataframes_part_value) == 0
            and len(not_in_dataframes_part_array) == 0
            and len(not_in_dataframes_part_struct) == 0
        ):
            print(
                "[SUCCESS] yaml file check passed, all elements in yaml file are in markdown file"
            )
        else:
            print(
                "[ ERROR ] yaml file check failed, some elements in yaml file are not in markdown file"
            )
            print("Elements in yaml file but not in markdown file: ")
            print("Values: ", not_in_dataframes_part_value)
            print("Arrays: ", not_in_dataframes_part_array)
            print("Structs: ", not_in_dataframes_part_struct)
            self.valid = False
        print(
            "**************************************** END OF PART 3.1 ****************************************"
        )
        print("\n")
        print(
            "**************** PART 3.2: CHECK ELEMENTS IN MARKDOWN FILE BUT NOT IN YAML FILE  ****************"
        )
        not_in_yaml_dict_values = self._check_value()
        not_in_yaml_dict_arrays = self._check_array()
        not_in_yaml_dict_structs = self._check_struct()
        if (
            len(not_in_yaml_dict_values) == 0
            and len(not_in_yaml_dict_arrays) == 0
            and len(not_in_yaml_dict_structs) == 0
        ):
            print(
                "[SUCCESS] yaml file check passed, all elements in markdown file are in yaml file"
            )
        else:
            print(
                "[ ERROR ] yaml file check failed, some elements in markdown file are not in yaml file"
            )
            print("Elements in markdown file but not in yaml file: ")
            print("Values: ", not_in_yaml_dict_values)
            print("Arrays: ", not_in_yaml_dict_arrays)
            print("Structs: ", not_in_yaml_dict_structs)
            self.valid = False
        print(
            "**************************************** END OF PART 3.2 ****************************************"
        )
        print(
            "**************************************** END OF PART 3 ****************************************"
        )
        print("\n")


def summary(markdown_checker, yaml_checker, yaml_markdown_checker) -> None:
    print(
        "**************************************** SUMMARY ****************************************"
    )

    check_results = {
        "markdown file": markdown_checker.valid,
        "yaml file": yaml_checker.valid,
        "yaml-markdown": yaml_markdown_checker.valid,
    }

    passed_checks = [name for name, valid in check_results.items() if valid]
    failed_checks = [name for name, valid in check_results.items() if not valid]

    if failed_checks:
        print("[ ERROR ] check failed for: " + ", ".join(failed_checks))
        print(
            "**************************************** SUMMARY ****************************************"
        )
        sys.exit(1) # 用于在CI中判断是否通过 FIX: 2023-12-18 11:24:55
        
    else:
        print("[SUCCESS] all checks passed")
        print(
            "**************************************** SUMMARY ****************************************"
        )
        sys.exit(0) # 用于在CI中判断是否通过 FIX: 2023-12-18 11:24:55
    

    # 输出总共有多少个接口和多少个数据类型, 便于之后检查是否对应
    # print(f"Total Interfaces in Markdown File: {markdown_checker.count_table_rows()}")
    # print(
    #     f"Total Values in YAML File: {YamlChecker.count_yaml_data_types(yaml_checker)[0]} \
    #     \nTotal Arrays in YAML File: {YamlChecker.count_yaml_data_types(yaml_checker)[1]} \
    #     \nTotal Structs in YAML File: {YamlChecker.count_yaml_data_types(yaml_checker)[2]} \
    #     \nTotal Data Types in YAML File: {YamlChecker.count_yaml_data_types(yaml_checker)[3]}"
    # )


if __name__ == "__main__":
    markdown_checker = MarkdownChecker(markdown_file)
    markdown_checker.generate_report()
    yaml_checker = YamlChecker(yaml_file)
    yaml_checker.generate_report()
    yaml_markdown_checker = YamlMarkdownChecker(markdown_checker, yaml_checker)
    yaml_markdown_checker.generate_report()
    summary(markdown_checker, yaml_checker, yaml_markdown_checker)
    # 等待用户确认
    input("Press any key to exit...")
