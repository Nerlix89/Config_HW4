import yaml
import struct
import argparse

INSTRUCTION_SET = {
    "LOAD_CONST": 30,      # A=30
    "READ_MEM": 19,        # A=19
    "WRITE_MEM": 17,       # A=17
    "BITREVERSE": 23,      # A=23
}

def assemble(input_file, binary_file, log_file):
    instructions = []
    binary_data = bytearray()

    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()  # Удаляем пробелы в начале и конце строки
            if not line:  # Пропускаем пустые строки
                continue

            parts = line.split()  # Разбиваем строку на части
            cmd = parts[0]
            opcode = INSTRUCTION_SET.get(cmd)

            if cmd == "LOAD_CONST":
                const = int(parts[1])
                instruction = struct.pack("<BI", opcode, const)
                binary_data.extend(instruction)
                instructions.append({"instruction": cmd, "value": const})

            elif cmd in ["READ_MEM", "WRITE_MEM"]:
                address = int(parts[1])
                instruction = struct.pack("<BI", opcode, address)
                binary_data.extend(instruction)
                instructions.append({"instruction": cmd, "address": address})

            elif cmd == "BITREVERSE":
                instruction = struct.pack("<B", opcode)
                binary_data.extend(instruction)
                instructions.append({"instruction": cmd})

    with open(binary_file, "wb") as f:
        f.write(binary_data)

    with open(log_file, "w") as f:
        yaml.dump(instructions, f, default_flow_style=False, sort_keys=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input file")
    parser.add_argument("--binary", required=True, help="Path to output binary file")
    parser.add_argument("--log", required=True, help="Path to log file")
    args = parser.parse_args()

    assemble(args.input, args.binary, args.log)
