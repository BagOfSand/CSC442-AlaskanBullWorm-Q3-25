import sys

SENTINEL = bytearray([0x0, 0xFF, 0x0, 0x0, 0xFF, 0x0])


def read_file(filepath):
    try:
        with open(filepath, 'rb') as file:
            return bytearray(file.read())
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)


def byte_store(wrapper, hidden, offset, interval):
    idx = 0
    while idx < len(hidden):
        wrapper[offset] = hidden[idx]
        offset += interval
        idx += 1
    idx = 0
    while idx < len(SENTINEL):
        wrapper[offset] = SENTINEL[idx]
        offset += interval
        idx += 1
    return wrapper


def byte_retrieve(wrapper, offset, interval):
    hidden_data = bytearray()
    sentinel_len = len(SENTINEL)
    
    while offset < len(wrapper):
        byte = wrapper[offset]
        hidden_data.append(byte)
        
        if hidden_data[-sentinel_len:] == SENTINEL:
            try:
                return hidden_data[:-sentinel_len].decode('utf-8', errors='replace')
            except UnicodeDecodeError:
                return hidden_data[:-sentinel_len]

        offset += interval
    

    try:
        return hidden_data.decode('utf-8', errors='replace')
    except UnicodeDecodeError:
        return hidden_data


def bit_store(wrapper, hidden, offset):
    for byte in hidden + SENTINEL:
        for i in range(8):
            wrapper[offset] &= 0b11111110
            wrapper[offset] |= (byte & 0b10000000) >> 7
            byte = (byte << 1) & 0xFF
            offset += 1
    return wrapper


def bit_retrieve(wrapper, offset, reverse=False):
    hidden_data = bytearray()
    sentinel_len = len(SENTINEL)

    while offset < len(wrapper):
        byte = 0


        for _ in range(8):
            if offset >= len(wrapper):
                break


            if reverse:
                byte = (byte >> 1) | ((wrapper[offset] & 0b00000001) << 7)
            else:
                byte = (byte << 1) | (wrapper[offset] & 0b00000001)

            offset += 1

        hidden_data.append(byte)


        if hidden_data[-sentinel_len:] == SENTINEL:
            return hidden_data[:-sentinel_len]

    return hidden_data


def main():
    args = sys.argv[1:]

    mode = None
    method = None
    offset = 0
    interval = 1
    reverse = False
    wrapper_file = None
    hidden_file = None


    second_offset = None
    second_interval = None

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == "-s":
            mode = "store"
        elif arg == "-r":
            mode = "retrieve"
        elif arg == "-b":
            method = "bit"
        elif arg == "-B":
            method = "byte"
        elif arg.startswith("-o"):
            if second_offset is None:
                offset = int(arg[2:])
            else:
                second_offset = int(arg[2:])
        elif arg.startswith("-i"):
            if second_interval is None:
                interval = int(arg[2:])
            else:
                second_interval = int(arg[2:])
        elif arg == "-w":
            i += 1
            if i < len(args):
                wrapper_file = args[i]
        elif arg == "-h":
            i += 1
            if i < len(args):
                hidden_file = args[i]
        elif arg == "-rev":
            reverse = True

        i += 1

    if not wrapper_file:
        print("Error: Wrapper file must be specified with -w<val>")
        sys.exit(1)

    wrapper = read_file(wrapper_file)

    if mode == "store":
        if not hidden_file:
            print("Error: Hidden file must be specified in store mode with -h<val>")
            sys.exit(1)
        hidden = read_file(hidden_file)
        if method == "byte":
            output = byte_store(wrapper, hidden, offset, interval)
        elif method == "bit":
            output = bit_store(wrapper, hidden, offset)
        else:
            print("Error: Invalid method. Use -b for bit or -B for byte.")
            sys.exit(1)
        sys.stdout.buffer.write(output)

    elif mode == "retrieve":
        if method == "byte":

            extracted_1 = byte_retrieve(wrapper, offset, interval)
            if isinstance(extracted_1, str):
                sys.stdout.write(extracted_1.encode('utf-8', errors='replace').decode('utf-8'))
            else:
                sys.stdout.buffer.write(extracted_1)

            if second_offset is not None and second_interval is not None:
                extracted_2 = byte_retrieve(wrapper, second_offset, second_interval)
    
                if isinstance(extracted_2, str):
                    sys.stdout.write(extracted_2.encode('utf-8', errors='replace').decode('utf-8'))
                else:
                    sys.stdout.buffer.write(extracted_2)


        elif method == "bit":
            extracted = bit_retrieve(wrapper, offset, reverse)
            sys.stdout.buffer.write(extracted)
        else:
            print("Error: Invalid method. Use -b for bit or -B for byte.")
            sys.exit(1)

if __name__ == "__main__":
    main()