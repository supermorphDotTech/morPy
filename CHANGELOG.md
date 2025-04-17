<img src="https://github.com/user-attachments/assets/38a7a1e8-2a55-4f42-95a8-691a1cd77586" alt="supermorph_morPy_alpha_badge_v001" style="max-width:33%; height:auto;">

More solutions. More insights. morPy.

Python multiprocessing aided app foundation. Feature rich and easy to learn.

Feel free to comment, share and support this project!  

![License](https://img.shields.io/github/license/supermorphDotTech/morPy)
![GitHub commit activity (monthly)](https://img.shields.io/github/commit-activity/m/supermorphDotTech/morPy)

# v1.0.0a Changelog - Table of Contents <a name="toc"></a>

[Backlog](#Backlog)  <br/>
[v1.0.0 - Release Goals](#v1.0.0)  <br/>
[v1.0.0a](#v1.0.0a)  <br/>
[v1.0.0b](#v1.0.0b)  <br/>

# Backlog [⇧](#toc) <a name="Backlog"></a>

- [ ] Enhance documentation with tutorial videos
- [ ] Find an elegant way to lock file access for thread safety
- [ ] Define dependencies in a supported manifest file types (`package.json` or `Gemfile`)
- [ ] Encryption of `app_dict["morpy"]["heap_shelf"]` and `app_dict["morpy"]["proc_waiting"]` to prevent code insertion
- [ ] Develop a `setup.py` and upload morPy to the *Python Package Index - PyPI*
- [ ] Provide a packaging mechanism for morPy
- [ ] Develop an 'OS'-class for easier ports to different systems
  - [ ] Develop an elevation handler in that class
  - [ ] Move DPI awareness from `lib.fct.sysinfo()`
- [ ] Reduce `TODO` and `FIXME` left in the code. Only keep when, if it points to known bugs.
- [ ] Use type hints wherever useful

# v1.0.0 - Release Goals [⇧](#toc) <a name="v1.0.0"></a>

### Release Goal Description

First stable version of morPy. Tested on Win32 and Linux Systems.

### Changes

- [ ] When calling `morPy.join_or_task()`, child processes should stay alive while there are tasks left.
- [ ] Finished SQLite3 module
- [ ] Develop unittests in a way, that the logs serve as an audit trail for a version release
  - [ ] Ideally leverage the morPy wrapper for automated unit tests
- [ ] Enhance formats of tasks tracked by `ProgressTrackerTk()` by list and tuple similar to `process_q()`
- [ ] Find a solution for multithreading (i.e. for threading in `ProgressTrackerTk()`)
  - [ ] Multi-platform compatible
  - [ ] Needs to respect the multiprocessing idea of morPy (i.e. max parallel processes)
- [ ] Finish `lib.xl.XlWorkbook.edit_worksheet()`; localization does already exist
- [ ] Finish metrics functionality
- [ ] Connect `lib.xl.XlWorkbook()` with GUI
  - [ ] Provide GUI connection in `lib.xl.XlWorkbook.write_ranges()` for `ProgressTrackerTk()`
  - [ ] Provide GUI connection in `lib.xl.XlWorkbook.read_cells()` for `ProgressTrackerTk()`
- [x] Moved `lib.conf.py` and renamed it as `config.py` for increased accessibility
- [x] Mitigation of race condition when joining processes in `lib.mp.MorPyOrchestrator._mp_loop()`


# v1.0.0a [⇧](#toc) <a name="v1.0.0a"></a>

### Release Description

Clean Release for public testing. Linux compatibility not tested yet.

### Changes

- [x] New Wrapper for morPy
    - [x] Include metrics
    - [x] Eliminate the standard returns
    - [x] Eliminate the try-except-blocks
    - [x] Eliminate the tracing updates and remove `tracing()` from the frontend
    - [x] Eliminate the helper `_init()` methods
- [x] Zero Lints
  - [x] Changed function name `find_replace_saveas()` to `find_replace_save_as()`
  - [x] Overhaul of the frontend `.\morPy.py`
- [x] Provided `morPy.join_or_task()` to join processes.
- [x] Acquire lock on log DB during init and release it on exit
- [x] New function `morPy.conditional_lock()` to dynamically use a context manager only of the object has a 'lock' attribute.
  - [x] Eliminate inside `lib.mp.app_run()`
  - [x] Spread to other classes & functions for thread safety
- [x] Clean up localization from unused strings
- [x] Improve docstrings
- [x] Refactor `morpy_trace` to `trace`
- [x] Improve performance of locks on `app_dict` by checking the workflows in `lib.mp`

# v1.0.0b [⇧](#toc) <a name="v1.0.0b"></a>

### Release Description

First Release for public testing. Still quick and dirty in parts.

### New Features

Everything. Multiprocessing works efficiently including task shelving for greatly reduced overhead.
Fallback to single process utilizing standard `dict` works without notable impact on efficiency.