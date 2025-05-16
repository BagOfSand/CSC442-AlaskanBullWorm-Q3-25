import sys
import argparse

# Sentinel marking end of hidden data (6 bytes)
SENTINEL = bytearray([0x00, 0xFF, 0x00, 0x00, 0xFF, 0x00])


def store_byte(wrapper: bytearray, hidden: bytearray, offset: int, interval: int) -> None:
    """Store hidden data + sentinel byte-by-byte into wrapper at given offset and interval"""
    total = hidden + SENTINEL
    end_pos = offset + interval * (len(total) - 1)
    if end_pos >= len(wrapper):
        sys.exit("Error: wrapper too small for byte-mode storing with given offset and interval.")
    pos = offset
    for b in total:
        wrapper[pos] = b
        pos += interval


def retrieve_byte(wrapper: bytearray, offset: int, interval: int) -> bytearray:
    """Retrieve hidden data in byte-mode until sentinel is encountered"""
    data = bytearray()
    pos = offset
    while pos < len(wrapper):
        b = wrapper[pos]
        data.append(b)
        if data.endswith(SENTINEL):
            return data[:-len(SENTINEL)]
        pos += interval
    return data


def store_bit(wrapper: bytearray, hidden: bytearray, offset: int, interval: int) -> None:
    """Store hidden data + sentinel bit-by-bit into wrapper LSBs at given offset and interval"""
    total = hidden + SENTINEL
    # check size
    needed = (len(total) * 8 - 1) * interval + offset
    if needed >= len(wrapper):
        sys.exit("Error: wrapper too small for bit-mode storing with given offset and interval.")
    pos = offset
    for byte in total:
        b = byte
        for _ in range(8):
            # zero out LSB
            wrapper[pos] &= 0xFE
            # set LSB to MSB of hidden
            wrapper[pos] |= (b & 0x80) >> 7
            # shift hidden byte
            b = (b << 1) & 0xFF
            pos += interval


def retrieve_bit(wrapper: bytearray, offset: int, interval: int) -> bytearray:
    """Retrieve hidden data bit-by-bit from wrapper LSBs until sentinel is encountered"""
    data = bytearray()
    pos = offset
    while pos + 7 * interval < len(wrapper):
        b = 0
        for i in range(8):
            bit = wrapper[pos] & 0x1
            b = (b << 1) | bit
            pos += interval
        data.append(b)
        if data.endswith(SENTINEL):
            return data[:-len(SENTINEL)]
    return data


def main():
    usage = (
        "python Steg.py -(sr) -(bB) -o<val> [-i<val>] -w<val> [-h<val>]"
    )
    parser = argparse.ArgumentParser(add_help=False, usage=usage)
    # operations
    parser.add_argument('-s', action='store_true', dest='store', help='store')
    parser.add_argument('-r', action='store_true', dest='retrieve', help='retrieve')
    # modes
    parser.add_argument('-b', action='store_true', dest='bit', help='bit mode')
    parser.add_argument('-B', action='store_true', dest='byte', help='byte mode')
    # parameters
    parser.add_argument('-o', type=int, dest='offset', required=True, help='set offset')
    parser.add_argument('-i', type=int, dest='interval', default=1, help='set interval')
    parser.add_argument('-w', dest='wrapper', required=True, help='wrapper file')
    parser.add_argument('-h', dest='hidden', help='hidden file (required for store)')

    args = parser.parse_args()

    # validate
    if args.store == args.retrieve:
        sys.exit('Error: specify exactly one of -s (store) or -r (retrieve).')
    if args.bit == args.byte:
        sys.exit('Error: specify exactly one of -b (bit) or -B (byte) mode.')

    # read wrapper
    try:
        wrapper_data = bytearray(open(args.wrapper, 'rb').read())
    except FileNotFoundError:
        sys.exit(f"Error: wrapper file '{args.wrapper}' not found.")

    if args.store:
        # hidden required
        if not args.hidden:
            sys.exit('Error: hidden file (-h) is required when storing.')
        try:
            hidden_data = bytearray(open(args.hidden, 'rb').read())
        except FileNotFoundError:
            sys.exit(f"Error: hidden file '{args.hidden}' not found.")

        if args.byte:
            store_byte(wrapper_data, hidden_data, args.offset, args.interval)
        else:
            store_bit(wrapper_data, hidden_data, args.offset, args.interval)
        sys.stdout.buffer.write(wrapper_data)

    else:  # retrieve
        if args.byte:
            hidden = retrieve_byte(wrapper_data, args.offset, args.interval)
        else:
            hidden = retrieve_bit(wrapper_data, args.offset, args.interval)
        sys.stdout.buffer.write(hidden)


if __name__ == '__main__':
    main()
