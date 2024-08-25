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

    @staticmethod
    def get_by_value(value):
        for member in ConstantType:
            if member.value == value:
                return member
        raise Exception(f"Constant type {value} not found!")


def read_xu(f, x): return f.read(x)


def read_1u(f): return int.from_bytes(read_xu(f, 1))


def read_2u(f): return int.from_bytes(read_xu(f, 2))


def read_4u(f): return int.from_bytes(read_xu(f, 4))


if __name__ == '__main__':
    constant_pool = []
    clazz = {}
    with open("./Main.class", "rb") as f:
        clazz["magic_number"] = f.read(4)
        clazz["minor_version"] = f.read(2)
        clazz["major_version"] = f.read(2)
        clazz["constant_pool_count"] = read_2u(f)
        print(f"Constant pool count {clazz["constant_pool_count"]}")
        for i in range(clazz["constant_pool_count"] - 1):
            cp_info = {}
            tag = read_1u(f)
            cp_info['tag'] = ConstantType.get_by_value(tag)
            if tag == ConstantType.CONSTANT_Methodref.value or tag == ConstantType.CONSTANT_Fieldref.value or tag == ConstantType.CONSTANT_InterfaceMethodref.value:
                cp_info['class_index'] = read_2u(f)
                cp_info['name_and_type_index'] = read_2u(f)
            elif tag == ConstantType.CONSTANT_Class.value:
                cp_info['name_index'] = read_2u(f)
            elif tag == ConstantType.CONSTANT_NameAndType.value:
                cp_info['name_index'] = read_2u(f)
                cp_info['descriptor_index'] = read_2u(f)
            elif tag == ConstantType.CONSTANT_Utf8.value:
                cp_info['length'] = read_2u(f)
                cp_info["bytes"] = f.read(cp_info["length"])
            elif tag == ConstantType.CONSTANT_String.value:
                cp_info["string_index"] = read_2u(f)
            else:
                assert False, f"Unexpected tag {tag}"
            print(f"[{i + 1}]cp_info = {cp_info}")
            constant_pool.append(cp_info)
        clazz["constant_pool"] = constant_pool
        clazz["access_flags"] = read_2u(f)
        # print(f"magic number = {magic_number}")
