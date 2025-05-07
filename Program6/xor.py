import sys
from pathlib import Path

BUFFER_SIZE = 4096

def xor_bytes(data: bytearray, key_chunk: bytearray) -> bytearray:
    return bytearray([b ^ k for b, k in zip(data, key_chunk)])

def main():
    key_path = Path("key")
    if not key_path.exists():
        print("Key file not found.", file=sys.stderr)
        sys.exit(1)

    key = bytearray(key_path.read_bytes())
    key_len = len(key)

    offset = 0

    while True:
        chunk = sys.stdin.buffer.read(BUFFER_SIZE)
        if not chunk:
            break

        chunk = bytearray(chunk)
        chunk_len = len(chunk)

        if offset + chunk_len > key_len:
            print("Key is too short for the input data.", file = sys.stderr)
            sys.exit(1)

        key_chunk = key[offset:offset + chunk_len]
        output = xor_bytes(chunk, key_chunk)
        sys.stdout.buffer.write(output)

        offset += chunk_len

if __name__ == "__main__":
    main()
