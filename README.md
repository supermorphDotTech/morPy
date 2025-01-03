[<img src="https://github.com/user-attachments/assets/0e92f76c-67db-4ff6-8e58-9ab77a9a6e8e" alt="supermorph_PixelSnake_logo_v001" width="812" height="182" class="jop-noMdConv">](https://www.supermorph.tech/)  
<br/><br/><br/><br/><img src="https://github.com/user-attachments/assets/51fd6975-d4cd-4123-b708-552e8fee9c1a" alt="supermorph_morPy_github_v001" width="812" height="364" class="jop-noMdConv">

More solutions. More insights. morPy.

Multiprocessing aided Python framework with integrated logging to database. Be the master of your app by analyzing runtime. Enjoy the comfort of runtime documentation ready for use in validated environments.

Feel free to comment, share and support this project.  
Visit me on [supermorph.tech](https://www.supermorph.tech/) to get in touch with me.

# v1.0.0c - Table of contents <a name="toc"></a>

`1.` [Requirements and Dependencies](#1.) <br>
`1.1` [Microsoft Windows](#1.1) <br>
`1.1.1` [Software Requirements](#1.1.1) <br>
`1.1.2` [Setup Guidance](#1.1.2) <br>
`1.1.3` [Virtual Environment](#1.1.3) <br>
`1.1.3.1` [Basic Setup](#1.1.3.1) <br>
`1.1.3.2` [Install Dependencies](#1.1.3.2) <br>
`1.1.3.3` [Copy Packages to Virtual Environment](#1.1.3.3) <br>
`2.` [Versioning - α.β.γλ](#2.) <br>
`3.` [Parallelization](#3.) <br>
`4.` [Shared App Dictionary](#4.) <br>
`4.1` [Introduction](#4.1) <br>
`4.2` [Navigating the App Dictionary](#4.2) <br>
`4.2.1` [Categorization & Sub-Dictionaries](#4.2.1) <br>
`4.2.2` [App Dictionary Map](#4.2.2) <br>
`5.` [Dependency Visualization](#5.) <br>
`5.1` [Setup Dependency Visualization (Microsoft Windows)](#5.1) <br>
`5.2` [Visualize Dependencies (Microsoft Windows)](#5.2) <br>
`6.` [Abbreviations](#6.) <br>

# 1. Requirements and Dependencies <a name="1."></a>

## 1.1 Microsoft Windows [⇧](#toc) <a name="1.1"></a>

### 1.1.1 Software Requirements [⇧](#toc) <a name="1.1.1"></a>

| Depency | Requirements |
| --- | --- |
| Python | [Python 3.10.11](https://www.python.org/downloads/release/python-31011/) |
| UltraDict | [Microsoft Visual C++ BuildTools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) |

### 1.1.2 Setup Guidance [⇧](#toc) <a name="1.1.2"></a>

`1.` Install Python with the option "Add python.exe to PATH" enabled.<br>
`2.` Install Microsoft Visual C++ BuildTools<br>
`2.1.` Select "Desktopdevelopment with C++"<br>
`3.` Install a virtual environment in your project path (see below)<br>
`3.1.` [Basic Setup](#1.1.3.1)<br>
`3.2.` [Install Dependencies](#1.1.3.2)<br>
`3.3.` [Copy Packages to Virtual Environment](#1.1.3.3)<br>

### 1.1.3 Virtual Environment [⇧](#toc) <a name="1.1.3"></a>

*Compare with [freeCodeCamp.org](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)*

#### 1.1.3.1 Basic Setup [⇧](#toc) <a name="1.1.3.1"></a>

1.  Run PowerShell
2.  Navigate to `pip.exe`  
    If Python was installed in the user path, type

```PowerShell
cd $env:userprofile\AppData\Local\Programs\Python\Python313\Scripts
```

3.  install the virtualenv library

```PowerShell
.\pip install virtualenv
```

4.  install tcl libraries

```PowerShell
.\pip install tcl
```

```PowerShell
.\pip install tk
```

5.  Setup the path to the Python project as an environment variable (for this PowerShell session only), i.e.

```PowerShell
$env:PythonProject = "C:\Projects\morPy"
```

6.  Navigate to the root folder of the Python project, i.e.

```PowerShell
cd $env:PythonProject
```

7.  Insert the virtual environment into the project.

```PowerShell
python -m venv .venv-win
```

If an error occurs indicating `python<version> was not recognized as a cmdlet`, it is likely, that Python was not installed with the option "Add python.exe to PATH".

#### 1.1.3.2 Install Dependencies [⇧](#toc) <a name="1.1.3.2"></a>

1.  Navigate to the root folder of the Python project (if not still there), i.e.

```PowerShell
cd $env:PythonProject
```

2.  Activate the virtual environment:

```PowerShell
& "$env:PythonProject\.venv-win\scripts\activate.ps1"
```

3.  Upgrade Pip

```PowerShell
python.exe -m pip install --upgrade pip
```

4.  Run the following pip installations one by one:

```PowerShell
pip install psutil
```

```PowerShell
pip install chardet
```

```PowerShell
pip install openpyxl
```

```PowerShell
pip install atomics
```

```PowerShell
pip install ultradict
```

```PowerShell
pip install ultraimport
```

#### 1.1.3.3 Copy Packages to Virtual Environment [⇧](#toc) <a name="1.1.3.3"></a>

*Manual installation of* `tcl` *and* `tk` *in the virtual environment. This needed, as tcl does not install correctly, otherwise.*

1.  Navigate to the tcl installation folder and copy it to the virtual environment, i.e.:

`\> copy tcl`

```PowerShell
$env:userprofile\AppData\Local\Programs\Python\Python313\tcl\tcl8.6
```

`\> copy tk`

```PowerShell
$env:userprofile\AppData\Local\Programs\Python\Python313\tcl\tk8.6
```

`\> paste to`

```PowerShell
$env:PythonProject\.venv-win\Lib\site-packages\Tcl
```

*Create the* `tcl` *subfolder if it does not exist.*

# 2. Versioning - α.β.γλ [⇧](#toc) <a name="2."></a>

| Symbol | Description |
| --- | --- |
| α   | Major Version.  <br>No downward compatibility: CRITICAL errors expected. |
| β   | Improvement Version.  <br>Limited downward compatibility: WARNING and DENIED messages expected. |
| γ   | Bugfix Version.  <br>Full downward compatibility. |
| λ   | Version status.  <br>*None*: Release version  <br>*a*: Alpha version with minor bugs for public testing.  <br>*b*: Beta version with potential showstopper bugs for internal testing.  <br>*c*: Gamma version. Development. Not presentable to public. |

# 3. Parallelization [⇧](#toc) <a name="3."></a>

The parallelization in morPy is done utilizing an orchestration process with which the entire program starts and ends. The process ID "0" is always reserved for the orchestration process. It will take care of logging and is reserved for tasks with a priority in between 0 and 10 (smaller numbers for higher priority). All app tasks will automatically receive a higher number (lower priority) than morPy reserved tasks. In case a priority is corrected, a warning will be raised.

This is merely an example, of how parallelization may look like. There is still freedom to change how exactly the app is orchestrated (i.e. by setting a limit of maximum concurrent processes in `.\lib\mpy_conf.py`).

![EN-morPy-parallelization-scheme-v1 0 0-darkmode](https://github.com/user-attachments/assets/4f460193-7a01-4c78-a501-16b99aea747b)

# 4. Shared App Dictionary [⇧](#toc) <a name="4."></a>

## 4.1 Introduction [⇧](#toc) <a name="4.1"></a>

At the heart of the morPy framework a program wide dictionary is available. Within this dictionary, all morPy functions and classes store their data to be used either globally, process-, thread, or task-wide. This dictionary is further divided into dictionaries to avoid naming conflicts and provide a categorization to potentially organize data in a streamlined way. Nested dictionaries were divided into `app` and `mpy`, whereas the latter is reserved for the morPy framework.

The `app_dict` is an instanciated custom subclass of the Python `dict`\-class. For details on the sub-class `cl_mpy_dict` see it's own section. The pattern of instanciating such dictionary is

```Python
app_dict = cl_mpy_dict(name="app_dict", access="locked")
app_dict._update_self(access="tightened")
```

Developer created sub-dictionaries may mirror this way of dictionary creation, integrating it into the `app_dict`.

```Python
# Examplary dev dictionary nesting
app_dict["run"]["add_data"] = cl_mpy_dict(name="app_dict[run][add_data]")
```

## 4.2 Navigating the App Dictionary [⇧](#toc) <a name="4.2"></a>

### 4.2.1 Categorization & Sub-Dictionaries [⇧](#toc) <a name="4.2.1"></a>

***Relevant dictionaries for developers to be utilized and altered will be marked `dev` in the descriptions.***

Sub-dictionaries are hardened by specifiying the access type, to streamline the utilization of `app_dict` as designed. The access types are  
`normal` - works like any Python dictionary
`tightened` - keys can not be added to or removed from the dict. Values may be altered, however.
`locked` - dictionary is in lockdown and can not be altered in any way except, referenced UltraDict's can still be altered.
An asterisk as in `*tightened` indicates, that the access type is circumvented by morPy core functionalities. Nested dictionaries not mentioned explicitly (comapare with "App Dictionary Map") always are of access type `normal`.

```Python
app_dict
```

- `tightened`
- Globally shared root dictionary

```Python
app_dict["loc"]
```

- `locked`
- sd-lvl-1 root for Localization

```Python
app_dict["loc"]["mpy"]
```

- `locked`
- Localization sd-lvl-2: morPy only

```Python
app_dict["loc"]["mpy_dbg"]
```

- `locked`
- Localization sd-lvl-2: morPy unit tests and general debugging only

```Python
app_dict["loc"]["app"]
```

- `dev`
- `locked`
- Localization sd-lvl-2: app specific only

```Python
app_dict["loc"]["app_dbg"]
```

- `dev`
- `locked`
- Localization sd-lvl-2: app specific debugging only

```Python
app_dict["conf"]
```

- `dev`
- `locked`
- sd-lvl-1 reserved for configuration and settings for runtime (see mpy_conf.py for the initialized configuration)

```Python
app_dict["sys"]
```

- `locked`
- sd-lvl-1 reserved for host, system and network information

```Python
app_dict["run"]
```

- `tightened`
- sd-lvl-1 reserved for runtime and metrics information

```Python
app_dict["global"]
```

- `tightened`
- sd-lvl-1 root for global data storage

```Python
app_dict["global"]["mpy"]
```

- `normal`
- sd-lvl-2 morPy core global data storage

```Python
app_dict["global"]["app"]
```

- `dev`
- `normal`
- sd-lvl-2 app global data storage

```Python
app_dict["proc"]
```

- `tightened`
- sd-lvl-1 root for process and thread specific data storage

```Python
app_dict["proc"]["mpy"]
```

- `*tightened`
- sd-lvl-2 morPy core process specific data storage
- Even though this dictionary tightened, the nested process specific dictionaries are created by the multiprocessing priority queue and deleted at process exit.

```Python
app_dict["proc"]["mpy"]["Pn"]
```

- `normal`
- sd-lvl-3 morPy core thread specific data storage

```Python
app_dict["proc"]["app"]
```

- `dev`
- `*tightened`
- sd-lvl-2 app process specific data storage
- Even though this dictionary tightened, the nested process specific dictionaries are created by the multiprocessing priority queue and deleted at process exit.

```Python
app_dict["proc"]["app"]["Pn"]
```

- `dev`
- `normal`
- sd-lvl-3 app thread specific data storage

### 4.2.2 App Dictionary Map [⇧](#toc) <a name="4.2.2"></a>

*See [Abbreviations](#6.) for further explanations.*  
Pn ... Process with ID 'n'  
Tm ... Thread with ID 'm'

```Python
app_dict = [dict]{
    "loc" : [dict]{ # See ..\loc\
        "mpy" : [dict]{"key" : val,...}
        "mpy_dbg" : [dict]{"key" : val,...}
        "app" : [dict]{"key" : val,...}
        "app_dbg" : [dict]{"key" : val,...}
    }
    "conf" : [dict]{
    }
    "sys" : [dict]{
        "mproc" : [dict]{
            "procs_available" : [int] n
        }
        "mthread" : [dict]{
            "threads_available" : [int] m
        }
    }
    "run" : [dict]{
        "m.op" : [dict]{"key" : val,...}
        "key" : val,...
    }
    "global" [dict]{
        "mpy" : [dict]{
            "m.op" : [dict]{"key" : val,...}
            "key" : val,...
        }
        "app" : [dict]{
            "m.op" : [dict]{"key" : val,...}
            "key" : val,...
        }
    }
    "proc" : [dict]{
        "mpy" : [dict]{
            "P0" : [dict]{
                "T0" : [dict]{
                    "m.op" : [dict]{"key" : val,...}
                    "key" : val,...
                }
                "Tm" : [dict]{
                    "m.op" : [dict]{"key" : val,...}
                    "key" : val,...
                }
                "m.op" : [dict]{"key" : val,...}
                "key" : val,...
            }
            "Pn" [dict]{
                "T0" : [dict]{
                    "m.op" : [dict]{"key" : val,...}
                    "key" : val,...
                }
                "Tm" : [dict]{
                    "m.op" : [dict]{"key" : val,...}
                    "key" : val,...
                }
                "m.op" : [dict]{"key" : val,...}
                "key" : val,...
            }
        }
        "app" : [dict]{
            "P0" : [dict]{
                "T0" : [dict]{
                    "m.op" : [dict]{"key" : val,...}
                    "key" : val,...
                }
                "Tm" : [dict]{
                    "m.op" : [dict]{"key" : val,...}
                    "key" : val,...
                }
                "m.op" : [dict]{"key" : val,...}
                "key" : val,...
            }
            "Pn" [dict]{
                "T0" : [dict]{
                    "m.op" : [dict]{"key" : val,...}
                    "key" : val,...
                }
                "Tm" : [dict]{
                    "m.op" : [dict]{"key" : val,...}
                    "key" : val,...
                }
                "m.op" : [dict]{"key" : val,...}
                "key" : val,...
            }
        }
    }
}
```

# 5. Dependency Visualization [⇧](#toc) <a name="5."></a>

For dependency visualization `pydeps` is used, which itself requires `graphviz` for the actual visualization.

## 5.1 Setup Dependency Visualization (Microsoft Windows) [⇧](#toc) <a name="5.1"></a>

**! You need winget installed !**  
(alternatively install the packages manually, that would outherwise require winget)

1.  Setup the path to the Python project as an environment variable (for this PowerShell session only), i.e.

```PowerShell
#Only if $env:PythonProject is not defined yet
$env:PythonProject = "C:\Projects\morPy"
```

2.  Navigate to the root folder of the Python project (if not still there), i.e.

```PowerShell
#Only if $env:PythonProject is not defined yet
cd $env:PythonProject
```

3.  Activate the virtual environment:

```PowerShell
& "$env:PythonProject\.venv-win\scripts\activate.ps1"
```

4.  Run the following pip installations one by one:

```PowerShell
pip install pydeps
```

```PowerShell
pip install graphviz
```

5.  Install `graphviz` with winget.

```PowerShell
winget install graphviz
```

6.  Add environment variables in order to make the "dot"-command from `graphviz` available to `pydeps`. You may have to start a new PowerShell session for the changes to take effect.

```PowerShell
#For all users (needs admin privileges)
[System.Environment]::SetEnvironmentVariable("Path", $([System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";C:\Program Files\Graphviz\bin"), [System.EnvironmentVariableTarget]::Machine)
```

```PowerShell
#For the current user
[System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Graphviz\bin", [System.EnvironmentVariableTarget]::User)
```

## 5.2 Visualize Dependencies (Microsoft Windows) [⇧](#toc) <a name="5.2"></a>

1.  Setup the path to the Python project as an environment variable (for this PowerShell session only), i.e.

```PowerShell
#Only if $env:PythonProject is not defined yet
$env:PythonProject = "C:\Projects\morPy"
```

2.  Navigate to the root folder of the Python project (if not still there), i.e.

```PowerShell
#Only if $env:PythonProject is not defined yet
cd $env:PythonProject
```

3.  Activate the virtual environment:

```PowerShell
& "$env:PythonProject\.venv-win\scripts\activate.ps1"
```

4.  Run `pydeps` for morPy.

```PowerShell
pydeps --cluster --rankdir "LR" --include-missing ".\"
```

5.  To visualize cyclic imports, run

```PowerShell
#Visualize cyclic imports
 pydeps --cluster --rankdir "LR" --include-missing --show-cycles ".\"
```

# 6. Abbreviations [⇧](#toc) <a name="6."></a>

| **Abbreviation** | **Context** | **Description** |
| --- | --- | --- |
| dev | Documentation | `dev` marks a (nested/shared) dictionary as relevant for developers. These datasections may be leveraged freely. |
| normal | app_dict._access | The (nested/shared) dictionary works like any dict-type. |
| tightened | app_dict._access | In the (nested/shared) dictionary, keys can not be added or popped from the dict. Values may be altered, however. |
| locked | app_dict._access | The (nested/shared) dictionary is in lockdown and can not be altered in any way except, referenced UltraDict's can still be altered. |
| dict | Python Code | Python dictionary object |
| sdict | Python Code | Python dictionary object - sub-dictionary |
| sd-lvl-n | Python Code | Python dictionary object - sub-dictionary at level n relative to the root dictionary |
| m.op | Python Code | Operation identifier string (module.operation) |
| "key" | Python Code | Generic key of a Python dictionary |
| val | Python Code | Generic value or variable |
