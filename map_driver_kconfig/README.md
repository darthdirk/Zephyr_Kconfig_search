Overview

This script searches for a user-specified Kconfig parameter within the Zephyr project directory and maps it to corresponding driver source files. The script performs the following steps:

Prompts the user for a Kconfig parameter.

Searches Kconfig files to verify if the parameter exists.

If found, scans driver source files (.c and .h) for references to the parameter.

Outputs the mapping results to a file named driver_mappings.txt.

Prerequisites

Ensure you have the following:

Python 3 installed

Access to a Zephyr source directory

Proper permissions to read files within the Zephyr project

Usage

Run the script:

python map_driver.py

Enter the Kconfig parameter when prompted.

If the parameter exists, the script will scan driver files and generate driver_mappings.txt with the results.

Output

The script generates a driver_mappings.txt file containing:

The searched Kconfig parameter

List of source files referencing the parameter (if any)

Customization

Modify the zephyr_base_dir variable in the script to point to the correct Zephyr source directory:

zephyr_base_dir = "/path/to/zephyr/"

Example Output

Kconfig Parameter: CONFIG_MY_DRIVER
Referenced in files:
  /home/user/zephyr/drivers/sensor/my_sensor.c
  /home/user/zephyr/drivers/sensor/my_sensor.h
----------------------------------------

Troubleshooting

If the script does not find the parameter, ensure it is correctly spelled and present in the Kconfig files.

If no references are found, check whether the parameter is actually used in the driver source code.

