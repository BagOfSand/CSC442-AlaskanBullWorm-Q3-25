import sys
from pathlib import Path

def xor_bytes(data1: bytes, data2: bytes) -> bytes:
    return bytes([b1 ^ b2 for b1, b2 in zip(data1, data2)])

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 xor.py <file1> <file2>", file=sys.stderr)
        sys.exit(1)

    file1_path = Path(sys.argv[1])
    file2_path = Path(sys.argv[2])

    if not file1_path.exists() or not file2_path.exists():
        print("One or both input files not found.", file=sys.stderr)
        sys.exit(1)

    data1 = file1_path.read_bytes()
    data2 = file2_path.read_bytes()

    if len(data1) != len(data2):
        print("Files must be the same length to XOR.", file=sys.stderr)
        sys.exit(1)

    output = xor_bytes(data1, data2)
    sys.stdout.buffer.write(output)

if __name__ == "__main__":
    main()
