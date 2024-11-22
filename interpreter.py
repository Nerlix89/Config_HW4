import yaml
import struct
import argparse

MEMORY = [0] * 1024
ACCUMULATOR = 0

def execute(binary_file, memory_file, memory_range):
    global ACCUMULATOR, MEMORY
    start, end = map(int, memory_range.split(":"))

    with open(binary_file, "rb") as f:
        binary_data = f.read()

    pc = 0
    while pc < len(binary_data):
        opcode = binary_data[pc]
        pc += 1

        if opcode == 30:  # LOAD_CONST
            value = struct.unpack("<I", binary_data[pc:pc + 4])[0]
            ACCUMULATOR = value & 0xFF  # Ограничиваем значение до 8 бит
            pc += 4

        elif opcode == 19:  # READ_MEM
            address = struct.unpack("<I", binary_data[pc:pc + 4])[0]
            ACCUMULATOR = MEMORY[address]
            pc += 4

        elif opcode == 17:  # WRITE_MEM
            address = struct.unpack("<I", binary_data[pc:pc + 4])[0]
            MEMORY[address] = ACCUMULATOR & 0xFF  # Записываем только 8 бит
            pc += 4

        elif opcode == 23:  # BITREVERSEE
            ACCUMULATOR = int('{:08b}'.format(ACCUMULATOR & 0xFF)[::-1], 2)  # Реверсируем только 8 бит

    result = [{"address": addr, "value": MEMORY[addr]} for addr in range(start, end + 1)]
    with open(memory_file, "w") as f:
        yaml.dump({"memory": result}, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True, help="Path to input binary file")
    parser.add_argument("--output", required=True, help="Path to memory result file")
    parser.add_argument("--range", required=True, help="Memory range (start:end)")
    args = parser.parse_args()

    execute(args.binary, args.output, args.range)
