import os
import re

def print_environment_variables():
    """Print all environment variables for debugging."""
    print("\nEnvironment Variables:")
    for key, value in os.environ.items():
        print(f"{key}={value}")
    print("-" * 40)

def read_file_with_fallback(file_path):
    """
    Reads a file with UTF-8 encoding, falling back to binary if UTF-8 fails.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except UnicodeDecodeError:
        print(f"Warning: Failed to read {file_path} with UTF-8 encoding. Retrying in binary mode.")
        try:
            with open(file_path, 'rb') as f:
                return f.readlines()
        except Exception as e:
            print(f"Error reading file {file_path} in binary mode: {e}")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return None

def search_kconfig_for_param(base_dir, target_param):
    """
    Searches Kconfig files for a specific driver-related parameter.
    """
    found = False
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if "Kconfig" in file:
                file_path = os.path.join(root, file)
                lines = read_file_with_fallback(file_path)
                if lines:
                    for line in lines:
                        if re.match(rf'\s*config\s+{target_param}', line):
                            found = True
                            break
    return found

def map_kconfig_to_drivers(base_dir, target_param):
    """
    Maps a specific Kconfig parameter to source files in the drivers directory.
    """
    driver_map = {target_param: []}
    for root, dirs, files in os.walk(os.path.join(base_dir, "drivers")):
        for file in files:
            if file.endswith((".c", ".h")):
                file_path = os.path.join(root, file)
                lines = read_file_with_fallback(file_path)
                if lines:
                    for line in lines:
                        if target_param in line:
                            driver_map[target_param].append(file_path)
                            break
    return driver_map

def write_results_to_file(driver_map, output_file):
    """Write the driver mappings to a text file."""
    with open(output_file, 'w') as f:
        for param, files in driver_map.items():
            f.write(f"Kconfig Parameter: {param}\n")
            if files:
                f.write("Referenced in files:\n")
                for file in files:
                    f.write(f"  {file}\n")
            else:
                f.write("No references found.\n")
            f.write("-" * 40 + "\n")
    print(f"Results written to {output_file}")

def main():
    # Print environment variables for debugging
    print_environment_variables()

    # Base directory of Zephyr source
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
    zephyr_base_dir = os.path.abspath(os.path.join(script_dir, "../../ncs/v2.7.0/zephyr/"))
    print(f"\nStarting search in directory: {zephyr_base_dir}")
    
    # Prompt user for a Kconfig parameter
    target_param = input("Enter the Kconfig parameter to search for: ").strip()
    
    # Step 1: Search if the parameter exists in Kconfig files
    print(f"\nSearching for Kconfig parameter '{target_param}'...")
    if not search_kconfig_for_param(zephyr_base_dir, target_param):
        print(f"Kconfig parameter '{target_param}' not found in the Kconfig files.")
        return
    
    print("Kconfig parameter found. Mapping to driver files...")
    
    # Step 2: Map Kconfig parameter to driver source files
    driver_map = map_kconfig_to_drivers(zephyr_base_dir, target_param)
    
    # Step 3: Save results to a file
    output_file = "driver_mappings.txt"
    write_results_to_file(driver_map, output_file)

if __name__ == "__main__":
    main()
