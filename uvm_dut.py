from uvm_properties import uvm_parameter
from uvm_sv import uvm_arg, uvm_sv
import pathlib as pl


class uvm_in_out:
    def __init__(self, in_or_out, type, name, value="", lbs="", mbs=""):
        self.in_or_out = in_or_out
        self.type = type
        self.name = name
        self.value = value
        self.lbs = lbs
        self.mbs = mbs

    def __repr__(self):
        return f"uvm_in_out({self.in_or_out!r}, {self.type!r}, {self.name!r}, {self.value!r})"


# 本模块不会生成任何文件，会将导入module模块进行解析
class uvm_dut(uvm_sv):
    def __init__(self, module_path):
        super().__init__()
        self.name = ""
        self.content = ""
        self.mod_path = pl.Path(module_path)
        if (not self.mod_path.exists()) or self.mod_path.is_dir():
            raise Exception("wrong file path")
        self.parameters: list[uvm_parameter] = []
        self.wires: list[uvm_in_out] = []
        self.process()

    def process(self):
        self.content = self.read_file()
        self.get_type()
        self.get_module_name()
        self.get_sharps_parameters()
        self.get_wires_to_list()

    def read_file(self):
        if not self.mod_path.exists():
            raise FileNotFoundError(f"SV file not found: {self.mod_path}")
        return self.mod_path.read_text(encoding="utf-8")

    def _strip_comments(self, text: str) -> str:
        import re
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        text = re.sub(r"//.*?$", "", text, flags=re.M)
        return text

    def _find_matching_parenthesis(self, text: str, start_index: int) -> int:
        depth = 0
        in_string = False
        escape = False
        for index in range(start_index, len(text)):
            char = text[index]
            if char == "\\" and not escape:
                escape = True
                continue
            if char in ('"', "'") and not escape:
                in_string = not in_string
            if in_string:
                escape = False
                continue
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    return index
            escape = False
        raise ValueError("No matching parenthesis found")

    def _split_top_level(self, text: str, delimiter: str) -> list[str]:
        parts = []
        current = []
        depth = 0
        in_string = False
        escape = False
        for char in text:
            if char == "\\" and not escape:
                escape = True
                current.append(char)
                continue
            if char in ('"', "'") and not escape:
                in_string = not in_string
            if not in_string:
                if char == "(":
                    depth += 1
                elif char == ")":
                    depth = max(depth - 1, 0)
                elif char == delimiter and depth == 0:
                    parts.append("".join(current))
                    current = []
                    continue
            current.append(char)
            escape = False
        if current:
            parts.append("".join(current))
        return parts

    def get_type(self):
        import re
        clean = self._strip_comments(self.content)
        match = re.search(r"^\s*(module|interface)\b", clean, flags=re.M)
        if not match:
            raise ValueError("No module or interface declaration found")
        module_type = match.group(1)
        if module_type != "module":
            raise ValueError(f"Unsupported type: {module_type}. Only module is supported.")

    def get_module_name(self):
        import re
        clean = self._strip_comments(self.content)
        match = re.search(r"^\s*module\s+([A-Za-z_]\w*)", clean, flags=re.M)
        if not match:
            raise ValueError("Cannot determine module name")
        self.name = match.group(1)

    def get_sharps_parameters(self):
        import re
        clean = self._strip_comments(self.content)
        module_header = re.search(
            rf"^\s*module\s+{re.escape(self.name)}\s*#\s*\((.*?)\)\s*\(",
            clean,
            flags=re.S | re.M,
        )
        if not module_header:
            return

        parameter_block = module_header.group(1)
        parameter_items = self._split_top_level(parameter_block, ",")
        for item in parameter_items:
            part = item.strip()
            if not part:
                continue
            part = part.rstrip(",").strip()
            part = re.sub(r"//.*$", "", part, flags=re.M).strip()
            if not part:
                continue
            if part.startswith("parameter"):
                part = part[len("parameter") :].strip()
            if "=" not in part:
                continue
            left, right = part.split("=", 1)
            left = left.strip()
            right = right.strip().rstrip(",")
            left_tokens = left.split()
            if len(left_tokens) > 1:
                left = left_tokens[-1]
            if left and right:
                self.parameters.append(uvm_parameter(left, right))

    def get_wires_to_list(self):
        import re
        clean = self._strip_comments(self.content)
        module_header = re.search(
            rf"^\s*module\s+{re.escape(self.name)}(?:\s*#\s*\(.*?\))?\s*\(",
            clean,
            flags=re.S | re.M,
        )
        if not module_header:
            return

        start = module_header.end() - 1
        end = self._find_matching_parenthesis(clean, start)
        port_block = clean[start + 1 : end]
        port_items = self._split_top_level(port_block, ",")

        for item in port_items:
            raw = item.strip()
            if not raw:
                continue
            raw = re.sub(r"\s*//.*$", "", raw, flags=re.M).strip()
            if not raw:
                continue
            m = re.match(r"^(input|output|inout)\b\s*(.*)$", raw)
            if not m:
                continue
            direction = m.group(1)
            rest = m.group(2).strip()
            rest = rest.rstrip(",").strip()
            type_match = re.match(r"^(wire|logic|reg|tri|bit)\b\s*(.*)$", rest)
            type_name = "wire"
            if type_match:
                type_name = type_match.group(1)
                rest = type_match.group(2).strip()
            width = ""
            lbs = ""
            mbs = ""
            width_match = re.match(r"^(\[[^\]]+\])\s*(.*)$", rest)
            if width_match:
                width = width_match.group(1)
                rest = width_match.group(2).strip()
                width_content = width[1:-1].strip()
                if ":" in width_content:
                    left, right = [part.strip() for part in width_content.split(":", 1)]
                    lbs = left
                    mbs = right
                else:
                    lbs = width_content
            name_match = re.match(r"^([A-Za-z_]\w*)", rest)
            if not name_match:
                continue
            name = name_match.group(1)
            self.wires.append(uvm_in_out(direction, type_name, name, width, lbs, mbs))

    def get_wires_str(self):
        lines = []
        for wire in self.wires:
            if wire.lbs or wire.mbs:
                if wire.lbs and wire.mbs:
                    width = f" [{wire.lbs}:{wire.mbs}]"
                elif wire.lbs:
                    width = f" [{wire.lbs}]"
                else:
                    width = f" [{wire.mbs}]"
            elif wire.value:
                width = f" {wire.value}"
            else:
                width = ""
            lines.append(f"{wire.in_or_out} {wire.type}{width} {wire.name};")
        return "\n".join(lines) + ("\n" if lines else "")

    def __repr__(self):
        return f"uvm_dut(name={self.name!r}, path={self.mod_path!r})"

