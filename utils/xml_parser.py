import xml.etree.ElementTree as ET
from typing import Any, Union

def tag_name(elem: ET.Element) -> str:
    tag = elem.tag
    if '}' in tag:
        return tag.rsplit('}', 1)[1].lower()
    return tag.lower()

def parse_element(elem: ET.Element) -> Any:
    t = tag_name(elem)
    # dict-like (both <dict> and <d> used in these files)
    if t in ("dict", "d"):
        children = list(elem)
        res = {}
        i = 0
        while i < len(children):
            key_elem = children[i]
            kn = tag_name(key_elem)
            # accept both <k> and <key>
            if kn not in ("k", "key"):
                i += 1
                continue
            key = key_elem.text or ""
            i += 1
            if i >= len(children):
                # missing value, set None
                res[key] = None
                break
            val_elem = children[i]
            res[key] = parse_element(val_elem)
            i += 1
        return res

    # array-like (accept <array> or <a>)
    if t in ("array", "a"):
        return [parse_element(c) for c in list(elem)]

    # integer (<i> or <integer>)
    if t in ("i", "integer"):
        txt = (elem.text or "").strip()
        try:
            return int(txt) if txt != "" else 0
        except Exception:
            try:
                return int(float(txt))
            except Exception:
                return txt

    # real / float
    if t in ("real", "float", "r"):
        txt = (elem.text or "").strip()
        try:
            return float(txt)
        except Exception:
            return txt

    # boolean single-letter tags: <t/> (true), <f/> (false) or words
    if t in ("t", "true"):
        return True
    if t in ("f", "false"):
        return False

    # string / data / date
    if t in ("s", "string", "data", "date"):
        return elem.text or ""

    # fallback: if element has children, build list/dict accordingly
    children = list(elem)
    if children:
        # if children are alternating key/value, try dict
        if all(tag_name(c) in ("k", "key") for c in children[::2]) and len(children) % 2 == 0:
            return parse_element(ET.Element("d", list(children)))  # build fake dict wrapper
        return [parse_element(c) for c in children]

    # final fallback: text
    return elem.text

def load_gmd(path: str) -> Union[dict, list, str, None]:
    """
    解析 .gmd（plist 风格但使用短标签）并返回 Python 原生对象（dict/list/scalars）。
    只负责读取和反序列化，后续处理由调用者完成。
    """
    tree = ET.parse(path)
    root = tree.getroot()
    rt = tag_name(root)

    # 如果根是 plist，寻找第一个 dict 或 array 子节点
    if rt == "plist":
        for child in root:
            cn = tag_name(child)
            if cn in ("dict", "d", "array", "a"):
                return parse_element(child)
        # 如果没有 dict/array，尝试解析根下的第一个子元素
        if len(list(root)) == 1:
            return parse_element(list(root)[0])
        # 否则构造一个 dict/array 尝试解析全部子节点为 dict
        # 尝试把根的子节点当作 dict 的内容（交替 key/value）
        return parse_element(root)

    # 如果根本身是 dict/array
    if rt in ("dict", "d", "array", "a"):
        return parse_element(root)

    # 否则尝试找到第一个 dict/array 下的节点
    node = root.find(".//{*}dict") or root.find(".//{*}d") or root.find(".//{*}array") or root.find(".//{*}a")
    if node is not None:
        return parse_element(node)

    # 无法识别时，返回根的文本或 None
    return root.text
