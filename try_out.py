from models import OdooModule

a = OdooModule('/Users/dries/Documents/leren/Python/jaar 2/syntra_python_groepswerk_2024-2025/')

print(a.files)
print(a.directories)
print(a.xmls)
print(a.pys)
print(a.name)
print(a.version)
print(a.category)
print(a.summary)
print(a.description)
print(a.author)
print(a.website)
print(a.license)
print(a.depends)
print(a.data)
print(a.demo)
print(a.assets)
print(a.installable)
print(a.auto_install)
print(a.application)
print(a.images)

for model_name, model in a.models.items():
    print(model_name, model.methods, model.attributes)

