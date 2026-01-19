"""
This module provides tools to XOR-encrypt binary data and 
automatically format the results for C or Python projects.

Functions:
    - XOR encryption with a custom key (string or hex).
    - Export to C-array format.
    - Export to Python-list format.

Usage:
    python Slutprojekt.py -i input.bin -k secret -f python
"""
import argparse
import sys

# Skapar en c-array output 
def c_array(data):
    """Formats binary data into a C-style byte array string."""
    hex_list = [f"0x{b:02x}" for b in data]
    return f"unsigned char buff[] = {{ {', '.join(hex_list)}}};"

# Skapar en python-array/lista output
def python_array(data):
    """Formats binary data into a Python list of hex values."""
    hex_list = [f"0x{b:02x}" for b in data]
    return f"shellcode = [{', '.join(hex_list)}]"

#
def xor_encrypt(data, key):
    """
    Encrypts data using XOR by iterating cyclically over the key.
    
    :param data: Bytes object to encrypt.
    :param key: List of integers representing the XOR key.
    :return: Bytes object containing the encrypted result.
    """
    output = bytearray()
    for i in range(len(data)):
        output.append(data[i] ^ key[i % len(key)])
    return bytes(output)


# Huvudprogram med argparse
def main():
    """
    Parses command-line arguments, reads input file, and coordinates 
    encryption and export of results to file or terminal.
    """
    parser = argparse.ArgumentParser(description="XOR Encryptor for Shellcode")

    # Argument/nödvändiga flaggor för användaren
    parser.add_argument("-i","--in_file", required=True, help="Input raw shellcode (.bin)")
    parser.add_argument("-o","--out_file", required=False, help="Output file for encrypted shellcode")
    parser.add_argument("-k","--key", required=True, help="XOR key (e.g. 0x42 or secret)")
    parser.add_argument("-f","--format", choices=["raw", "python", "c"], default="raw")

    args = parser.parse_args()

    # Försök läsa indata. Använder 'rb' eftersom shellcode alltid är binär.
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

    # Omvandlar nyckel-strängen till en lista av integers med ord() för att kunna köra XOR
    if args.key.startswith("0x"):
        try:
            key = [int(args.key, 16)]
        except ValueError:
            print("Error: Invalid hex format for key.")
            sys.exit(1)
    else:
        key = [ord(c) for c in args.key] # ord() hämtar en bokstavs ASCII-värde, XOR inte funkar på bokstäver
    
    # Genomför kryptering
    encrypted_data = xor_encrypt(shellcode, key)

    # Formaterar datan baserat på vald flagga (-f)
    if args.format == "c":
        results = c_array(encrypted_data)
    elif args.format == "python":
        results = python_array(encrypted_data)
    else:
        results = encrypted_data

    # Sparar till fil eller skriver ut till konsolen
    if args.out_file:
        # Binärt läge "wb" för raw, textläge "w" för C/Python
        if args.format == "raw":
            mode = "wb"
        else:
            mode = "w"
        with open(args.out_file, mode) as f:
            f.write(results)
        print(f"Result saved to {args.out_file}")
    else:
        print(results)

if __name__ == "__main__":
    main()