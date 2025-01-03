[![supermorph_PixelSnake_logo_v001](https://github.com/user-attachments/assets/0e92f76c-67db-4ff6-8e58-9ab77a9a6e8e)](https://www.supermorph.tech/)
<br><br><br>
![supermorph_morPy_github_v001](https://github.com/user-attachments/assets/51fd6975-d4cd-4123-b708-552e8fee9c1a)


More solutions. More insights. morPy.

Multiprocessing aided Python framework with integrated logging to database. Be the master of your app by analyzing runtime. Enjoy the comfort of runtime documentation ready for use in validated environments.

Feel free to comment, share and support this project.
Visit me on [supermorph.tech](https://www.supermorph.tech/) to get in touch with me.

# Requirements and Dependencies


## Software

### morPy v1.0.0c - Microsoft Windows

| Depency | Requirements |
| --- | --- |
| Python | [Python 3.10.11](https://www.python.org/downloads/release/python-31011/) |
| UltraDict | [Microsoft Visual C++ BuildTools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (Install Desktopdevelopment with C++) |

1.  Install Python with the option "Add python.exe to PATH" enabled.

## Virtual Environment (MS Windows)

*Compare with [freeCodeCamp.org](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)*

### Basic Setup

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

### Install Dependencies

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

### Copy Packages to Virtual Environment

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

# Versioning - α.β.γλ

| Symbol | Description |
| --- | --- |
| α   | Major Version.  <br>No downward compatibility: CRITICAL errors expected. |
| β   | Improvement Version.  <br>Limited downward compatibility: WARNING and DENIED messages expected. |
| γ   | Bugfix Version.  <br>Full downward compatibility. |
| λ   | Version status.  <br>*None*: Release version  <br>*a*: Alpha version with minor bugs for public testing.  <br>*b*: Beta version with potential showstopper bugs for internal testing.  <br>*c*: Gamma version. Development. Not presentable to public. |

# Parallelization

The parallelization in morPy is done utilizing an orchestration process with which the entire program starts and ends. The process ID "0" is always reserved for the orchestration process. It will take care of logging and is reserved for tasks with a priority in between 0 and 10 (smaller numbers for higher priority). All project tasks will automatically receive a higher number (lower priority) than morPy reserved tasks. In case a priority is corrected, a warning will be raised.

![EN-morPy-parallelization-scheme-v1 0 0-darkmode](https://github.com/user-attachments/assets/4f460193-7a01-4c78-a501-16b99aea747b)
