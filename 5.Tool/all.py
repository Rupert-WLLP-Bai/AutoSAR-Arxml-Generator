# /*
#  * @Author: junhao.bai
#  * @Date: 2023-11-28
#  * @Last Modified by:   junhao.bai
#  * @Last Modified time: 2024-1-15 16:19:14
#  */


import os
import subprocess
import time


def execute_command(command, workdir=None):
    cwd = os.getcwd()  # Store the current working directory
    if workdir:
        os.chdir(workdir)  # Change the directory

    print(f"Executing: {command}\n{'='*20}")
    start_time = time.time()

    process = subprocess.Popen(command, shell=True)
    process.wait()

    end_time = time.time()
    elapsed_time = end_time - start_time

    os.chdir(cwd)  # Change back to the original directory
    return elapsed_time


def main(timing=False):
    total_start_time = time.time()
    step1_time = execute_command("python md_yaml_check.py", "InterfaceArxml")
    step2_time = execute_command("python md_yaml_to_excel.py", "InterfaceArxml")
    step3_time = execute_command(
        "python port_interface_data_types_process_sr.py", "Excel2Arxml"
    )
    step4_time = execute_command(
        "python port_interface_data_types_process_cs.py", "Excel2Arxml"
    )
    step5_time = execute_command("python component_gen.py", "Excel2Arxml")

    total_end_time = time.time()
    total_elapsed_time = total_end_time - total_start_time

    # Print out the execution times
    if timing:
        print("=" * 20)
        print(f"\nTotal Time Elapsed: {total_elapsed_time:.3f} seconds")
        print(f"Step 1 Time: {step1_time:.3f} seconds")
        print(f"Step 2 Time: {step2_time:.3f} seconds")
        print(f"Step 3 Time: {step3_time:.3f} seconds")
        print(f"Step 4 Time: {step4_time:.3f} seconds")
        print(f"Step 5 Time: {step5_time:.3f} seconds")


if __name__ == "__main__":
    main(timing=False)
