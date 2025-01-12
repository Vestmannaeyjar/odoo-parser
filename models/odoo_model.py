from models import OdooAttribute, OdooMethod
import ast


class OdooModel:

    def __init__(self, class_name, class_code):
        self.class_name = class_name
        self.class_code = class_code
        self.methods = []
        self.attributes = []

        self._parse_class_code()

    def _get_method_nodes(self):
        tree = ast.parse(self.class_code)
        method_nodes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                method_nodes.append(node)

        return method_nodes

    def _is_class_level_assignment(self, node):
        for method in self._get_method_nodes():
            if method.lineno <= node.lineno <= method.end_lineno:
                return False
        return True

    def _parse_class_code(self):
        tree = ast.parse(self.class_code)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                method_name = node.name
                method_args = [arg.arg for arg in node.args.args]
                start = node.lineno - 1
                end = start + len(node.body) + 1
                method_code = ''.join(self.class_code.splitlines()[start:end])
                self.methods.append(OdooMethod(method_name, self.class_name, method_args, method_code))

            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                        if self._is_class_level_assignment(node):
                            self.attributes.append(OdooAttribute(target))
