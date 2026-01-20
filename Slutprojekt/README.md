# Shellcode XOR Encryptor

A lightweight Python utility designed to encrypt raw binary data (shellcode) using XOR. It automatically formats the output into arrays for **C** or **Python** projects, or exports it as a raw binary file.



## Features

* **Cyclic XOR Encryption:** Handles keys of any length by repeating the key across the data.
* **Flexible Key Input:** Supports both plain-text strings and hexadecimal keys (e.g., `0x42`).
* **Multiple Output Formats:**
    * `raw`: Exports the raw encrypted bytes.
    * `c`: Formats the data as a `unsigned char buff[]` array.
    * `python`: Formats the data as a `shellcode = []` list.
* **Safety Checks:** Includes error handling for missing files, empty input, and invalid hex formats.

---

## Installation

Ensure you have Python 3.x installed. No external dependencies are required.

1. Save `Slutprojekt.py` to your project folder.
2. Open your terminal or command prompt.

---

## Usage

The script uses command-line arguments to handle input and output.

### Basic Syntax
```bash
py Slutprojekt.py -i <input_file> [-o <output_file>] -k <key> -f <format> [options]

Flag	Name	Required	Description
-i	--in_file	Yes	        Path to the raw binary input file (.bin).
-o	--out_file	No	        Path to save the result. If omitted, result prints to terminal.
-k	--key	    Yes	        XOR key (e.g., secret or 0x42).
-f	--format	No	        raw (default), python, or c.
```

## Examples

1. Encrypt and format for C
```bash
py Slutprojekt.py -i beacon.bin -k MySecretKey -f c -o encrypted.txt
```

2. Encrypt using a Hex key and output to Python
```bash
py Slutprojekt.py -i shell.bin -k 0xAA -f python
```

3. Generate raw encrypted binary
```bash
py Slutprojekt.py -i payload.bin -k 0x55 -f raw -o payload.enc
```

Technical Details
The encryption follows the cyclic XOR principle. This ensures that even if your key is only 1 byte long, it can encrypt a file of any size by repeating the key pattern.

## Output Examples

### C Format (-f c)
```text
----------------------------------------
Encrypted shellcode saved to encrypted.txt

unsigned char buff[] = { 0x4a, 0x21, 0x01 };
----------------------------------------
```
