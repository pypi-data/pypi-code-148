from jinja2 import Environment, FileSystemLoader

## Get this variables from config module
project_name = "probable_fiesta"
package_name = "probable-fiesta"
package_version = "0.0.3"
package_description = "There's a fiesta somewhere"
package_author = "Sergio Sierra"
package_email = "sergio.munoz@pubnub.com"

## tox.ini
tox_exclude_src_files = f"src/{project_name}.py"

## pyproject.toml
#project_name = "probable_fiesta" # already defined above
#package_name = "probable-fiesta" # already defined above
package_version_path = f"src/{project_name}/__about__.py"

environment = Environment(loader=FileSystemLoader("templates/"))
environment = Environment(loader=FileSystemLoader("./"))

# tox.ini
template = environment.get_template("tox.ini.j2")
filename = f"tox.ini"
content = template.render(
    tox_exclude_src_files=tox_exclude_src_files
)
template = environment.get_template("tox.ini.j2")
with open(filename, mode="w", encoding="utf-8") as template_file:
    template_file.write(content)
    print(f"... wrote {filename}")

# pyproject.toml
template = environment.get_template("pyproject.toml.j2")
filename = f"pyproject.toml"
content = template.render(
    project_name = project_name,
    package_name = package_name,
    package_version = package_version,
    package_description = package_description,
    package_author = package_author,
    package_email = package_email
)
template = environment.get_template("pyproject.toml.j2")
with open(filename, mode="w", encoding="utf-8") as template_file:
    template_file.write(content)
    print(f"... wrote {filename}")

# hatch.toml
template = environment.get_template("hatch.toml.j2")
filename = f"hatch.toml"
content = template.render(
    package_name = package_name
)
template = environment.get_template("hatch.toml.j2")
with open(filename, mode="w", encoding="utf-8") as template_file:
    template_file.write(content)
    print(f"... wrote {filename}")


# run___init__.py  # 3 underscores then 2 underscores
template = environment.get_template("run___init__.py.j2")
filename = f"src/{project_name}/run/__init__.py"  # only 2 underscores
content = template.render(
    package_name = package_name
)
template = environment.get_template("run___init__.py.j2")
with open(filename, mode="w", encoding="utf-8") as template_file:
    template_file.write(content)
    print(f"... wrote {filename}")

# __about.py
template = environment.get_template("__about__.py.j2")
filename = f"src/{project_name}/__about__.py"
content = template.render(
    package_name = package_name,
    package_version = package_version
)
template = environment.get_template("__about__.py.j2")
with open(filename, mode="w", encoding="utf-8") as template_file:
    template_file.write(content)
    print(f"... wrote {filename}")