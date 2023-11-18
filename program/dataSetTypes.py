from enum import Enum

SUPPLY = "Supply"
PRODUCTS = "Products"
SUPPLIERS = "Suppliers"

DATA_PATH = "../data/"
INDEX_PATH = "../index/"
TREE_PIC_PATH = "../treePic/"
OUTPUT_PATH = "../queryOutput/"

QUERY_RESULT = "queryResult.txt"
SCHEMAS = "schemas.txt"
PAGE_POOL = "pagePool.txt"
PAGE_LINK = "pageLink.txt"
INDEX_DIRECTORY = "directory.txt"

TYPE_POS = 0
CONTENT_POS = 2
RELATION_POS = 0
ATTR_POS = 1
ROOT_POS = 2
ORDER_POS = 3

CAPACITY = 2


class INTERNAL_NODE(Enum):
    NODE_TYPE = 0
    PARENTAL_POINTER = 1
    CONTENT = 2


class LEAF_NODE(Enum):
    NODE_TYPE = 0
    PARENTAL_POINTER = 1
    LEFT_POINTER = 2
    RIGHT_POINTER = 3
    CONTENT = 4


class INDEX_TYPE(Enum):
    CLUSTERED_INDEX = 0
    UNCLUSTERED_INDEX = 1


class ATT_CATEGORY(Enum):
    XID = 0
    OTHER = 1


class DIRECTION(Enum):
    LEFT = 0
    RIGHT = 1


class ATT_TYPE(Enum):
    STRING = "str"
    INTEGER = "int"


clustered_index = [("Products", "pid"), ("Suppliers", "sid"), ("Supply", "sid")]
unclustered_index = [
    ("Products", "pname"), ("Products", "color"),
    ("Suppliers", "sname"), ("Suppliers", "address"),
    ("Supply", "pid"), ("Supply", "cost")
]
xid_att = ["sid", "pid"]
att_type = {"sid": ATT_TYPE.STRING.value, "sname": ATT_TYPE.STRING.value, "address": ATT_TYPE.STRING.value,
            "pid": ATT_TYPE.STRING.value, "pname": ATT_TYPE.STRING.value, "color": ATT_TYPE.STRING.value,
            "cost": ATT_TYPE.INTEGER.value}