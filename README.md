<img src="https://github.com/user-attachments/assets/38a7a1e8-2a55-4f42-95a8-691a1cd77586" alt="supermorph_morPy_alpha_badge_v001" style="max-width:66%; height:auto;">

More solutions. More insights. morPy.

Python multiprocessing aided app foundation. Feature rich and easy to learn.

Feel free to comment, share and support this project!  

![License](https://img.shields.io/github/license/supermorphDotTech/morPy)
![GitHub commit activity (monthly)](https://img.shields.io/github/commit-activity/m/supermorphDotTech/morPy)

# v1.0.0a - Table of contents [≛](#4.) [⇩](#7.) <a name="toc"></a>

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
&nbsp;
└─│`3.1` [Reserved Orchestrator Heap Priorities](#3.1)  
&nbsp;
└─│`3.2` [Parallelization Map](#3.2)  
`4.` [≛ Shared App Dictionary](#4.)  
&nbsp;
└─│`4.1` [Introduction](#4.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`4.1.1` [Limitations of the Shared App Dictionary](#4.1.1)  
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
└─│`6.1` [Known Vulnerabilities of morPy](#6.1)  
&nbsp;
└─│`6.2` [Scan installed packages against known vulnerabilities](#6.2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`6.2.1` [Install required libraries](#6.2.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`6.2.2` [Scan Installed Packages](#6.2.2)  
&nbsp;
└─│`6.3` [Security Guidance](#6.3)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`6.3.1` [Constant Security checks in productive environments](#6.3.1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
└─│`6.3.2` [Lock Down Virtual Environments](#6.3.2)  
`7.` [Abbreviations](#7.)  

# 1. Requirements and Dependencies [⇧](#toc) <a name="1."></a>

## 1.1 Microsoft Windows [⇧](#toc) <a name="1.1"></a>

### 1.1.1 Software Requirements [⇧](#toc) <a name="1.1.1"></a>

| Dependency                                                                                                                                                                    | Requirement Description                                                         |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| [![Python 3.10.11](https://img.shields.io/badge/Python-3.10.11+-blue.svg)](https://www.python.org/downloads/release/python-31011/)                                            | Oldest supported Python version. Introduction of match-case and Union operator. |
| [![Microsoft Visual C++ BuildTools](https://img.shields.io/badge/Microsoft-Visual%20C++%20BuildTools-orange.svg)](https://visualstudio.microsoft.com/visual-cpp-build-tools/) | Build tools required for UltraDict pip install.                                 |

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
$env:python_version = 310   # Python version indication
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

If an error occurs indicating `python<version> was not recognized as a cmdlet`, it is likely, that Python was not
installed with the option "Add python.exe to PATH".

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
pip install qrcode
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

*Manual copy of* `tcl` *and* `tk` *from Python installation to the virtual environment. This is required, as tcl does
not install correctly, otherwise.*

1.  Navigate to the tcl installation folder and copy it to the virtual environment.
2. (*Change `Python312` to your Python version installed in the virtual environment!*)

Copy the following path into your Windows Explorer path bar and press ENTER.
```
%USERPROFILE%\AppData\Local\Programs\Python\Python312\tcl
```

Copy the following subdirectories.
```
.\tcl8.6
.\tk8.6
```

Navigate to the virtual environment and paste the directories. Your may have to create a new folder `.\Tcl`.
(*Change `PROJECT` to your Python project path!*)
```
PROJECT\.venv-win\Lib\site-packages\Tcl
```

# 2. Versioning - α.β.γλ [⇧](#toc) <a name="2."></a>

| Symbol | Description                                                                                                                                                                                                                                             |
| --- |---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| α   | Major Version.  <br>No downward compatibility requires architectural changes.                                                                                                                                                                           |
| β   | Improvement Version.  <br>Limited downward compatibility. "Easy" modifications required.                                                                                                                                                                |
| γ   | Bugfix Version.  <br>Full downward compatibility.                                                                                                                                                                                                       |
| λ   | Version status.  <br>*None*: Golden release version  <br>*a*: Alpha version with minor bugs for public testing.  <br>*b*: Beta version with potential showstopper bugs for public testing.  <br>*c*: Gamma version. For developmental internal testing. |

# 3. Parallelization [⇧](#toc) <a name="3."></a>

The parallelization in morPy is done utilizing an orchestration process with which the entire program starts and ends.
The process ID "0" is reserved for the orchestration process. It will take care of logging and is reserved for tasks
with a priority smaller than 0 (smaller numbers equal higher priority). All app tasks priorities will default to 100,
if not specified and will be autocorrected if set below 0. In case a priority is corrected, a warning will be raised.

## Reserved Orchestrator Heap Priorities [⇧](#toc) <a name="3.1"></a>

| Priority | Operation                           | Description                                                                |
|----------|-------------------------------------|----------------------------------------------------------------------------|
| -100     | lib.decorators.log()                | Absolute highest priority reserved for logging. Prevents build up of heap. |
| -90      | lib.mp.MorPyOrchestrator._app_run() | Task of the actual app. Only enqueued once after initialization.           |
| \[100\]  | morPy.process_q()                   | Default priority of a new child process.                                   |

## Parallelization Map [⇧](#toc) <a name="3.2"></a>

![EN-morPy-parallelization-scheme-v1 0 0-darkmode](https://github.com/user-attachments/assets/4f460193-7a01-4c78-a501-16b99aea747b)

# 4. Shared App Dictionary [⇧](#toc) <a name="4."></a>

## 4.1 Introduction [⇧](#toc) <a name="4.1"></a>

To share data across processes, morPy utilizes [`UltraDict`](https://github.com/ronny-rentner/UltraDict/tree/main) to
efficiently and atomically acquire locks, read and write data across spawned child processes. In single process mode,
the framework falls back to the `dict` type to keep performance as high as possible.

The class of `app_dict` is, in dependency to how many processes are configured in settings, either a regular `dict` in
single process mode or an `UltraDict` if more than one process shall be leveraged. The latter ensures efficient shared
memory (as much as possible) and a way to share data between spawned processes.

```Python
# Exemplary dev dictionary nesting
app_dict["global"]["app"]["my_project"] = {}
app_dict["global"]["app"]["my_project"].update({"key" : "value"})
```

## 4.1.1 Limitations of the Shared App Dictionary [⇧](#toc) <a name="4.1.1"></a>

For more complex types like `set()` and `list()` (and others), in-place modifications may not work
as expected. Methods like `.pop()` are not pickled and synchronized across processes. To mitigate issues,
perform *copy-modify-write* sequences or use immutable values associated to their regarding keys.
As an example, you may choose to define a nested shared dictionary instead of a `set()`, with the values
being `None` if not required.

Storing classes in `app_dict` to share them across processes may fail, because it's attributes
are not propagated reliably to other processes. In multiprocessing contexts, a classes attributes are not
shared like other values and types. Instead, if attributes have to be accessible by other processes, construct
shared dictionaries to achieve that. Make sure to avoid infinite recursions by creating a new
shared dict, that is not nested in app_dict.
This means, that you may have pseudo-attributes in your class addressing
`app_dict["..."]["..."]`, instead of references to self.

*If synchronization can not be achieved*, it is recommended to stick with simple key-value-pairs in `app_dict` with
proxy functions transforming the data instead of more complex types.

## 4.2 Navigating the App Dictionary [⇧](#toc) <a name="4.2"></a>

### 4.2.1 Categorization & Sub-Dictionaries [⇧](#toc) <a name="4.2.1"></a>

***Relevant dictionaries for developers to beleveraged will be marked `dev` in the descriptions.***

```Python
# Root dictionary. Data may be stored in here to be shared across processes.
app_dict
```

» `dev`

```Python
# Nested dictionary for morPy core functionality. Keep it and it's nested dictionaries untouched.
app_dict["morpy"]
```

```Python
# Stored information from conf.py
app_dict["morpy"]["conf"]
```

» `dev`

```Python
# Nested dictionary serving as a shelf for child processes to put tasks in. These shelved tasks will be transferred into the heap by the orchestrator and removed from the dictionary in doing so.
app_dict["morpy"]["heap_shelf"]
```

```Python
# Nested dictionary storing information on which log levels have to be logged or ignored. Initialized once, improves performance.
app_dict["morpy"]["logs_generate"]
```

```Python
# Nested dictionary reserved for the orchestrator.
app_dict["morpy"]["orchestrator"]
```

```Python
# Nested dictionary with buffered references to  active processes.
app_dict["morpy"]["proc_refs"]
```

```Python
# Nested dictionary with buffered references to  waiting processes. It stores {PID : shelf}, where shelf may be filled with a task by the orchestrator. Massively reduces multiprocessing overhead.
app_dict["morpy"]["proc_waiting"]
```

```Python
# Nested dictionary storing system specific information (i.e. operating system, logical CPUs)
app_dict["morpy"]["sys"]
```

```Python
# Nested dictionary holding the nested dictionaries for localized messages.
app_dict["loc"]
```

```Python
# Nested dictionary holding the localized messages for the morPy framework.
app_dict["loc"]["morpy"]
```

» Data initialized from `loc.morPy_[LANG].py`, where `LANG` is the localization (i.e. 'en_US').

```Python
# Nested dictionary holding the localized messages for the morPy framework unit tests.
app_dict["loc"]["morpy_dbg"]
```

» Data initialized from `loc.morPy_[LANG].py`, where `LANG` is the localization (i.e. 'en_US').

```Python
# Nested dictionary holding the localized messages for the developed app.
app_dict["loc"]["app"]
```

» `dev`\
» Data initialized from `loc.app_[LANG].py`, where `LANG` is the localization (i.e. 'en_US').

```Python
# Nested dictionary holding the localized messages for the developed apps unit tests.
app_dict["loc"]["app_dbg"]
```

» `dev`\
» Data initialized from `loc.app_[LANG].py`, where `LANG` is the localization (i.e. 'en_US').

### 4.2.2 App Dictionary Map [⇧](#toc) <a name="4.2.2"></a>

Following is a map of `app_dict` illustrating how it is organized. The standard nested dictionaries are not meant to be
tampered with, as that may lead to unexpected behaviour and all kinds of issues and crashes. Dictionaries which are
only marked with a `*` will not exist in a single process context.
*See [Abbreviations](#6.) for further explanations.*  

```Python
app_dict = [dict | UltraDict]{
    "morpy":    [dict | UltraDict]{
        "conf":             [dict | UltraDict]  # Copy of lib.conf.settings()
       *"heap_shelf":       [UltraDict]         # Shelf for child processes to put tasks in. Will be picked up by the orchestrator.
        "logs_generate":    [dict | UltraDict]  # Log levels and their on/off switches. Performance improvement.
        "orchestrator":     [dict | UltraDict]  # Space reserved for the morpy orchestrator.
       *"proc_refs":        [UltraDict]         # Buffer of references to child processes spawned.
       *"proc_waiting":     [UltraDict]         # References to waiting processes which may receive a task.
        "sys":              [dict | UltraDict]  # Data regarding the machine running morPy.
        "processes_max":    [int]               # Maximum processes leveraged during runtime.
       *"proc_available":   [UltraDict]         # Pool of available processes which may be spawned.
       *"proc_busy":        [UltraDict]         # Pool of running processes.
       *"proc_joined":      [bool]              # Flag signaling that all processes are joined and may be released.
        "proc_master":      [int]               # Process ID of the master process.
        "interrupt":        [bool]              # Flag to signal all processes to wait. On release terminate or continue.
        "exit":             [bool]              # Flag to signal app exit. All processes will terminate as soon as possible.
        "init_complete"     [bool]              # Is True, once app transitioned from app.init() into app.run().
    }
    "loc":      [dict | UltraDict]{             # See ..\loc\
        "morpy":            [dict | UltraDict]  # Localization of morPy messages
        "morpy_dbg":        [dict | UltraDict]  # Localization of morPy unit test messages
        "app":              [dict | UltraDict]  # Localization of app messages
        "app_dbg":          [dict | UltraDict]  # Localization of app unit test messages
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

## 6.1 Known Vulnerabilities of morPy [⇧](#toc) <a name="6.1"></a>

### 6.1.1 Code Insertion [⇧](#toc) <a name="6.1.1"></a>

I f an attacker gains access to the machine on which morPy is running, it is possible for the
attacker to query through shared memory segments and identify those holding the UltraDict
instances `app_dict["morpy"]["heap_shelf"]` or `app_dict["morpy"]["proc_waiting"]` of currently
running apps. In that case, functions can be written into either of those which will then be picked
up for execution. The shared memory segments are obscured by their names to harden a little against
this threat. It is also noteworthy, that the inserted code must adhere to the morPy templates
and be importable by the interpreter in order to be executed successfully. This issue will
be addressed in a future release.

## 6.2 Scan installed packages against known vulnerabilities [⇧](#toc) <a name="6.2"></a>

### 6.2.1 Install required libraries [⇧](#toc) <a name="6.2.1"></a>

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

### 6.2.2 Scan Installed Packages [⇧](#toc) <a name="6.2.2"></a>

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

## 6.3 Security Guidance [⇧](#toc) <a name="6.2"></a>

### 6.3.1 Constant Security checks in a productive environment [⇧](#toc) <a name="6.3.1"></a>

It is advisable to keep a clone of the Python virtual environment including all dependencies used in the production code on a non-critical server. The vulnerability Checks may then be automated to run at least once a day and send reports to the security dev team.

### 6.3.2 Lock Down Virtual Environments [⇧](#toc) <a name="6.3.2"></a>

Disallow any changes in the virtual environment to prevent the use of dangerous libraries. To do this, make the virtual environment a read-only directory and only allow for write-access to patch vulnerabilities.   
As an example, it is not advisory to allow installation of `jkuri/bore`, as it allows circumventing certain network security features.  

# 7. Abbreviations [⇧](#toc) <a name="7."></a>

| **Abbreviation** | **Context** | **Description** |
| --- | --- | --- |
| dev | Documentation | `dev` marks a (nested/shared) dictionary as relevant for developers. These datasections may be leveraged freely. |
| dict | Python Code | Python dictionary object |
| m.op | Python Code | Operation identifier string (module.operation) |
