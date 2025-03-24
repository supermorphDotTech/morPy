<img src="https://github.com/user-attachments/assets/38a7a1e8-2a55-4f42-95a8-691a1cd77586" alt="supermorph_morPy_alpha_badge_v001" style="max-width:66%; height:auto;">

More solutions. More insights. morPy.

Multiprocessing aided Python framework with integrated logging to database. Be the master of your app by analyzing runtime. Enjoy the comfort of runtime documentation ready for use in validated environments.

Feel free to comment, share and support this project!  

![License](https://img.shields.io/github/license/supermorphDotTech/morPy)
![GitHub commit activity (monthly)](https://img.shields.io/github/commit-activity/m/supermorphDotTech/morPy)

# v1.0.0c - Table of contents [≛](#4.) [⇩](#7.) <a name="toc"></a>

`1.` [Requirements and Dependencies](#1.)  
&nbsp;
└─│`1.1` [Microsoft Windows](#1.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`1.1.1` [Software Requirements](#1.1.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`1.1.2` [Setup Guidance](#1.1.2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`1.1.3` [Virtual Environment](#1.1.3)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`1.1.3.1` [Basic Setup](#1.1.3.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`1.1.3.2` [Install Dependencies](#1.1.3.2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`1.1.3.3` [Copy Packages to Virtual Environment](#1.1.3.3)  
`2.` [Versioning - α.β.γλ](#2.)  
`3.` [Parallelization](#3.)  
`4.` [≛ Shared App Dictionary](#4.)  
&nbsp;
└─│`4.1` [Introduction](#4.1)  
&nbsp;
└─│`4.2` [Navigating the App Dictionary](#4.2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`4.2.1` [Categorization & Sub-Dictionaries](#4.2.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`4.2.2` [App Dictionary Map](#4.2.2)  
`5.` [Dependency Visualization](#5.)  
&nbsp;
└─│`5.1` [Setup Dependency Visualization (Microsoft Windows)](#5.1)  
&nbsp;
└─│`5.2` [Visualize Dependencies (Microsoft Windows)](#5.2)  
`6.` [Security and Dependency Analysis](#6.)  
&nbsp;
└─│`6.1` [Scan installed packages against known vulnerabilities](#6.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`6.1.1` [Install required libraries](#6.1.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`6.1.2` [Scan Installed Packages](#6.1.2)  
&nbsp;
└─│`6.2` [Security Guidance](#6.2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`6.2.1` [Constant Security checks in productive environments](#6.2.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`6.2.2` [Lock Down Virtual Environments](#6.2.2)  
`7.` [Abbreviations](#7.)  

# 1. Requirements and Dependencies [⇧](#toc) <a name="1."></a>

## 1.1 Microsoft Windows [⇧](#toc) <a name="1.1"></a>

### 1.1.1 Software Requirements [⇧](#toc) <a name="1.1.1"></a>

| Dependency                                                                                                                                                                    | Requirement Description                                              |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| [![Python 3.10.11](https://img.shields.io/badge/Python-3.10.11+-blue.svg)](https://www.python.org/downloads/release/python-31011/)                                            | Oldest supported Python version. First implementation of match-case. |
| [![Microsoft Visual C++ BuildTools](https://img.shields.io/badge/Microsoft-Visual%20C++%20BuildTools-orange.svg)](https://visualstudio.microsoft.com/visual-cpp-build-tools/) | Build tools required for UltraDict pip install.                      |

### 1.1.2 Setup Guidance [⇧](#toc) <a name="1.1.2"></a>

`1.` Install Python with the option "Add python.exe to PATH" enabled.  
`2.` Install Microsoft Visual C++ BuildTools  
`2.1.` Select "Desktopdevelopment with C++"  
`3.` Install a virtual environment in your project path (see below)  
`3.1.` [Basic Setup](#1.1.3.1)  
`3.2.` [Install Dependencies](#1.1.3.2)  
`3.3.` [Copy Packages to Virtual Environment](#1.1.3.3)

### 1.1.3 Virtual Environment [⇧](#toc) <a name="1.1.3"></a>

*Compare with [freeCodeCamp.org](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)*

#### 1.1.3.1 Basic Setup [⇧](#toc) <a name="1.1.3.1"></a>

1.  Run PowerShell
2. Define the Python version

```PowerShell
$env:python_version = 312
$env:python_path = "$($env:userprofile)\AppData\Local\Programs\Python\Python$($env:python_version)"
$env:python_exe = "$($env:python_path)\python.exe"
```

3.  Navigate to `pip.exe` 
    If Python was installed in the user path, type

```PowerShell
cd "$($env:python_path)\Scripts"
```

4.  install the virtualenv library

```PowerShell
.\pip install virtualenv
```

5.  install tcl libraries

```PowerShell
.\pip install tcl
```

```PowerShell
.\pip install tk
```

6.  Setup the path to the Python project as an environment variable (for this PowerShell session only), i.e.

```PowerShell
$env:PythonProject = "C:\Projects\morPy"
```

7.  Navigate to the root folder of the Python project, i.e.

```PowerShell
cd $env:PythonProject
```

8.  Insert the virtual environment into the project.

```PowerShell
& "$env:python_exe" -m venv .venv-win
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
pip install defusedxml
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

```PowerShell
pip install pillow
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

This is merely an example, of how parallelization may look like. There is still freedom to change how exactly the app is orchestrated (i.e. by setting a limit of maximum concurrent processes in `.\lib\conf.py`).

![EN-morPy-parallelization-scheme-v1 0 0-darkmode](https://github.com/user-attachments/assets/4f460193-7a01-4c78-a501-16b99aea747b)

# 4. Shared App Dictionary [⇧](#toc) <a name="4."></a>

## 4.1 Introduction [⇧](#toc) <a name="4.1"></a>

At the heart of the morPy framework a program wide dictionary is available. Within this dictionary, all morPy functions and classes store their data to be used either globally, process-, thread, or task-wide. This dictionary is further divided into dictionaries (nested) to avoid naming conflicts and provide a categorization to potentially organize data in a streamlined way. Nested dictionaries were divided into `app` and `morpy`, whereas the latter is reserved for the morPy framework core.

The class of `app_dict` is, in dependency to the GIL, either a regular `dict` or an `UltraDict`. The latter ensures efficient shared memory (as much as possible) when spawning processes.

```Python
# Exemplary dev dictionary nesting
app_dict["global"]["app"]["my_project"] = {}
app_dict["global"]["app"]["my_project"].update({"key" : "value"})
```

## 4.2 Navigating the App Dictionary [⇧](#toc) <a name="4.2"></a>

### 4.2.1 Categorization & Sub-Dictionaries [⇧](#toc) <a name="4.2.1"></a>

***Relevant dictionaries for developers to be utilized and altered will be marked `dev` in the descriptions.***

```Python
app_dict
```

- Globally shared root dictionary

```Python
app_dict["loc"]
```

- sd-lvl-1 root for Localization

```Python
app_dict["loc"]["morpy"]
```

- Localization sd-lvl-2: morPy only

```Python
app_dict["loc"]["morpy_dbg"]
```

- Localization sd-lvl-2: morPy unit tests and general debugging only

```Python
app_dict["loc"]["app"]
```

- `dev`
- Localization sd-lvl-2: app specific only

```Python
app_dict["loc"]["app_dbg"]
```

- `dev`
- Localization sd-lvl-2: app specific debugging only

```Python
app_dict["conf"]
```

- `dev`
- sd-lvl-1 reserved for configuration and settings for runtime (see conf.py for the initialized configuration)

```Python
app_dict["sys"]
```

- sd-lvl-1 reserved for host, system and network information

```Python
app_dict["run"]
```

- sd-lvl-1 reserved for runtime and metrics information

```Python
app_dict["global"]
```

- sd-lvl-1 root for global data storage

```Python
app_dict["global"]["morpy"]
```

- sd-lvl-2 morPy core global data storage

```Python
app_dict["global"]["app"]
```

- `dev`
- sd-lvl-2 app global data storage

```Python
app_dict["proc"]
```

- sd-lvl-1 root for process and thread specific data storage

```Python
app_dict["proc"]["morpy"]
```

- sd-lvl-2 morPy core process specific data storage

```Python
app_dict["proc"]["morpy"]["Pn"]
```

- sd-lvl-3 morPy core thread specific data storage

```Python
app_dict["proc"]["app"]
```

- `dev`
- sd-lvl-2 app process specific data storage

```Python
app_dict["proc"]["app"]["Pn"]
```

- `dev`
- sd-lvl-3 app thread specific data storage

### 4.2.2 App Dictionary Map [⇧](#toc) <a name="4.2.2"></a>

*See [Abbreviations](#6.) for further explanations.*  
Pn ... Process with ID 'n'  
Tm ... Thread with ID 'm'

```Python
app_dict = [dict]{
    "loc" : [dict]{ # See ..\loc\
        "morpy" : [dict]{"key" : val,...}
        "morpy_dbg" : [dict]{"key" : val,...}
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
        "morpy" : [dict]{
            "m.op" : [dict]{"key" : val,...}
            "key" : val,...
        }
        "app" : [dict]{
            "m.op" : [dict]{"key" : val,...}
            "key" : val,...
        }
    }
    "proc" : [dict]{
        "morpy" : [dict]{
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

# 6. Security and Dependency Analysis [⇧](#toc) <a name="6."></a>

## 6.1 Scan installed packages against known vulnerabilities [⇧](#toc) <a name="6.1"></a>

### 6.1.1 Install required libraries [⇧](#toc) <a name="6.1.1"></a>

1.  Setup the path to the Python project as an environment variable (for this PowerShell session only), i.e.

```PowerShell
$env:PythonProject = "C:\Projects\morPy"
```

2.  Navigate to the root folder of the Python project, i.e.

```PowerShell
cd $env:PythonProject
```

3.  Activate the virtual environment:

```PowerShell
& "$env:PythonProject\.venv-win\scripts\activate.ps1"
```

4.  Install `pip-audit` (Scans your installed packages against known vulnerability databases):

```PowerShell
pip install pip-audit
```

5.  Install `safety` (Registration required):

```PowerShell
pip install safety; safety auth
```

### 6.1.2 Scan Installed Packages [⇧](#toc) <a name="6.1.2"></a>

6.  Run `pip-audit`:

```PowerShell
pip-audit
```

7.  Run `safety`:

```PowerShell
safety scan
```

8.  Check for CVE's

[CVEdetails.com - Python](https://www.cvedetails.com/version-list/10210/18230/1/Python-Python.html)  
[CVEdetails.com - Python Vulnerability Satistics](https://www.cvedetails.com/vendor/10210/Python.html)

## 6.2 Security Guidance [⇧](#toc) <a name="6.2"></a>

### 6.2.1 Constant Security checks in a productive environment [⇧](#toc) <a name="6.2.1"></a>

It is advisable to keep a clone of the Python virtual environment including all dependencies used in the production code on a non-critical server. The vulnerability Checks may then be automated to run at least once a day and send reports to the security dev team.

### 6.2.2 Lock Down Virtual Environments [⇧](#toc) <a name="6.2.2"></a>

Disallow any changes in the virtual environment to prevent the use of dangerous libraries. To do this, make the virtual environment a read-only directory and only allow for write-access to patch vulnerabilities.   
As an example, it is not advisory to allow installation of `jkuri/bore`, as it allows circumventing certain network security features.  

# 7. Abbreviations [⇧](#toc) <a name="7."></a>

| **Abbreviation** | **Context** | **Description** |
| --- | --- | --- |
| dev | Documentation | `dev` marks a (nested/shared) dictionary as relevant for developers. These datasections may be leveraged freely. |
| dict | Python Code | Python dictionary object |
| sdict | Python Code | Python dictionary object - sub-dictionary |
| sd-lvl-n | Python Code | Python dictionary object - sub-dictionary at level n relative to the root dictionary |
| m.op | Python Code | Operation identifier string (module.operation) |
| "key" | Python Code | Generic key of a Python dictionary |
| val | Python Code | Generic value or variable |
