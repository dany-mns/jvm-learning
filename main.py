from enum import Enum


class ConstantType(Enum):
    CONSTANT_Class = 7
    CONSTANT_Fieldref = 9
    CONSTANT_Methodref = 10
    CONSTANT_InterfaceMethodref = 11
    CONSTANT_String = 8
    CONSTANT_Integer = 3
    CONSTANT_Float = 4
    CONSTANT_Long = 5
    CONSTANT_Double = 6
    CONSTANT_NameAndType = 12
    CONSTANT_Utf8 = 1
    CONSTANT_MethodHandle = 15
    CONSTANT_MethodType = 16
    CONSTANT_InvokeDynamic = 18


if __name__ == '__main__':
    constant_pool = []
    with open("./Main.class", "rb") as f:
        magic_number = f.read(4)
        minor_version = f.read(2)
        major_version = f.read(2)
        constant_pool_count = int.from_bytes(f.read(2))
        print(f"Constant pool count {constant_pool_count}")
        for i in range(constant_pool_count - 1):
            cp_info = {}
            tag = int.from_bytes(f.read(1))
            cp_info['tag'] = tag
            if tag == ConstantType.CONSTANT_Methodref.value:
                cp_info['class_index'] = int.from_bytes(f.read(2))
                cp_info['name_and_type_index'] = int.from_bytes(f.read(2))
                print(f"cp_info = {cp_info}")
            else:
                assert False, f"Unexpected tag {tag}"
            constant_pool.append(cp_info)

        # print(f"magic number = {magic_number}")
