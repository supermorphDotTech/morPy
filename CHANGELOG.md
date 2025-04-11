<img src="https://github.com/user-attachments/assets/38a7a1e8-2a55-4f42-95a8-691a1cd77586" alt="supermorph_morPy_alpha_badge_v001" style="max-width:66%; height:auto;">

More solutions. More insights. morPy.

Python multiprocessing aided app foundation. Feature rich and easy to learn.

Feel free to comment, share and support this project!  

![License](https://img.shields.io/github/license/supermorphDotTech/morPy)
![GitHub commit activity (monthly)](https://img.shields.io/github/commit-activity/m/supermorphDotTech/morPy)

# v1.0.0b Changelog <a name="toc"></a>

[Backlog](#Backlog)  <br/>
[v1.0.0a - Release Goals](#v1.0.0a)  <br/>
[v1.0.0b](#v1.0.0b)  <br/>

# Backlog [⇧](#toc) <a name="Backlog"></a>

- [ ] Enhance documentation with tutorial videos
- [ ] Develop unittests in a way, that the logs serve as an audit trail for a version release
- [ ] Enhance formats of tasks tracked by `ProgressTrackerTk()` by list and tuple similar to `process_q()`
- [ ] Improve locks on `app_dict` to remove the ternary statements used now to determine type `dict | UltraDict`
- [ ] Find an elegant way to lock file access for multiprocessing
- [ ] Define dependencies in a supported manifest file types (`package.json` or `Gemfile`)
- [ ] Improve performance of locks on `app_dict` by checking the workflows in `lib.mp`
- [ ] Encryption of `app_dict["morpy"]["heap_shelf"]` and `app_dict["morpy"]["proc_waiting"]` to prevent code insertion
- [ ] Develop a `setup.py` and upload morPy to the *Python Package Index - PyPI*
- [ ] Provide a packaging mechanism for morPy
- [ ] Develop an 'OS'-class for easier ports to different systems
  - [ ] Develop an elevation handler in that class
- [ ] Find a solution for multithreading (i.e. for threading in `ProgressTrackerTk()`)
  - [ ] multi-platform compatible
  - [ ] Needs to respect the multiprocessing idea of morPy (i.e. max parallel processes)

# v1.0.0a - Release Goals [⇧](#toc) <a name="v1.0.0a"></a>

### Release Description

Clean Release for public testing. Linux compatibility tested.

### Changes

- [ ] Zero Lints
  - [x] Changed function name `find_replace_saveas()` to `find_replace_save_as()`
  - [x] Overhaul of the frontend `.\morPy.py`
- [ ] Reduce `TODO` and `FIXME` left in the code. Only keep when, if it points to known bugs.
- [ ] Provide a "process join" function
- [ ] New Wrapper for morPy
    - [ ] Include metrics (also finish metrics functionality)
    - [ ] Eliminate the standard returns
    - [ ] Eliminate the try-except-blocks
    - [ ] Eliminate the declarations for tracing and remove `tracing()` from frontend
    - [ ] Eliminate the helper `_init()` methods
- [ ] Finish metrics functionality
- [ ] Finish SQLite3 module
- [ ] Clean up localization from unused strings
- [ ] Improve docstrings
- [ ] Use type hints wherever useful
- [ ] Audit the methods and algorithms used (make morPy more pythonic)
  - [ ] Use `any()` instead of `or`
  - [ ] Use more list comprehensions
  - [ ] Check, if generators are useful
  - [ ] Check, if assert has use cases somewhere

# v1.0.0b [⇧](#toc) <a name="v1.0.0b"></a>

### Release Description

First Release for public testing. Still quick and dirty in parts.

### New Features

Everything. Multiprocessing works efficiently including task shelving for greatly reduced overhead.