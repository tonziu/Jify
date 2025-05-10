# What it is
**J**obs **I** do **F**or **Y**ou is a Python module that I use to automate the creation of coding projects.

:warning:
Please be aware that it is a work in progress and is at its very early stages.

# What it offers

The first task that I automated is the creation of a C Project. I usually have to put manually some libraries or headers I frequently use, so I decided to build a configuration-based parser
that is able to fetch the right files and put them in a folder using the layout I would expect. To model my layout, I used a *CProject* class (it is just a set of folders and a **CMakeLists.txt** file really).

In the configuration, I add what I call **cpackages** to add a related set of files (e.g. headers and libraries). Since each package has a tag, I can then use it to add packages to my c project in an automated way.

The automation is even faster with **ctemplates**, which are just a collection of already existing packages. Take a look at an example below:

```python
import jify

dest_folder = YOUR_CHOICE
proj_name = YOUR_CHOICE

prj = jify.CProject(dest_folder, proj_name)
prj.init_from_template("GLFW_GLAD")
```
The output is a folder in **dest_folder** that contains the layout implemented by **CProject**. The example is using this configuration:
```python
[cpackage]
tag = "GLFW"
include_folder = "C:\thirdparty\glfw\include\GLFW\"
lib_file = "C:\thirdparty\glfw\build\src\Debug\glfw3.lib"
[cpackage]
tag = "GLAD"
include_folder = "C:\thirdparty\glad\"

[ctemplate]
tag = "GLFW_GLAD"
cpackage = "GLFW"
cpackage = "GLAD"
```
You can extend and customise this system in many ways, adding models that use packages in any way you like.
