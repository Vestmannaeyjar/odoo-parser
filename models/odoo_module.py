import ast
import re
from pathlib import Path
from odoo_model import OdooModel


class OdooModule:

    def __init__(self, module_path):
        self.module_path = Path(module_path)

        # Listing of items (files/directories)
        self.files = [str(f) for f in self.module_path.rglob("*") if f.is_file()]
        self.directories = [str(d) for d in self.module_path.rglob("*") if d.is_dir()]
        self.xmls = [str(f) for f in self.module_path.rglob("*.xml")]
        self.pys = [str(f) for f in self.module_path.rglob("*.py")]
        self.models = self.get_models()

        # Listing of manifest data
        manifest_path = self.module_path / '__manifest__.py'
        manifest_dict = {}

        with open(manifest_path, 'r', encoding='utf_8') as manifest_file:
            manifest_file_content = manifest_file.read()
            dict_match = re.search(r'(\{.*\})', manifest_file_content, re.DOTALL)

            if dict_match:
                dict_content = dict_match.group(0)
                try:
                    manifest_dict = ast.literal_eval(dict_content)
                except ValueError as e:
                    print(f"Error parsing the manifest dictionary: {e}")

        self.name = manifest_dict.get('name', None)
        self.version = manifest_dict.get('version', None)
        self.category = manifest_dict.get('category', None)
        self.summary = manifest_dict.get('summary', None)
        self.description = manifest_dict.get('description', None)
        self.author = manifest_dict.get('author', None)
        self.website = manifest_dict.get('website', None)
        self.license = manifest_dict.get('license', None)
        self.depends = manifest_dict.get('depends', None)
        self.data = manifest_dict.get('data', None)
        self.demo = manifest_dict.get('demo', None)
        self.assets = manifest_dict.get('assets', None)
        self.installable = manifest_dict.get('installable', None)
        self.auto_install = manifest_dict.get('auto_install', None)
        self.application = manifest_dict.get('application', None)
        self.images = manifest_dict.get('images', None)

    def get_models(self):
        models = {}
        for py in self.pys:
            with open(py, 'r', encoding='utf-8') as file:
                tree = ast.parse(file.read())
                lines = file.readlines()

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    class_code = ''.join(lines[node.lineno - 1:node.end_lineno])
                    models[class_name] = OdooModel(class_name, class_code)
        return models


