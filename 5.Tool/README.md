# requirements

1. python3.10+ 
   - autosar部分有使用python3.10的Union 参考[PEP 604 – Allow writing union types as X | Y](https://peps.python.org/pep-0604/)
  
2. pandas, pyyaml, lxml, openpyxl

    ``` shell
    pip install pandas pyyaml lxml openpyxl
    ```
3. 执行`all.py`, 生成的结果是`result_component_new.arxml`