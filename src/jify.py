import os
import shutil
import ast

def welcome():
    print("### Hello from Jify.")

def mkdir(path):
    if os.path.exists(path):
        print(f"### Directory already exists: {path}")
        return
    print(f"### Creating '{path}'...")
    os.makedirs(path)

def touch(path, filename, clear=True):
    if not clear and os.path.exists(path + filename):
        print(f"### File already exists: {path + filename}")

    print(f"### Creating '{filename}' in '{path}'")
    with open(path + filename, 'w') as f:
        pass

def copy_file(src, dest):
    if not os.path.exists(src):
        print(f"### File does not exist: {src}")
        return
    if not os.path.isfile(src):
        print(f"### It is not a file: {src}")
        return
    if not os.path.exists(dest):
        mkdir(dest)

    print(f"### Copying file '{src}' into '{dest}'")
    try:
        shutil.copy(src, dest)
    except Exception as e:
        print(f"### copy_file() failed: {e}")

def copy_dir(src, dest):
    if not os.path.exists(src):
        print(f"### Directory does not exist: {src}")
        return
    if not os.path.isdir(src):
        print(f"### It is not a directory: {src}")
        return
    if not os.path.exists(dest):
        mkdir(dest)

    src = os.path.normpath(src)
    print(f"### Copying directory '{src}' into '{dest}'")
    try:
        dest = os.path.join(dest, os.path.basename(src))
        shutil.copytree(src, dest, dirs_exist_ok=1)
    except Exception as e:
        print(f"### copy_dir() failed: {e}")

def append_to_file(filename, content):
    if not os.path.isfile(filename):
        print(f"### It is not a valid file: {filename}")
        return
    with open(filename, 'a') as f:
        print(f"### Editing file: {filename}")
        f.write(content)

def clear_file(filename):
    if not os.path.exists(filename):
        print(f"### Nothing to clear: {filename}")
        return
    with open(filename, 'w') as f:
        pass

def find_cpackage(target_tag):
    with open('jify.config', 'r') as config:
        lines = config.readlines()

    in_section = False
    include_folder = ""
    lib_files = []
    found = False
    tag = ""

    for line in lines:
        line = line.strip()
        if line == "[cpackage]" and found:
            if found: #we are done parsing
                break
            else:
                continue

        if line.startswith("tag") and not found:
            tag = CPackage.parse_tag(line)
            if tag == target_tag:
                found = True
                continue

        if found:
            if line.startswith("include_folder"):
                include_folder = CPackage.parse_include_folder(line)
            if line.startswith("lib_file"):
                lib_file = CPackage.parse_lib_file(line)
                lib_files.append(lib_file)

    if not found:
        return None

    return CPackage(tag, include_folder, lib_files)

def find_ctemplate(target_tag):
    with open('jify.config', 'r') as config:
        lines = config.readlines()

    in_section = False
    cpackages = []

    found = False
    tag = ""

    for line in lines:
        line = line.strip()
        if line == "[ctemplate]" and found:
            if found: #we are done parsing
                break
            else:
                continue

        if line.startswith("tag") and not found:
            tag = CTemplate.parse_tag(line)
            if tag == target_tag:
                found = True
                continue

        if found:
            if line.startswith("cpackage"):
                cpackage_name = CTemplate.parse_cpackage_tag(line)
                cpackage = find_cpackage(cpackage_name)
                if cpackage is not None:
                    cpackages.append(cpackage)

    if not found:
        return None

    return CTemplate(tag, cpackages)

def parse_config_string(line, name):
    _, value = line.split(" = ")
    value = value.strip('"')
    return value

class CPackage:
    def __init__(self, tag, include_folder, lib_files):
        self.tag = tag
        self.include_folder = include_folder
        self.lib_files = lib_files

    def parse_tag(line):
        return parse_config_string(line, "tag")

    def parse_include_folder(line):
        return parse_config_string(line, "include_folder")

    def parse_lib_file(line):
        return parse_config_string(line, "lib_file")

class CTemplate:
    def __init__(self, tag, cpackages):
        self.tag = tag
        self.cpackages = cpackages

    def parse_tag(line):
        return parse_config_string(line, "tag")

    def parse_cpackage_tag(line):
        return parse_config_string(line, "cpackage")

class CProject:
    def __init__(self, dest_folder, name):
        self.name = name
        self.prj_folder = dest_folder + name + "/"
        self.include_folder = self.prj_folder + "include/"
        self.src_folder = self.prj_folder + "src/"
        self.lib_folder = self.prj_folder + "lib/"
        self.build_folder = self.prj_folder + "build/"
        self.cmakelists_file = self.prj_folder + "CMakeLists.txt"

        mkdir(self.include_folder)
        mkdir(self.lib_folder)
        mkdir(self.src_folder)

        self._bare_cmakelists()

    def copy_folder_to_include(self, folder):
        copy_dir(folder, self.include_folder)

    def copy_folder_to_lib(self, folder):
        copy_dir(folder, self.lib_folder)

    def copy_file_to_include(self, file):
        copy_file(file, self.include_folder)

    def copy_file_to_lib(self, file):
        copy_file(file, self.lib_folder)

    def _bare_cmakelists(self):
        touch(self.prj_folder, "CMakeLists.txt")
        append_to_file(self.cmakelists_file, "CMAKE_MINIMUM_REQUIRED(VERSION XXX)\n")
        append_to_file(self.cmakelists_file, f"PROJECT({self.name})\n")

    def add_cpackage(self, package_name):
        package = find_cpackage(package_name)
        if package is None:
            print(f"### Package not found: {package_name}")
            return

        if package.include_folder:
            self.copy_folder_to_include(package.include_folder)

        for lib_file in package.lib_files:
            if not lib_file:
                continue
            self.copy_file_to_lib(lib_file)

    def init_from_template(self, ctemplate_tag):
        template = find_ctemplate(ctemplate_tag)
        if template is not None:
            for package in template.cpackages:
                self.add_cpackage(package.tag)

if __name__ == "__main__":
    welcome()

