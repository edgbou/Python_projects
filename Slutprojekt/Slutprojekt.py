"""
Shellcode XOR Encryptor

This module provides tools to XOR-encrypt binary data and 
automatically format the results for C or Python projects.

Functions:
    - XOR encryption with a custom key (string or hex).
    - Export to C-array format.
    - Export to Python-list format.

Usage:
    py Slutprojekt.py -i input.bin [-o output.bin] -k secret -f python
"""
import argparse
import sys

# Formats binary data as a C-style unsigned char array
def c_array(data):
    """Formats binary data into a C-style byte array string."""
    hex_list = [f"0x{b:02x}" for b in data]
    return f"unsigned char buff[] = {{ {', '.join(hex_list)}}};"

# Formats binary data as a Python list of hex values
def python_array(data):
    """Formats binary data into a Python list of hex values."""
    hex_list = [f"0x{b:02x}" for b in data]
    return f"shellcode = [{', '.join(hex_list)}]"

# Performs XOR encryption/decryption with a repeating key
def xor_encrypt(data, key):
    """
    Applies XOR encryption to the input data using a repeating key.

    Iterates through the data with an index to perform a cyclic XOR operation,
    ensuring the key wraps around if it is shorter than the data.

    :param data: The raw input bytes to be encrypted or decrypted.
    :param key: A list of integers (bytes) used as the XOR key.
    :return: A bytes object containing the resulting data.
    """
    output = []
    key_len = len(key)
    for i, byte in enumerate(data):
        output.append(byte ^ key[i % key_len])
    return bytes(output)


# Main program with argparse
def main():
    """
    Parses command-line arguments, reads input file, and coordinates 
    encryption and export of results to file or terminal.
    """
    parser = argparse.ArgumentParser(description="XOR Encryptor for Shellcode")

    # Command-line arguments/flags
    parser.add_argument("-i","--in_file", required=True, help="Input raw shellcode (.bin)")
    parser.add_argument("-o","--out_file", required=False, help="Output file for encrypted shellcode")
    parser.add_argument("-k","--key", required=True, help="XOR key (e.g. 0x42 or secret)")
    parser.add_argument("-f","--format", choices=["raw", "python", "c"], default="raw")

    args = parser.parse_args()

    # Attempt to read input file
    try:    
        with open(args.in_file, "rb") as f:
            shellcode = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: '{args.in_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading: {e}")
        sys.exit(1)

    if not shellcode:
        print("Error: Input file is empty.")
        sys.exit(1)

    # Converts the key to a list of integers from either hex (0x..) or plain text
    if args.key.startswith("0x"):
        try:
            key = [int(args.key, 16)]
        except ValueError:
            print("Error: Invalid hex format for key.")
            sys.exit(1)
    else:
        key = [ord(c) for c in args.key] # Converts each character to its ASCII integer value
    
    # Execute encryption
    encrypted_data = xor_encrypt(shellcode, key)

    # Select formatting based on the -f flag
    if args.format == "c":
        results = c_array(encrypted_data)
    elif args.format == "python":
        results = python_array(encrypted_data)
    else:
        results = encrypted_data

    # Save to file or print to terminal
    if args.out_file:
        # Binary mode for raw, text mode for formatted arrays
        if args.format == "raw":
            mode = "wb"
        else:
            mode = "w"
        with open(args.out_file, mode) as f:
            f.write(results)
        print("----------------------------------------")
        print(f"Encrypted shellcode saved to {args.out_file}\n")
        print(results)
        print("----------------------------------------")
    else:
        print(results)

if __name__ == "__main__":
    main()