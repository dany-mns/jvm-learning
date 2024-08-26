import json
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


class_access_flags = [
    ("ACC_PUBLIC", 0x0001),
    ("ACC_FINAL", 0x0010),
    ("ACC_SUPER", 0x0020),
    ("ACC_INTERFACE", 0x0200),
    ("ACC_ABSTRACT", 0x0400),
    ("ACC_SYNTHETIC", 0x1000),
    ("ACC_ANNOTATION", 0x2000),
    ("ACC_ENUM", 0x4000)
]

method_access_flags = [
    ("ACC_PUBLIC", 0x0001),
    ("ACC_PRIVATE", 0x0002),
    ("ACC_PROTECTED", 0x0004),
    ("ACC_STATIC", 0x0008),
    ("ACC_FINAL", 0x0010),
    ("ACC_SYNCHRONIZED", 0x0020),
    ("ACC_BRIDGE", 0x0040),
    ("ACC_VARARGS", 0x0080),
    ("ACC_NATIVE", 0x0100),
    ("ACC_ABSTRACT", 0x0400),
    ("ACC_STRICT", 0x0800),
    ("ACC_SYNTHETIC", 0x1000)
]


def read_xu(f, x): return f.read(x)


def read_1u(f): return int.from_bytes(read_xu(f, 1))


def read_2u(f): return int.from_bytes(read_xu(f, 2))


def read_4u(f): return int.from_bytes(read_xu(f, 4))


def get_access_flags(flags, access_flags) -> [str]:
    return [name for (name, value) in access_flags if (flags & value) != 0]


if __name__ == '__main__':
    constant_pool = []
    clazz = {}
    with open("./Main.class", "rb") as f:
        clazz["magic_number"] = read_4u(f)
        clazz["minor_version"] = read_2u(f)
        clazz["major_version"] = read_2u(f)
        clazz["constant_pool_count"] = read_2u(f)
        print(f"Constant pool count {clazz["constant_pool_count"]}")
        for i in range(clazz["constant_pool_count"] - 1):
            cp_info = {}
            tag = read_1u(f)
            cp_info['tag'] = ConstantType.get_by_value(tag).name
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
                cp_info["bytes"] = f.read(cp_info["length"]).decode('utf-8') # TODO Remove decode
            elif tag == ConstantType.CONSTANT_String.value:
                cp_info["string_index"] = read_2u(f)
            else:
                assert False, f"Unexpected tag {tag}"
            print(f"[{i + 1}]cp_info = {cp_info}")
            constant_pool.append(cp_info)
        clazz["constant_pool"] = constant_pool
        clazz["access_flags"] = get_access_flags(read_2u(f), class_access_flags)
        clazz["this_class"] = read_2u(f)
        clazz["super_class"] = read_2u(f)
        clazz["interfaces_count"] = read_2u(f)
        for i in range(clazz["interfaces_count"]):
            assert False, "Parsing interfaces is NOT IMPLEMENTED"

        clazz["fields_count"] = read_2u(f)
        for i in range(clazz["fields_count"]):
            assert False, "Parsing fields is NOT IMPLEMENTED"

        clazz["methods_count"] = read_2u(f)
        methods = []
        for i in range(clazz["methods_count"]):
            """
            method_info {
                u2             access_flags;
                u2             name_index;
                u2             descriptor_index;
                u2             attributes_count;
                attribute_info attributes[attributes_count];
            }
            """
            method_info = {"access_flags ": get_access_flags(read_2u(f), method_access_flags),
                           "name_index ": read_2u(f), "descriptor_index ": read_2u(f), "attribute_count": read_2u(f)}

            method_attributes = []

            for j in range(method_info["attribute_count"]):
                """
                    attribute_info {
                        u2 attribute_name_index;
                        u4 attribute_length;
                        u1 info[attribute_length];
                    }
                """
                method_attribute = {"attribute_name_index": read_2u(f), "attribute_length": read_4u(f)}
                method_attribute["info"] = f.read(method_attribute["attribute_length"]).decode("UTF-u") # TODO

                method_attributes.append(method_attribute)

            method_info["attribute_info"] = method_attributes

            methods.append(method_info)
        clazz["method_info"] = methods

        clazz["attributes_count"] = read_2u(f)
        attributes = []
        for i in range(clazz["attributes_count"]):
            attributes.append({})
            assert False, "Atrribute in class parsing is NOT IMPLEMENTED"
        clazz["attribute_info"] = attributes

        print(json.dumps(clazz, indent=4, sort_keys=True))
        # print(f"magic number = {magic_number}")

    print(clazz["constant_pool"][clazz["constant_pool"][clazz["this_class"] - 1]["name_index"] - 1])
