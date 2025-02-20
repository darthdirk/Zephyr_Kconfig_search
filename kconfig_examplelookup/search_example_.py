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

    Args:
        file_path (str): Path to the file.

    Returns:
        list: File lines or None if unable to read.
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

def search_kconfig_files(base_dir, parameter):
    """
    Search for a specific parameter in Kconfig-related files.

    Args:
        base_dir (str): Base directory to start the search.
        parameter (str): Parameter to search for.

    Returns:
        list: Matches with file name, line number, and context.
    """
    matches = []
    pattern = re.compile(re.escape(parameter), re.IGNORECASE)  # Case-insensitive search
    file_extensions = [".conf", ".sysbuild"]  # Only Kconfig-related files

    # Walk through the directory to find matching files
    for root, _, files in os.walk(base_dir):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)
                print(f"Scanning file: {file_path}")  # Debug output
                
                # Read the file and search for the parameter
                lines = read_file_with_fallback(file_path)
                if lines:
                    for i, line in enumerate(lines):
                        # Decode binary lines if needed
                        if isinstance(line, bytes):
                            try:
                                line = line.decode('utf-8')
                            except UnicodeDecodeError:
                                continue
                        
                        if pattern.search(line):  # Use regex search
                            context = lines[max(0, i-2):i+3]  # Get surrounding lines for context
                            # Decode binary context lines
                            context = [l.decode('utf-8', errors='ignore') if isinstance(l, bytes) else l for l in context]
                            matches.append({
                                "file": file_path,
                                "line_number": i + 1,
                                "context": context
                            })
    
    return matches

def main():
    # Print all environment variables
    print_environment_variables()
        
    # Base directory of Zephyr source
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
    zephyr_base_dir = os.path.abspath(os.path.join(script_dir, "../../ncs/v2.7.0/"))

    print(f"\nStarting search in directory: {zephyr_base_dir}")
    
    # The parameter to search for
    parameter_to_search = input("Enter the parameter to search for: ").strip()
    
    # Find parameter occurrences
    matches = search_kconfig_files(zephyr_base_dir, parameter_to_search)
    
    if matches:
        print(f"\nFound '{parameter_to_search}' in the following locations:\n")
        for match in matches:
            print(f"File: {match['file']} (Line {match['line_number']})")
            print("Context:")
            for line in match["context"]:
                print(line.strip())
            print("-" * 40)
    else:
        print(f"\nNo matches found for '{parameter_to_search}'.")

if __name__ == "__main__":
    main()
