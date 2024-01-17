import os
import time
import shutil
import venv
import subprocess
import concurrent.futures
import logging
from pathlib import Path

# Initialize the logger
logging.basicConfig(level=logging.INFO)


# Create a virtual environment
def create_venv(venv_path):
    logging.info("Creating virtual environment...")
    start_time = time.time()
    venv.create(venv_path, with_pip=True)
    end_time = time.time()
    logging.info(f"Virtual environment created in {end_time - start_time} seconds.")


# Install necessary packages into the venv
def install_packages(packages):
    start_time = time.time()
    result = subprocess.call(
        ["venv/bin/pip" if os.name != "nt" else "venv/Scripts/pip", "install"]
        + packages
    )

    # Check installation success
    if result != 0:
        logging.error(f"Error occurred while installing packages: {result}")
        return False

    end_time = time.time()
    logging.info(f"Packages installed in {end_time - start_time} seconds.")
    return True


# Check if necessary tools are available in venv
def check_tools_in_venv(tool):
    tool_path = f"venv/bin/{tool}" if os.name != "nt" else f"venv/Scripts/{tool}.exe"
    if not Path(tool_path).exists():
        logging.error(
            f"{tool} not found in virtual environment. Please check the package installation."
        )
        return False
    return True


# Compile a Python script
def compile_script(script_name):
    start_time = time.time()
    result = subprocess.call(
        [
            f"venv/bin/pyinstaller" if os.name != "nt" else "venv/Scripts/pyinstaller",
            "--onefile",
            f"{script_name}.py",
        ]
    )

    if result != 0:
        logging.error(f"Error occurred while executing command: {result}")
        return None

    elapsed_time = time.time() - start_time
    logging.info(f"Compiled {script_name} in {elapsed_time} seconds.")
    return script_name


# Copy executables to current directory
def copy_exe(future):
    script = future.result()
    if script:
        shutil.copy(f"dist/{script}.exe", ".")
        exe_size = Path(f"{script}.exe").stat().st_size
        logging.info(f"Copied {script}.exe ({exe_size / 1024 / 1024:.2f} MB)")


# Delete a directory
def delete_dir(dir_path):
    shutil.rmtree(dir_path, ignore_errors=True)
    logging.info(f"Deleted directory {dir_path}")


# Delete a file
def delete_file(file_path):
    file_path = Path(file_path)
    if file_path.exists():
        file_path.unlink()
        logging.info(f"Deleted file {file_path}")


# Remove the venv
def remove_venv(venv_path):
    start_time = time.time()
    shutil.rmtree(venv_path, ignore_errors=True)
    elapsed_time = time.time() - start_time
    logging.info(f"Removed virtual environment in {elapsed_time} seconds.")


if __name__ == "__main__":
    # Define scripts, packages, and directories
    scripts = ["md_yaml_check", "md_yaml_to_excel"]
    packages = ["pandas", "pyyaml", "numpy", "pyinstaller", "openpyxl"]
    dirs_to_delete = ["build", "dist", "venv"]
    files_to_delete = ["md_yaml_check.spec", "md_yaml_to_excel.spec"]

    # Create venv
    create_venv("venv")

    # Install packages
    if not install_packages(packages):
        exit(1)

    # Check if necessary tools are available in venv
    if not check_tools_in_venv("pyinstaller"):
        exit(1)

    # Compile scripts in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(compile_script, script) for script in scripts]
        for future in futures:
            future.add_done_callback(copy_exe)

    # Delete directories and files
    for dir_path in dirs_to_delete:
        delete_dir(dir_path)

    for file_path in files_to_delete:
        delete_file(file_path)

    remove_venv("venv")
