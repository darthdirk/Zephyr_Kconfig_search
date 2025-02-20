This script allows you to search for specific parameters within Kconfig-related files in a Zephyr RTOS project directory. It scans .conf and .sysbuild files for a given keyword and displays matching lines with surrounding context. The idea for this script is to easily identify related .conf and .sysbuild files for examples to pick from.

Features

Scans Only Kconfig-related Files: The search is restricted to .conf and .sysbuild files.

Case-Insensitive Matching: Finds terms like UART, uart, Uart.

Contextual Results: Displays 2 lines before and after each match.

Relative Path Support: The script dynamically resolves the Zephyr base directory using ~/ncs/v2.7.0/.

Requirements

Python 3.x

A Zephyr project located at ~/ncs/v2.7.0/ (modify if necessary)

Installation

No external dependencies are required. Ensure Python is installed, then clone or copy the script to your workspace.

Usage

Run the script from a terminal:

python search_example.py

Step-by-Step Execution

The script will print all environment variables (useful for debugging).

It prompts you to enter the parameter you want to search for.

The script recursively scans ~/ncs/v2.7.0/ for occurrences of the parameter.

If matches are found, they will be displayed with:

File path

Line number

Context (2 lines before and after the match)

Example Output

Enter the parameter to search for: UART

Scanning file: /home/user/ncs/v2.7.0/zephyr/Kconfig
Scanning file: /home/user/ncs/v2.7.0/modules/Kconfig

Found 'UART' in the following locations:

File: /home/user/ncs/v2.7.0/zephyr/samples/subsys/zbus/uart_bridge/boards/hifive1_fe310_B.conf (Line 2)
Context:
CONFIG_UART_INTERRUPT_DRIVEN=y
CONFIG_UART_SIFIVE_PORT_1=y
CONFIG_UART_SIFIVE_PORT_1_TXCNT_IRQ=1
CONFIG_UART_SIFIVE_PORT_1_RXCNT_IRQ=1
----------------------------------------


Troubleshooting

No Matches Found

Ensure that the parameter exists in Kconfig-related files:

grep -ri "UART" ~/ncs/v2.7.0/ --include=.conf --include=.sysbuild

Verify that the zephyr_base_dir path is correct.

Try different case variations (uart, UART, Uart).

Script Doesn’t Run

Ensure Python 3 is installed (python3 --version).

Make the script executable:

chmod +x search_example.py

Run with:

python3 search_example.py

Modifications

Change the Zephyr Base Directory

Modify the following line in the script:

zephyr_base_dir = os.path.abspath(os.path.expanduser("~/ncs/v2.7.0/"))

Change ~/ncs/v2.7.0/ to match your Zephyr workspace.