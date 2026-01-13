import argparse
import sys
from pathlib import Path

def c_array(data):
    hex_list = [f"0x{b:02x}" for b in data]
    return f"unsigned char buff[] = {{ {', '.join(hex_list)}}};"

def python_array(data):
    hex_list = [f"0x{b:02x}" for b in data]
    return f"shellcode = [{', '.join(hex_list)}]"

def xor_encrypt(data, key):
    output = bytearray()
    for i in range(len(data)):
        output.append(data[i] ^ key[i % len(key)])
    return bytes(output)


def main():
    parser = argparse.ArgumentParser(description="XOR Encryptor for Shellcode")

    # Argument för användaren
    parser.add_argument("-i","--in_file", required=True, help="Input raw shellcode (.bin)")
    parser.add_argument("-o","--out_file", required=True, help="Output file for encrypted shellcode")
    parser.add_argument("-k","--key", required=True, help="XOR key (e.g. 0x42 or secret)")
    parser.add_argument("-f","--format", choices=["raw", "python", "c"], default="raw")

    args = parser.parse_args()

    # Läser in filen binärt
    try:    
        with open(args.in_file, "rb") as f:
            shellcode = f.read()
    except FileNotFoundError:
        print(f"[-] Fel: Hittade inte filen {args.in_file}")
    if args.key.startswith("x0"):
        key = [int(args.key, 16)]
    else:
        key = [ord(c) for c in args.key] # ord() hämtar en bokstavs ASCII-värde, XOR inte funkar på bokstäver
    
    encryped_data = xor_encrypt(shellcode, key)

    if args.format == "c":
        results = c_array(encryped_data)
    elif args.format == "python":
        results = python_array(encryped_data)
    else:
        results = encryped_data

    if args.out_file:
        if args.format == "raw":
            mode = "wb"
        else:
            mode = "w"
        with open(args.out_file, mode) as f:
            f.write(results)
        print(f"Resultat sparat till {args.out_file}")
    else:
        print(results)

if __name__ == "__main__":
    main()