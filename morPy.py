r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module serves as the primary frontend for the morPy framework. It integrates UI
            components, logging, and task orchestration to support high‑level application functionality.
"""

from collections.abc import Callable


class FileDirSelectTk:
    r"""
    Provides a Tkinter graphical interface for file and directory selection. Each row represents an
    individual selection choice, and an optional top row of icons may be displayed for branding or
    additional context.
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, rows_data: dict, title: str = None,
                 icon_data: dict = None) -> None:
        r"""
        Initializes the FileDirSelectTk window with parameters for tracing, the global app configuration,
        and a dictionary defining selection rows. Each row’s data may specify whether the selection is for
        a file or directory, allowed file types (for dialogs), an optional custom image (and its size),
        and an optional default path. An optional icon configuration dictionary may be provided to display
        a top row of icons.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: morPy global dictionary containing app configurations.
        :param rows_data: Dictionary mapping row names to configuration dictionaries (see expected structure).
            Expected structure:
                {"selection_name" : {
                    "is_dir" : True | False,  # True for directory selection, False for file selection.
                    "file_types" : (('PDF','*.pdf'), ('Textfile','*.txt'), ('All Files','*.*')),  # For file dialogs.
                    "image_path" : "path/to/image.png",  # Optional custom image.
                    "image_size" : (width, height),  # Optional; defaults to (48, 48) if not provided.
                    "default_path" : "prefilled/default/path"  # Optional prefill for the input.},
                    ...}
        :param title: Optional window title; if omitted, a localized default is used.
        :param icon_data: Optional dictionary of icon configurations for the top row.”
            Expected structure:
                {"icon_name" : {
                    "position" : 1,         # placement, order (lowest first)
                    "img_path" : "path/to/image.png",     # image file path
                    "icon_size" : (width, height),        # (optional) size for the icon},
                    ...}

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
            selections: Dictionary with selections made, keyed with the row name. Example:
                {"selection_name" : value}

        :example:
            import morPy

            icon_data = {
                "company_logo1" : {
                    "position" : 1,                       # placement, order (lowest first)
                    "img_path" : "path/to/image.png",     # image file path
                }
            }
            selection_config = {
                "file_select" : {
                    "is_dir" : False,
                    "file_types" : (('Textfile','*.txt'), ('All Files','*.*')),
                    "default_path" : "prefilled/default/path"
                },
                "dir_select" : {
                    "is_dir" : True,
                    "default_path" : "prefilled/default/path"
                }
            }
            gui = morPy.FileDirSelectTk(morpy_trace, app_dict, rows_data, title="Select...")
            results = gui.run(morpy_trace, app_dict)["selections"]
            file = results["file_selected"]
            dir = results["dir_selected"]
        """
        import lib.ui_tk
        # Instantiate the underlying implementation.
        self._impl = lib.ui_tk.FileDirSelectTk(
            morpy_trace, app_dict, rows_data=rows_data, title=title, icon_data=icon_data
        )

    def run(self, morpy_trace: dict, app_dict: dict):
        r"""
        Starts the file/directory selection GUI and blocks until the user completes
        their selections.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
<<<<<<< Updated upstream
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
            selections: A dictionary of user inputs keyed by row name.
=======
            selections: A dictionary where keys are the row names and values are the
                        paths selected by the user.
>>>>>>> Stashed changes
        """
        return self._impl.run(morpy_trace, app_dict)


class GridChoiceTk:
    r"""
    Implements a Tkinter grid menu that displays image tiles with labels underneath. When the
    user clicks a tile, its associated return value is captured, enabling menu‐style selection.
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, tile_data: dict, title: str=None,
                 default_tile_size: tuple=None, icon_data: dict=None):
        r"""
        Initializes the grid menu interface with tracing, global app configuration, and a
        dictionary defining each tile. The tile_data dictionary should map tile names to
        configurations that include grid coordinates, an image path, a descriptive text label,
        a return value, and optionally a tile size. An optional title, default tile size, and
        icon configuration may also be provided.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param tile_data: Dictionary containing configuration for each tile.
            The expected structure is:
            {"tile_name" : {
                    "row_column" : (row, column),         # grid placement
                    "img_path" : "path/to/image.png",     # image file path
                    "text" : "Descriptive text",          # label under the image
                    "return_value" : some_value,          # value returned when clicked
                    "tile_size" : (width, height),        # (optional) size for the image tile
                    },
            ...}
        :param title: Title of the tkinter window. Defaults to morPy localization.
        :param default_tile_size: Default (width, height) if a tile does not specify its own size. Defaults to
                                  a fraction of main monitor height.
        :param icon_data: (Optional) Dictionary containing configuration for top row icons. Defaults to None.
            Expected structure:
            {"icon_name" : {
                    "position" : 1,         # placement, order (lowest first)
                    "img_path" : "path/to/image.png",     # image file path
                    "icon_size" : (width, height),        # (optional) size for the icon
                    },
            ...}

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            import morPy

            icon_data = {
                "company_logo1" : {
                    "position" : 1,                       # placement, order (lowest first)
                    "img_path" : "path/to/image.png",     # image file path
                }
            }

            tile_data = {
                "start" : {
                    "row_column" : (row, column),
                    "img_path" : "path/to/image.png",
                    "text" : "Start the App",
                    "return_value" : 1,
                    },
            ...}
            gui = morPy.GridChoiceTk(morpy_trace, app_dict, tile_data,
                title="Start Menu",
                default_tile_size=(128, 128),
                icon_data=icon_data
            )
            result = gui.run(morpy_trace, app_dict)["choice"]
        """
        import lib.ui_tk
        # Instantiate the underlying implementation.
        self._impl = lib.ui_tk.GridChoiceTk(
            morpy_trace, app_dict, tile_data=tile_data, title=title, default_tile_size=default_tile_size,
            icon_data=icon_data
        )

    def run(self, morpy_trace: dict, app_dict: dict):
        r"""
        Launches the grid‐choice GUI and waits until the user clicks a tile.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
            choice: The value associated with the selected tile.

        :example:
            import morPy

            tile_data = {
                "start" : {
                    "row_column" : (row, column),
                    "img_path" : "path/to/image.png",
                    "text" : "Start the App",
                    "return_value" : 1,
                },
            ...}
            gui = morPy.GridChoiceTk(morpy_trace, app_dict, tile_data,
                title="Start Menu",
                default_tile_size=(128, 128),
            )
            result = gui.run(morpy_trace, app_dict)["choice"]
        """
        return self._impl.run(morpy_trace, app_dict)


class MorPyException(Exception):
    r"""
    This wraps errors in the standard morPy fashion. If one of the arguments
    required for logging is missing, this wrapper will raise other errors in
    order to reduce tracebacks and specifically point to the issue at hand.
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, exception_obj: BaseException, line: int,
                 log_level: str, message: str = None) -> None:
        r"""
        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param log_level: Severity: debug/info/warning/error/critical/denied
        :param line: Line number of the original error that could not be logged.
        :param exception_obj: Exception object as passed by sys of the parent function/method.
        :param message: Additional exception text attached to the end of the standard message.

        :example:
            import morPy
            import sys
            try:
                pass # some code
            except Exception as e:
                raise morPy.exception(
                    morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "info",
                    message="Specifics regarding the error"
                )
        """
        import lib.exceptions
        # Instantiate the underlying implementation.
        self._impl = lib.exceptions.MorPyException(
            morpy_trace, app_dict, exception_obj, line, log_level, message=message
        )


class PriorityQueue:
    r"""
    Provides a priority‑based task queue where lower numeric values indicate
    higher priority. Enqueued tasks are also timestamped with an incrementing
    counter to preserve insertion order for tasks sharing the same priority.
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, name: str = None) -> None:
        r"""
<<<<<<< Updated upstream
        :param morpy_trace: Operation credentials and tracing information
=======
        Sets up the priority queue with tracing, the global configuration, and an
        optional name. It initializes internal counters and data structures needed
        for task storage and lookup.

        :param trace: Operation credentials and tracing information
>>>>>>> Stashed changes
        :param app_dict: morPy global dictionary containing app configurations
        :param name: Name or description of the instance
        """
        import lib.common
        # Instantiate the underlying implementation.
        self._impl = lib.common.PriorityQueue(morpy_trace, app_dict, name=name)

    def enqueue(self, morpy_trace: dict, app_dict: dict, priority: int=100, task: tuple=None) -> dict:
        r"""
        Adds a task to the priority queue under a specified integer priority (lower means
        higher priority). The task must be supplied as a callable packaged with its arguments
        (for example, as a tuple or partial). If the task is already present (as determined by
        its system‐ID), a debug message indicates duplication; otherwise, it is inserted with
        an associated counter.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param priority: Integer representing task priority (lower is higher priority)
        :param task: Tuple of a callable, *args and **kwargs (func, *args, **kwargs)

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates if the task was enqueued successfully

        :example:
            from functools import partial
            queue = PriorityQueue(morpy_trace, app_dict, name="example_queue")
            task = partial(my_func, morpy_trace, app_dict)
            queue.enqueue(morpy_trace, app_dict, priority=25, task=task)
        """
        return self._impl.enqueue(morpy_trace, app_dict, priority=priority, task=task)

    def pull(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Removes the highest‑priority task from the queue and returns a dictionary
        with the task’s priority, counter value, system‑assigned task ID, and the
        task components as a list. If the queue is empty, a debug message is logged.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates if the task was pulled successfully
            priority: Integer representing task priority (lower is higher priority)
            counter: Number of the task when enqueued
            task_id : Continuously incremented task ID (counter).
            task_sys_id : ID of the task determined by Python core
            task: The pulled task list
            task_callable: The pulled task callable

        :example:
            from functools import partial
            queue = PriorityQueue(morpy_trace, app_dict, name="example_queue")
            task = queue.pull(morpy_trace, app_dict)['task']
            task()
        """
        return self._impl.pull(morpy_trace, app_dict)


class ProgressTracker:
    r"""
    Maintains a numerical counter to track progress during long‑running operations. It logs progress
    updates at specified tick percentages and supports both floating‑point and integer counting for
    efficiency.
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, description: str=None, total: float=None, ticks: float=None,
                 float_progress: bool=False, verbose: bool=False) -> None:
        r"""
<<<<<<< Updated upstream
        :param morpy_trace: operation credentials and tracing information
=======
        Initializes the progress tracker with a descriptive label, a total count needed for completion,
        and a tick value (in percent) that determines when to log progress updates. An option is
        available to use floating‑point progress and to enable verbose logging.

        :param trace: operation credentials and tracing information
>>>>>>> Stashed changes
        :param app_dict: morPy global dictionary containing app configurations
        :param description: Describe, what is being processed (i.e. file path or calculation)
        :param total: Mandatory - The total count for completion
        :param ticks: Mandatory - Percentage of total to log the progress. I.e. at ticks=10.7 at every
            10.7% progress exceeded the exact progress will be logged. If None or greater 100, will default to 10.
        :param float_progress: For efficient progress tracking, by default the progress is not tracked with
            floats. If True, the amount of ticks at which to update progress may be a lot more expensive.
            Defaults to False.
        :param verbose: If True, progress is only logged in verbose mode except for the 100% mark. Defaults to False.

        :example:
            TODO example
        """
        import lib.common
        # Instantiate the underlying implementation.
        self._impl = lib.common.ProgressTracker(
            morpy_trace, app_dict, description=description, total=total, ticks=ticks,
            float_progress=float_progress, verbose=verbose
        )

    def update(self, morpy_trace: dict, app_dict: dict, current: float = None) -> dict:
        r"""
<<<<<<< Updated upstream
        Update current progress and log the progress if a tick is passed.
=======
        Updates the current progress count (either incrementally or to a given value) and
        logs progress if a tick threshold is reached.
>>>>>>> Stashed changes

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param current: Current progress count. If None, each call of this method will add +1
            to the progress count. Defaults to None.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors
            prog_rel: Relative progress, float between 0 and 1
            prog_abs: Absolute progress, float between 0.00 and 100.00
            message: Message generated. None, if no tick was hit.

        :example:
            TODO example
        """
        return self._impl.update(morpy_trace, app_dict, current=current)


class ProgressTrackerTk:
    r"""
    Creates a graphical progress tracker using Tkinter. The GUI displays one or two progress bars
    (overall progress and, if there are multiple stages, stage progress), along with descriptive
    headlines and an optional console for status output. The window may close automatically at
    100% progress or await manual closure.
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, frame_title: str=None, frame_width: int=None,
              frame_height: int=None, headline_total: str=None, headline_font_size: int=10,
              detail_description_on: bool=False, description_font_size: int=8, font: str="Arial",
              stages: int=1, console: bool=False, auto_close: bool=False, work=None):

        r"""
        Initializes the ProgressTrackerTk window with parameters such as: frame title; optional
        frame dimensions (otherwise defaults based on monitor size); overall headline text and
        font size; flag and font size for displaying detailed status messages; a base GUI font;
        the number of progress stages; a flag to enable redirection of console output; an
        auto‑close option; and an optional work callable that runs in a background thread.
        The method configures default widget dimensions based on system resolution.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param frame_title: Window frame title as shown in the title bar.
        :param frame_width: Frame width in pixels.
                            Defaults to 1/3rd of main monitor width.
        :param frame_height: Frame height in pixels.
                             Defaults to a value depending on which widgets are displayed.
        :param headline_total: Descriptive name for the overall progress.
                               Defaults to morPy localization.
        :param headline_font_size: Font size for both, overall and stage descriptive names.
                                   Defaults to 10.
        :param detail_description_on: If True, a widget for the detail messages will be drawn to GUI.
                                      Defaults to False.
        :param description_font_size: Font size for description/status.
                                      Defaults to 8.
        :param font: Font to be used in the GUI, except for the title bar and console widget.
                     Defaults to "Arial".
        :param stages: Sum of stages until complete. Will not show progress bar for overall progress if equal to 1.
                       Defaults to 1.
        :param console: If True, will reroute console output to GUI.
                        Defaults to False.
        :param auto_close: If True, window automatically closes at 100%. If False, user must click "Close".
                           Defaults to False.
        :param work: A callable (e.g. functools.partial()). Will run in a new thread.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            gui = morPy.ProgressTrackerTk(morpy_trace: dict, app_dict,
                frame_title="My Demo Progress GUI",
                detail_description="Generic Progress stage",
                stages=outer_loop_count,
                stage_limit=inner_loop_count,
                work=work)
        """
        import lib.ui_tk
        # Instantiate the underlying implementation.
        self._impl = lib.ui_tk.ProgressTrackerTk(
            morpy_trace, app_dict, frame_title=frame_title, frame_width=frame_width, frame_height=frame_height,
            headline_total=headline_total, headline_font_size=headline_font_size,
            detail_description_on=detail_description_on, description_font_size=description_font_size, font=font,
            stages=stages, console=console, auto_close=auto_close, work=work
        )

    def run(self, morpy_trace: dict, app_dict: dict):
        r"""
        Starts the progress tracking GUI by initiating its internal update loop and then entering
        Tkinter’s main event loop. The GUI stays active until progress is complete and the window
        is closed.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            progress = morPy.ProgressTrackerTk(morpy_trace: dict, app_dict,
                frame_title="My Demo Progress GUI",
                detail_description="Generic Progress stage",
                stages=1,
                stage_limit=10,
                work=work)

            progress.run(morpy_trace, app_dict)
        """
        return self._impl.run(morpy_trace, app_dict)

    def begin_stage(self, morpy_trace: dict, app_dict: dict, stage_limit: (int, float) = 1, headline_stage: str = None,
                    detail_description: str=None, ticks: float=.01):
        r"""
        Begins a new stage of progress by resetting the stage-specific progress counter to zero and setting
        stage parameters such as the stage limit (the maximum progress value for this stage), a headline text,
        and an optional detailed description. A tick value (default 0.01%) determines how finely progress
        updates are logged.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param stage_limit: This is the maximum value of the stage progress. Set it to 0 to turn off the stage progress.
                            It represents the maximum value the stage progress will reach until 100%, which is
                            determined by which value you choose to increment the progress with (defaults to 1 per
                            increment). A value of 10 for example amounts to 10% per increment.
                            Defaults to 1.
        :param headline_stage: Descriptive name for the actual stage.
                               Defaults to morPy localization.
        :param detail_description: Description or status. Will
                                   not be shown if None at construction.
                                   Defaults to None.
        :param ticks: [optional] Percentage of total to log the progress. I.e. at ticks=10.7 at every
                      10.7% progress exceeded the exact progress will be logged. Defaults to 0.01.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            # Set up the next stage
            headline = "Currently querying"
            description = "Starting stage..."
            progress.begin_stage(morpy_trace, app_dict, stage_limit=10, headline_stage=headline,
            detail_description=description)
        """
        return self._impl.run(
            morpy_trace, app_dict, stage_limit=stage_limit, headline_stage=headline_stage,
            detail_description=detail_description, ticks=ticks
        )

    def update_progress(self, morpy_trace: dict, app_dict: dict, current: float = None) -> dict:
        r"""
        Queues an update to the current stage’s progress and, if an overall progress bar is present,
        recomputes the overall progress as a function of completed stages plus progress of the current
        stage. If overall progress reaches 100% and auto‑close is enabled, the window is closed;
        otherwise, a ‘Close’ button appears and console output is stopped.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param current: Current progress count. If None, each call of this method will add +1
            to the progress count. Defaults to None.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            progress = morPy.ProgressTrackerTk(morpy_trace: dict, app_dict,
                frame_title="My Demo Progress GUI",
                detail_description="Starting stage 1",
                stages=2,
                stage_limit=10,
                work=work)

            progress.run(morpy_trace, app_dict)

            curr_cnt = 5.67
            msg = f'Currently at {curr_cnt}'
            progress.update_progress(morpy_trace, app_dict, current=curr_cnt, detail_description=msg)

            # stage 1 is at 100%
            curr_cnt = 10
            msg = f'Currently at {curr_cnt}'
            progress.update_progress(morpy_trace, app_dict, current=curr_cnt, detail_description=msg)

            # Setup stage 2
            progress.update_text(morpy_trace, app_dict,
                headline_stage="Starting stage 2",
                detail_description="Now copying data...",
            )
            progress.update_progress(morpy_trace, app_dict, current=0, stage_limit=15)

            # stage 2 is at 100%
            curr_cnt = 15
            msg = f'Currently at {curr_cnt}'
            progress.update_progress(morpy_trace, app_dict, current=curr_cnt, detail_description=msg)
        """
        return self._impl.update_progress(morpy_trace, app_dict, current=current)

    def update_text(self, morpy_trace: dict, app_dict: dict, headline_total: str = None, headline_stage: str = None,
                    detail_description: str = None):
        r"""
        Queues a request to update the displayed headline texts and description in the progress GUI.
        The overall progress headline and stage headline can be replaced, along with the detail text
        below the stage bar.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param headline_total: If not None, sets the overall progress headline text.
        :param headline_stage: If not None, sets the stage progress headline text.
        :param detail_description: If not None, sets the description text beneath the stage headline.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether text update completed without errors

        :example:
            gui.update_text(morpy_trace, app_dict,
                headline_total="Processing Outer Loop 3",
                headline_stage="Processing File 5",
                detail_description="Now copying data...")
        """
        return self._impl.update_text(
            morpy_trace, app_dict, headline_total=headline_total, headline_stage=headline_stage,
            detail_description=detail_description
        )

<<<<<<< Updated upstream
    def end_stage(self, morpy_trace: dict, app_dict: dict):
=======

    def end_stage(self, trace: dict, app_dict: dict) -> None:
>>>>>>> Stashed changes
        r"""
        End the current stage by setting it to 100%.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self.end_stage(morpy_trace, app_dict)
        """
        return self._impl.end_stage(morpy_trace, app_dict)


class XlWorkbook:
    r"""
    Instantiates an Excel workbook to edit, read from and write to it.
    It uses OpenPyXL as the API to the workbooks.
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, workbook: str, create: bool=False,
              data_only: bool=False, keep_vba: bool=True) -> None:
        r"""
        Helper method for initialization to ensure @metrics decorator usage.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param workbook: Path of the workbook
        :param create: If True and file does not yet exist, will create the workbook. If file exists, will
                    open the existing file.
        :param data_only: If True, cells with formulae are represented by their calculated values.
                    Closing and reopening the workbook is required for this to change.
        :param keep_vba: If True, preserves any Visual Basic elements in the workbook. Only has an effect
                    on workbooks supporting vba (i.e. xlsm-files). These elements remain immutable. Closing
                    and reopening the workbook is required to change behaviour.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self._init(morpy_trace, app_dict)
        """

        import lib.xl
        # Instantiate the underlying implementation.
        self._impl = lib.xl.XlWorkbook(
            morpy_trace, app_dict, workbook, create=create, data_only=data_only, keep_vba=keep_vba
        )

    def save_workbook(self, morpy_trace: dict, app_dict: dict, close_workbook: bool=False) -> dict:
        r"""
        Saves the changes to the MS Excel workbook.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param close_workbook: If True, closes the workbook.

        :return: dict
            morpy_trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).
            wb_obj: Returns None, if the object was closed. Else returns self. Used to delete the
                reference to an instance.

        :example:
            wb_path = "C:\my.xlsx"
            wb = XlWorkbook(morpy_trace, app_dict, wb_path)

            # Save and close the workbook. Write "None" to the reference "wb".
            wb = wb.save_workbook(morpy_trace, app_dict, close=True)["wb_obj"]
            print(f'{wb}')
        """
        return self._impl.save_workbook(morpy_trace, app_dict, close_workbook=close_workbook)

    def close_workbook(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Closes the MS Excel workbook.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.

        :return: dict
            morpy_trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).
            wb_obj: Returns None, if the object was closed. Else returns self. Used to delete the
                reference to an instance.

        :example:
            wb_path = "C:\my.xlsx"
            wb = XlWorkbook(morpy_trace, app_dict, wb_path)

            # Close the workbook. Write "None" to the reference "wb".
            wb = wb.close_workbook(morpy_trace, app_dict)["wb_obj"]
            print(f'{wb}')
        """
        return self._impl.close_workbook(morpy_trace, app_dict)

    def activate_worksheet(self, morpy_trace: dict, app_dict: dict, worksheet: str) -> dict:
        r"""
        Activates a specified worksheet in the workbook. If the sheet is not found,
        an error is logged.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param worksheet: The name of the worksheet to activate.

        :return: dict
            morpy_trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).

        :example:
            wb_path = "C:\my.xlsx"
            wb = XlWorkbook(morpy_trace, app_dict, wb_path)
            w_sht = "Sheet1"
            wb.activate_worksheet(morpy_trace, app_dict, w_sht)
        """
        return self._impl.activate_worksheet(morpy_trace, app_dict, worksheet)

    def read_cells(self, morpy_trace: dict, app_dict: dict, cell_range: list=None,
                   cell_styles: bool=False, worksheet: str=None, gui=None) -> dict:
        r"""
        Reads the cells of MS Excel workbooks. Overlapping ranges will get auto-formatted
        to ensure every cell is addressed only once.

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param cell_range: The cell or range of cells to read from. If cell range is None, will read all cells
            inside the matrix of max_row and max_column (also empty ones). formats:
            - not case-sensitive
            - Single cell: ["A1"]
            - Range of cells: ["A1:ZZ1000"]
            - Ranges of cells: ["A1:ZZ1000", "c2:fl342"]
        :param cell_styles: If True, cell styles will be retrieved. If False, get value only.
        :param worksheet: Name of the worksheet, where the cell is located. If None, the
            active sheet is addressed.
        :param gui: User Interface reference. Automatically referenced by morPy.ProgressTrackerTk()

        :return: dict
            morpy_trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).
            cl_dict: Dictionary of cell content dictionaries containing values and styles of cells. Following is
                    an example of a single complete cell write:
                cl_dict = {
                    "A1" : {
                        "value" : "Data in Cell",
                        "comment" : {
                            "text" : "This is a comment",
                            "author" : "Mr. Author Man",
                        },
                        "format" : "General",           # Options: General|Number|Currency|Accounting|Date|Time|Percentage
                                                        # > Fraction|Scientific|Text|custom strings
                        "font" : {
                            "name" : "Calibri",
                            "bold" : True,
                            "italic" : True,
                            "vertical align" : None,    # Options: None|superscript|subscript
                            "underline" : None,         # Options: None|single|double|singleAccounting|doubleAccounting
                            "strike" : False,
                            "size" : 14,
                            "color" : "D1760C",
                        },
                        "background" : {
                            "fill type" : None,         # Options: None|solid|darkGrid|darkTrellis|lightDown|lightGray
                                                        # > lightGrid|lightHorizontal|lightTrellis|lightUp
                                                        # > lightVertical|mediumGray
                            "start color" : "307591",
                            "end color" : "67CCCC",
                        },
                        "border" : {
                            "edge" : "outline",         # Options: left|right|top|bottom|diagonal|outline
                                                        # > vertical|horizontal
                            "style" : None,             # Options: None|dashDot|dashDotDot|dashed|dotted|double|hair|medium
                                                        # > medium|mediumDashDot|mediumDashDotDot|mediumDashed|slantDashDot
                                                        # > thick|thin
                            "color" : "2A7F7F",
                            "diagonal direction" : 0,   # Options: 0 (no diagonal) | 1 (downwards) | 2 (upwards)
                        },
                        "alignment" : {
                            "horizontal" : "general",   # Options: general|left|center|right|fill|justify|centerContinuous
                                                        # > distributed
                            "vertical" : "center",      # Options: top|center|bottom|justify|distributed
                            "text rotation" : 0,
                            "wrap text" : False,
                            "shrink to fit" : False,
                            "indent" : 0,
                        },
                        "protection" : {
                            "locked" : False,
                            "hidden" : False,
                        },
                    },
                    "A2" : { ... }
                }

        :example:
            wb_path = "C:\my.xlsx"
            wb = morPy.XlWorkbook(morpy_trace, app_dict, wb_path)
            cl_dict = wb.read_cells(morpy_trace, app_dict, worksheet="Sheet1", cell_range=["A1", "B2:C3"])["cl_dict"]
            print(f'{cl_dict}')
        """
        return self._impl.read_cells(
            morpy_trace, app_dict, cell_range=cell_range, cell_styles=cell_styles, worksheet=worksheet, gui=gui
        )

    def write_ranges(self, morpy_trace: dict, app_dict: dict, worksheet: str=None, cell_range: list=None,
                     cell_writes: list=None, fill_range: bool=False, style_default: bool=False,
                     save_workbook: bool=True, close_workbook: bool=False) -> dict:
        r"""
        Writes data into cells of an Excel workbook. OpenPyXL documentation:
        https://openpyxl.readthedocs.io/en/stable/api/openpyxl.cell.cell.html#openpyxl.cell.cell.Cell
        https://openpyxl.readthedocs.io/en/3.1.3/styles.html

        :param morpy_trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param worksheet: Name of the worksheet, where the cell is located. If None, the
            active sheet is addressed.
        :param cell_range: The cell or range of cells to write. Accepted formats:
            - not case-sensitive
            - Single cell: ["A1"]
            - Range of cells: ["A1:ZZ1000"]
            - Ranges of cells: ["A1:ZZ1000", "c2:fl342"]
        :param cell_writes: List of cell content dictionaries to be written consecutively. If the list is shorter
            than the amount of cells in the range, it will stop writing to cells and finish the operation. The
            dictionaries do not need to contain all possible keys, only assign the cell attributes/values needed.
            See example for a display of usage. Following is an example of a single complete cell write:
                cl_list = [
                    {"value" : "Data in Cell",
                    "comment" : {
                        "text" : "This is a comment",
                        "author" : "Mr. Author Man",
                    },
                    "format" : "General",           # Options: General|Number|Currency|Accounting|Date|Time|Percentage
                                                    # > Fraction|Scientific|Text|custom strings
                    "font" : {
                        "name" : "Calibri",
                        "bold" : True,
                        "italic" : True,
                        "vertical align" : None,    # Options: None|superscript|subscript
                        "underline" : None,         # Options: None|single|double|singleAccounting|doubleAccounting
                        "strike" : False,
                        "size" : 14,
                        "color" : "D1760C",
                    },
                    "background" : {
                        "fill type" : None,         # Options: None|solid|darkGrid|darkTrellis|lightDown|lightGray
                                                    # > lightGrid|lightHorizontal|lightTrellis|lightUp
                                                    # > lightVertical|mediumGray
                        "start color" : "307591",
                        "end color" : "67CCCC",
                    },
                    "border" : {
                        "edge" : "outline",         # Options: left|right|top|bottom|diagonal|outline
                                                    # > vertical|horizontal
                        "style" : None,             # Options: None|dashDot|dashDotDot|dashed|dotted|double|hair|medium
                                                    # > medium|mediumDashDot|mediumDashDotDot|mediumDashed|slantDashDot
                                                    # > thick|thin
                        "color" : "2A7F7F",
                        "diagonal direction" : 0,   # Options: 0 (no diagonal) | 1 (downwards) | 2 (upwards)
                    },
                    "alignment" : {
                        "horizontal" : "general",   # Options: general|left|center|right|fill|justify|centerContinuous
                                                    # > distributed
                        "vertical" : "center",      # Options: top|center|bottom|justify|distributed
                        "text rotation" : 0,
                        "wrap text" : False,
                        "shrink to fit" : False,
                        "indent" : 0,
                    },
                    "protection" : {
                        "locked" : False,
                        "hidden" : False,
                    },
                },
                { ... }]
        :param fill_range: If True and if the cell_writes list is shorter than the amount
            of cells in the range, it will continue writing the values from beginning until the end
            of the range.
        :param style_default: If True, styles/attributes of cells will be reset to default. If False,
            the styles/attributes of the original cell will be preserved.
        :param save_workbook: If True, saves the workbook after the changes.
        :param close_workbook: If True, closes the workbook.

        :return: dict
            check: Indicates whether the function executed successfully (True/False).
            morpy_trace: Operation credentials and tracing.
            wb_obj: Returns None, if the object was closed. Else returns self. Used to delete the
                reference to an instance.

        :example:
            w_sh = "Sheet1"
            cl_rng = ["A1:A10"]
            cell_writes = []
            cell_writes.append(
                {"value": "Example"}
            )
            cell_writes.append({
                "value" : r"=1+2",
                "font" : {
                    "color" : "D1760C",
                    },
            })
            wb = wb.write_cells(morpy_trace, app_dict, worksheet=w_sh, cell_range=cl_rng, cell_writes=cell_writes
                                save_workbook=True, close_workbook=True)["wb_obj"]
        """
        return self._impl.write_ranges(
            morpy_trace, app_dict, worksheet=worksheet, cell_range=cell_range, cell_writes=cell_writes,
            fill_range=fill_range, style_default=style_default, save_workbook=save_workbook,
            close_workbook=close_workbook
        )


def app_dict_to_string(app_dict):
    r"""
    Generates a UTF‑8 string representation of the complete global app configuration
    dictionary (app_dict) preserving its nested structure. Note that for very large
    dictionaries this may be memory‑intensive.

    :param app_dict: morPy global dictionary

    :return app_dict_str: morPy global dictionary as a UTF-8 string

    :example:
        morPy.app_dict_to_string(app_dict) # Do not specify depth!
    """
    import lib.fct
    return lib.fct.app_dict_to_string(app_dict)

<<<<<<< Updated upstream
def csv_read(morpy_trace: dict, app_dict: dict, src_file_path: str=None, delimiter: str=None,
             print_csv_dict: bool=False, log_progress: bool=False, progress_ticks: float=None, gui=None):
=======

def conditional_lock(obj):
    r"""
    Returns a no‑op lock context manager if the provided object is a plain dictionary,
    or the object’s own lock if it supports locking (for example, if it is an UltraDict).

    :param obj: morPy global dictionary

    :example:
        with conditional_lock(app_dict["morpy"]):
            pass    # Add your code
    """

    # Fallback to no-lock when object is a 'dict'
    class _NoOpLock:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, traceback):
            pass

    return getattr(obj, "lock", _NoOpLock())


def csv_read(trace: dict, app_dict: dict, src_file_path: str=None, delimiter: str=None,
             print_csv_dict: bool=False, log_progress: bool=False, progress_ticks: float=None, gui=None) -> dict:
>>>>>>> Stashed changes
    r"""
    Reads a CSV file and converts its contents to a nested dictionary. The function auto‑detects the
    header row and delimiter (unless one is specified), splits data rows accordingly, and logs
    progress if requested. It returns a dictionary where each data “table” contains metadata
    (delimiter, header, column count, row count) and row‑by‑row data keyed by line number.

    :param morpy_trace: Operation credentials and tracing
    :param app_dict: morPy global dictionary containing app configurations
    :param src_file_path: Path to the csv file.
    :param delimiter: Delimiters used in the csv. None = Auto detection
    :param print_csv_dict: If true, the csv_dict will be printed to console. Should only
        be used for debugging with small example csv files. May take very long to complete.
    :param log_progress: If True, logs the progress.
    :param progress_ticks: Percentage of total to log the progress. I.e. at ticks=10.7 at every
        10.7% progress exceeded the exact progress will be logged. If None or greater 100, will default to 10.
        If gui is not None, may overwrite this setting.
    :param gui: User Interface reference. Automatically referenced by morPy.ProgressTrackerTk()

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        csv_dict: Dictionary containing all tags. The line numbers of data are
            the keys of the parent dictionary, and the csv header consists of
            the keys of every sub-dictionary.
            Pattern:
                {DATA1 :
                    delimiter : [str]
                    header : [tuple] (header(1), header(2), ...)
                    columns : [int] header columns
                    rows : [int] number of rows in data
                    ROW1 : [dict]
                        {header(1) : data(1, 1),
                        header(2) : data(2, 1),
                        ...}
                    ROW2 : [dict]
                        {header(1) : data(1, 2),
                        header(2) : data(2, 2),
                        ...}
                DATA2 : ...}

    :example:
        src_file_path = 'C:\my_file.csv'
        delimiter = '\",\"'
        csv = morPy.csv_read(morpy_trace, app_dict, src_file_path, delimiter)
        csv_dict = csv["csv_dict"]
        csv_header1 = csv["csv_dict"]["DATA1"]["header"]
        print(f'{csv_header1}')
    """
    import lib.csv
    return lib.csv.csv_read(
        morpy_trace, app_dict, src_file_path=src_file_path, delimiter=delimiter,
        print_csv_dict=print_csv_dict, log_progress=log_progress, progress_ticks=progress_ticks, gui=gui
    )

<<<<<<< Updated upstream
def csv_dict_to_excel(morpy_trace: dict, app_dict: dict, xl_path: str=None, overwrite: bool=False,
=======

def csv_dict_to_excel(trace: dict, app_dict: dict, xl_path: str=None, overwrite: bool=False,
>>>>>>> Stashed changes
                      worksheet: str=None, close_workbook: bool=False, csv_dict: dict=None,
                      log_progress: bool=False, progress_ticks: float=None):
    r"""
    Takes a CSV dictionary (as generated by csv_read), optionally processes it, and writes its
    data into an Excel workbook using OpenPyXL. Cell writes are performed sequentially over
    specified ranges; if the list of cell definitions is shorter than the range and ‘fill_range’
    is True, the definitions repeat until the range is completely written. The function can also
    reset cell styles and save/close the workbook as configured.

    :param morpy_trace: Operation credentials and tracing
    :param app_dict: morPy global dictionary containing app configurations
    :param xl_path: Path to the target MS Excel file.
    :param overwrite: If True, an existing MS Excel file may be overwritten.
    :param worksheet: Name of the worksheet, where the cell is located. If None, the
        active sheet is addressed.
    :param close_workbook: If True, closes the workbook.
    :param csv_dict: Dictionary containing all tags. The line numbers of data are
        the keys of the parent dictionary, and the csv header consists of
        the keys of every sub-dictionary.
        Pattern:
            {DATA1 :
                delimiter : [str]
                header : [tuple] (header(1), header(2), ...)
                columns : [int] header columns
                rows : [int] number of rows in data
                ROW1 : [dict]
                    {header(1) : data(1, 1),
                    header(2) : data(2, 1),
                    ...}
                ROW2 : [dict]
                    {header(1) : data(1, 2),
                    header(2) : data(2, 2),
                    ...}
            DATA2 : ...}
    :param log_progress: If True, logs the progress.
    :param progress_ticks: Percentage of total to log the progress. I.e. at ticks=10.7 at every
        10.7% progress exceeded the exact progress will be logged. If None or greater 100, will default to 10.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        wb_obj: Returns None, if the object was closed. Else returns an instance of "xl.XlWorkbook()".
            Used to delete the reference to an instance.

    :example:
        src_file_path = 'C:\my.csv'
        delimiter = '","'
        csv = morPy.csv_read(morpy_trace, app_dict, src_file_path, delimiter)

        # ... process data in csv["csv_dict"] ...

        target_path = 'C:\my.xlsx'
        wb_sht = 'Sheet1'
        wb = csv_dict_to_excel(morpy_trace, app_dict, csv_dict=csv["csv_dict"], xl_path=target_path,
            overwrite=True, worksheet=wb_sht)["wb_obj"]

        # ... modify 'C:\my.xlsx' ...

        # Save and close workbook
        wb.close_workbook(mpy_trac, app_dict, save_workbook=True, close_workbook=True)
    """
    import lib.csv
    return lib.csv.csv_dict_to_excel(
        morpy_trace, app_dict, xl_path=xl_path, overwrite=overwrite, worksheet=worksheet, close_workbook=close_workbook,
        csv_dict=csv_dict, log_progress=log_progress, progress_ticks=progress_ticks
    )


def datetime_now():
    r"""
    Returns a dictionary containing the current date and time in multiple formats: the raw datetime
    object, a formatted date (DD.MM.YYYY), a datestamp (YYYY-MM-DD), time (hh:mm:ss), timestamp (hhmmss),
    a combined date–timestamp string (YYYY-MM-DD_hhmmss), and a logging stamp (YYYYMMDD_hhmmss).

    :return: dict
        datetime_value - Date and time in the format YYYY-MM-DD hh:mm:ss.ms as value
                        (used to determine runtime).
        date - Date DD.MM.YYY as a string.
        datestamp - Datestamp YYYY-MM-DD as a string.
        time - Time hh:mm:ss as a string.
        timestamp - Timestamp hhmmss as a string.
        datetimestamp - Date- and timestamp YYY-MM-DD_hhmmss as a string.
        loggingstamp - Date- and timestamp for logging YYYMMDD_hhmmss as a string.
    """
    import lib.fct
    return lib.fct.datetime_now()

<<<<<<< Updated upstream
def decode_to_plain_text(morpy_trace: dict, app_dict: dict, src_input: str, encoding: str=''):
=======

def decode_to_plain_text(trace: dict, app_dict: dict, src_input: str, encoding: str=''):
>>>>>>> Stashed changes
    r"""
    Decodes binary data into a plain text (string) buffer using a specified encoding, or
    auto‑detects the encoding if none is provided. Returns a dictionary including the decoded
    result (as a StringIO object), the encoding used, and the number of lines in the text.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param src_input: Any kind of data to be decoded. Binary expected.
    :param encoding: String that defines encoding. Leave empty to auto-detect.

    :return: dict
        check: Indicates whether the function executed successfully (True/False).
        morpy_trace: Operation credentials and tracing.
        result: Decoded result. Buffered object that may be used with the readlines() method.
        encoding: String containing the encoding of src_input.
        lines: Number of lines in the file.

    :example:
        src_input = open(src_file, 'rb')
        encoding = 'utf-16-le'
        retval = decode_to_plain_text(morpy_trace, app_dict, src_input, encoding)
    """
    import lib.common
    return lib.common.decode_to_plain_text(morpy_trace, app_dict, src_input, encoding=encoding)

<<<<<<< Updated upstream
def dialog_sel_file(morpy_trace: dict, app_dict: dict, init_dir: str=None, file_types: tuple=None, title: str=None):
=======

def dialog_sel_file(trace: dict, app_dict: dict, init_dir: str=None, file_types: tuple=None, title: str=None):
>>>>>>> Stashed changes
    r"""
    Opens a file selection dialog using Tkinter. The dialog starts in the given initial directory
    and filters selectable file types according to the provided tuple.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param file_types: This tuple of 2-tuples specifies, which filetypes will be
        selectable in the dialog box.
    :param title: Title of the open file dialog

    :return: dict
        morpy_trace: [dictionary] operation credentials and tracing
        check: The function ended with no errors and a file was chosen
        file_path: Path of the selected file
        file_selected: True, if file was selected. False, if canceled.

    :example:
        init_dir = "C:\"
        file_types = (('PDF','*.pdf'),('Textfile','*.txt'),('All Files','*.*'))
        title = 'Select a file...'
        file_path = morPy.dialog_sel_file(morpy_trace, app_dict, init_dir=init_dir,
                        file_types=file_types, title=title)["file_path"]
    """
    import lib.ui_tk
    return lib.ui_tk.dialog_sel_file(morpy_trace, app_dict, init_dir, file_types, title)

<<<<<<< Updated upstream
def dialog_sel_dir(morpy_trace: dict, app_dict: dict, init_dir: str=None, title: str=None):
=======

def dialog_sel_dir(trace: dict, app_dict: dict, init_dir: str=None, title: str=None) -> dict:
>>>>>>> Stashed changes
    r"""
    Opens a directory selection dialog using Tkinter. The dialog starts in the specified
    initial directory.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param title: Title of the open directory dialog

    :return: dict
        morpy_trace: [dictionary] operation credentials and tracing
        check: The function ended with no errors and a file was chosen
        dir_path: Path of the selected directory
        dir_selected: True, if directory was selected. False, if canceled.

    :example:
        init_dir = "C:\"
        title = 'Select a directory...'
        dir_path = morPy.dialog_sel_dir(morpy_trace, app_dict, init_dir=init_dir, title=title)["dir_path"]
    """
    import lib.ui_tk
    return lib.ui_tk.dialog_sel_dir(morpy_trace, app_dict, init_dir, title)

<<<<<<< Updated upstream
def find_replace_save_as(morpy_trace: dict, app_dict: dict, search_obj, replace_tpl: tuple, save_as: str,
                        overwrite: bool=False):
=======

def find_replace_save_as(trace: dict, app_dict: dict, search_obj, replace_tpl: tuple, save_as: str,
                        overwrite: bool=False) -> None:
>>>>>>> Stashed changes
    r"""
    Iterates through each line of the given text (converted to a string) to find and replace
    substrings according to provided tuples of (pattern, replacement). The resulting text is
    written to the specified file. If the target file exists and overwriting is disallowed,
    the operation is skipped.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param search_obj: Can be any given object to search in for regular expressions. Searches line by line.
    :param replace_tpl: Tuple of tuples. Includes every tuple of regular expressions and what they are supposed
                        to be replaced by.
    :param save_as: Complete path of the file to be saved.
    :param overwrite: True if new files shall overwrite existing ones, if there are any. False otherwise.
                      Defaults to False.

    :return: dict
        check - The function ended with no errors
        morpy_trace - operation credentials and tracing

    :example:
        search_obj = "Let's replace1 and replace2!"
        replace_tpl = (("replace1", "with1"), ("replace2", "with2"))
        save_as = "C:\my_replaced_strings.txt"
        overwrite = True
        retval = find_replace_save_as(morpy_trace, app_dict, search_obj, replace_tpl, save_as, overwrite)
    """
    import lib.bulk_ops
    return lib.bulk_ops.find_replace_save_as(
        morpy_trace, app_dict, search_obj, replace_tpl, save_as, overwrite=overwrite
    )

<<<<<<< Updated upstream
def fso_copy_file(morpy_trace: dict, app_dict: dict, source: str, dest: str, overwrite: bool=False):
=======

def fso_copy_file(trace: dict, app_dict: dict, source: str, dest: str, overwrite: bool=False) -> None:
>>>>>>> Stashed changes
    r"""
    Copies a file from a complete source path to a complete destination path. Before copying,
    it verifies that the source exists and whether the destination should be overwritten based
    on the ‘overwrite’ flag; logs the action accordingly.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param source: Complete path to the source file, including the file extension.
    :param dest: Complete path to the destination file, including the file extension.
    :param overwrite: Boolean indicating if the destination file may be overwritten. Defaults to False.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        source: Path to the source file as a path object.
        dest: Path to the destination file as a path object.

    :example:
        result = fso_copy_file(morpy_trace, app_dict, "path/to/source.txt", "path/to/destination.txt", True)
    """
    import lib.common
    return lib.common.fso_copy_file(morpy_trace, app_dict, source, dest, overwrite=overwrite)

<<<<<<< Updated upstream
def fso_create_dir(morpy_trace: dict, app_dict: dict, mk_dir: str):
=======

def fso_create_dir(trace: dict, app_dict: dict, mk_dir: str) -> None:
>>>>>>> Stashed changes
    r"""
    Creates a directory (and all necessary parent directories) at the specified path.
    If the directory already exists, a debug message is logged and no action is taken.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param mk_dir: Path to the directory or directory tree to be created.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).

    :example:
        result = fso_create_dir(morpy_trace, app_dict, "path/to/new_directory")
    """
    import lib.common
    return lib.common.fso_create_dir(morpy_trace, app_dict, mk_dir)

<<<<<<< Updated upstream
def fso_delete_dir(morpy_trace: dict, app_dict: dict, del_dir: str):
=======

def fso_delete_dir(trace: dict, app_dict: dict, del_dir: str) -> None:
>>>>>>> Stashed changes
    r"""
    Recursively deletes an entire directory and its contents after checking that the
    specified directory exists. Logs the deletion outcome.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param del_dir: Path to the directory to be deleted.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).

    :example:
        result = fso_delete_dir(morpy_trace, app_dict, "path/to/directory_to_delete")
    """
    import lib.common
    return lib.common.fso_delete_dir(morpy_trace, app_dict, del_dir)

<<<<<<< Updated upstream
def fso_delete_file(morpy_trace: dict, app_dict: dict, del_file: str):
=======

def fso_delete_file(trace: dict, app_dict: dict, del_file: str) -> None:
>>>>>>> Stashed changes
    r"""
    Deletes a single file after verifying that the file exists at the specified path.
    Logs the operation, or if the file does not exist, logs a warning.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param del_file: Path to the file to be deleted.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).

    :example:
        result = morPy.fso_delete_file(morpy_trace, app_dict, "path/to/file_to_delete.txt")
    """
    import lib.common
    return lib.common.fso_delete_file(morpy_trace, app_dict, del_file)

<<<<<<< Updated upstream
def fso_walk(morpy_trace: dict, app_dict: dict, path: str, depth: int=1):
=======

def fso_walk(trace: dict, app_dict: dict, path: str, depth: int=1) -> dict:
>>>>>>> Stashed changes
    r"""
    Recursively lists the contents of the specified directory up to a given depth. Returns a
    dictionary mapping each discovered root (labeled sequentially) to its path, a list of
    sub‑directories, and a list of files.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param path: Path to the directory to be analyzed.
    :param depth: Limits the depth of the analysis. Defaults to 1. Examples:
                  -1: No limit.
                   0: Path only.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        walk_dict: Dictionary of root directories and their contents. Example:
                   {
                       'root0': {
                           'root': root,
                           'dirs': [dir list],
                           'files': [file list]
                       },
                       'root1': {
                           'root': root,
                           'dirs': [dir list],
                           'files': [file list]
                       },
                       [...],
                   }

    :example:
        result = fso_walk(morpy_trace, app_dict, "path/to/directory", -1)
    """
    import lib.common
    return lib.common.fso_walk(morpy_trace, app_dict, path, depth=depth)

<<<<<<< Updated upstream
def interrupt(morpy_trace: dict, app_dict: dict):
=======

def interrupt(trace: dict, app_dict: dict):
>>>>>>> Stashed changes
    r"""
    Sets a global interrupt flag so that running processes or threads will halt at
    designated safe points. Intended to signal an application‑wide abort.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates if the task was pulled successfully

    :example:
        mp.interrupt(morpy_trace, app_dict)
    """
    import lib.mp
<<<<<<< Updated upstream
    return lib.mp.interrupt(morpy_trace, app_dict)
=======
    return lib.mp.interrupt(trace, app_dict)


def join_or_task(trace: dict, app_dict: dict) -> None:
    r"""
    Waits in a loop until all spawned tasks have completed or a new task appears for the current process.
    This function is used to synchronize transitions between app phases.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :example:
        morPy.join_or_task(trace, app_dict)
    """
    import lib.mp
    return lib.mp.join_or_task(trace, app_dict)


def log(trace: dict, app_dict: dict, log_level: str, message: callable, verbose: bool=False):
    r"""
    Constructs and dispatches a log entry based on a specified severity level. The log message is
    generated by a supplied callable so that its evaluation is deferred until needed. The function
    updates event counters, sends the message to configured outputs (text file, database, console),
    and may trigger an interrupt if the level requires it.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param log_level: Severity: debug/info/warning/error/critical/denied
    :param message: A callable (e.g., lambda or function) that returns the log message.
    :param verbose: If True, message is only logged in verbose mode.

    :example:
        from morPy import log

        log(trace, app_dict, "info",
        lambda: "Hello world!")
    """

    import lib.msg as msg

    # Skip logging, if message is verbose and verbose is disabled
    if verbose and not app_dict["morpy"]["conf"].get("msg_verbose", False):
        return
    else:
        log_level = log_level.lower()

        if message and app_dict["morpy"]["logs_generate"].get(log_level, False):
            msg.log(trace, app_dict, log_level, message(), verbose)
>>>>>>> Stashed changes


def path_join(path_parts, file_extension):
    r"""
    Joins a tuple of path components into a single OS‑appropriate path string. If a file extension
    is provided (and not already part of the tuple), it is appended. Returns a pathlib.Path object
    representing the constructed path; if the input isn’t a tuple, returns None.

    :param path_parts: Tuple of parts to be joined. Exact order is critical. Examples:
                     ('C:', 'This', 'is', 'my', 'path', '.txt') - C:\This\is\my\path.txt
                     ('T:This_Fol', 'der_Will_Be_Split', 'this_Way') - T:\This_Fol\der_Will_Be_Split\this_Way
                     ('Y:', 'myFile.txt') - Y:\myFile.txt
    :param file_extension: String of the file extension (i.e. '.txt'). Leave
                         empty if path is a directory (None or '') or if the tuple already includes the
                         file extension.
    :return path_obj: OS path object of the joined path parts. Is None, if path_parts is not a tuple.
    """
    import lib.fct
    return lib.fct.path_join(path_parts, file_extension)


def pathtool(in_path):
    r"""
    Converts an input string into an absolute path using pathlib, and returns a dictionary
    containing: the normalized path; booleans indicating whether it represents a file or directory;
    existence checks; the file or directory name; any file extension; and the parent directory path.

    :param in_path: Path to be converted

    :return: dict
        out_path - Same as the input, but converted to a path.
        is_file - The path is a file path. File does not need to exist.
        file_exists - The file has been found under the given path.
        file_name - This is the actual file name.
        file_ext - This is the file extension or file type.
        is_dir - The path is a directory. Directory does not need to exist.
        dir_exists - The directory has been found under the given path.
        dir_name - This is the actual directory name.
        parent_dir - Path of the parent directory.

    :example:
        file_path = "C:\my_file.txt"
        file_path = morPy.pathtool(file_path)["out_path"]
    """
    import lib.fct
    return lib.fct.pathtool(in_path)

<<<<<<< Updated upstream
def perfinfo():
=======

def perf_info():
>>>>>>> Stashed changes
    r"""
    Gathers and returns a set of hardware and performance metrics including: boot time,
    physical and logical CPU counts, maximum/minimum/current CPU frequencies, system-wide
    CPU utilization (both overall and individual cores), total physical memory (MB),
    available memory, used memory, and free memory.

    :return: dict
        boot_time - Timestamp of the latest recorded boot process.
        cpu_count_phys - Return the number of physical CPUs in the system.
        cpu_count_log - Return the number of logical CPUs in the system.
        cpu_freq_max - Return the maximum CPU frequency expressed in Mhz.
        cpu_freq_min - Return the minimum CPU frequency expressed in Mhz.
        cpu_freq_comb - Return the combined CPU frequency expressed in Mhz.
        cpu_perc_comb - Returns the current combined system-wide CPU utilization as a percentage.
        cpu_perc_indv - Returns the current individual system-wide CPU utilization as a percentage.
        mem_total_MB - Total physical memory in MB (exclusive swap).
        mem_available_MB - Memory in MB that can be given instantly to processes without the system going into swap.
        mem_used_MB - Memory used in MB.
        mem_free_MB - Memory not being used at all (zeroed) that is readily available in MB.
    """
    import lib.fct
    return lib.fct.perfinfo()

<<<<<<< Updated upstream
def process_q(morpy_trace: dict, app_dict: dict, task: Callable | list | tuple=None, priority: int=100,
              autocorrect: bool=True):
    r"""
    This function enqueues a task in the morPy multiprocessing queue. The task is a
    tuple, that demands the positional arguments (func, morpy_trace, app_dict, *args, **kwargs).
=======

def process_q(trace: dict, app_dict: dict, task: Callable | list | tuple=None, priority: int=100,
              autocorrect: bool=True):
    r"""
    Enqueues a task into the morPy multiprocessing queue at the specified priority (with lower numbers
    indicating higher priority). The task may be provided as a callable, list, or tuple containing the
    function, positional arguments, and an optional dictionary of keyword arguments. An autocorrect flag
    ensures that the priority does not drop below zero unless explicitly allowed.
>>>>>>> Stashed changes

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param task: Callable, list or tuple packing the task. Formats:
        callable: partial(func, *args, **kwargs)
        list: [func, *args, {"kwarg1": val1, "kwarg2": val2, ...}]
        tuple: (func, *args, {"kwarg1": val1, "kwarg2": val2, ...})
    :param priority: Integer representing task priority (lower is higher priority)
    :param autocorrect: If False, priority can be smaller than zero. Priority
        smaller zero is reserved for the morPy Core. However, it is a devs choice
        to make.

    :return:
        -

    :example:
        from morPy import process_q
        from functools import partial
        message = "Gimme 5"
        def gimme_5(morpy_trace, app_dict, message):
            print(message)
            return message
        a_number = partial(gimme_5, morpy_trace, app_dict, message) # List of a callable, *args and **kwargs
        enqueued = process_q(morpy_trace, app_dict, task=a_number, priority=20) #
        if not enqueued:
            print("No, thank you!")
    """

    import lib.mp
    return lib.mp.heap_shelve(morpy_trace, app_dict, priority=priority, task=task, autocorrect=autocorrect)

<<<<<<< Updated upstream
def qrcode_generator_wifi(morpy_trace: dict, app_dict: dict, ssid: str = None, password: str = None,
                          file_path: str = None, file_name: str = None, overwrite: bool = True) -> dict:
=======

def qrcode_generator_wifi(trace: dict, app_dict: dict, ssid: str = None, password: str = None,
                          file_path: str = None, file_name: str = None, overwrite: bool = True) -> None:
>>>>>>> Stashed changes
    r"""
    Generates a QR code that encodes Wi‑Fi network credentials (SSID and WPA2 password) to allow easy
    network connection via scanning. The QR code is saved as a PNG file in a specified directory
    (defaulting to ‘./data’), and by default will overwrite any existing file with the same name.
    (It is recommended not to hardcode passwords in source code.)

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param ssid: Name of the Wi-Fi network.
    :param password: WPA2 password of the network. Consider handing the password via prompt instead
        of in code for better security.
    :param file_path: Path where the qr-code generated will be saved. If None, save in '.\data'.
    :param file_name: Name of the file without file extension (always PNG). Default to '.\qrcode.png'.
    :param overwrite: If False, will not overwrite existing files. Defaults to True.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        from morPy import qrcode_generator_wifi
        qrcode_generator_wifi(morpy_trace, app_dict,
            ssid="ExampleNET",
            password="3x4mp13pwd"
        )
    """
    import lib.common
    return lib.common.qrcode_generator_wifi(
        morpy_trace, app_dict, ssid=ssid, password=password, file_path=file_path, file_name=file_name,
        overwrite=overwrite
    )

<<<<<<< Updated upstream
def regex_findall(morpy_trace: dict, app_dict: dict, search_obj: object, pattern: str):
=======

def regex_findall(trace: dict, app_dict: dict, search_obj: object, pattern: str) -> dict:
>>>>>>> Stashed changes
    r"""
    Searches the input (converted to a string) for all occurrences of a given regular expression
    pattern and returns a list of all matching substrings, or None if no matches are found.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to search in for the regular expression (converted to a string).
    :param pattern: The regular expression pattern to search for.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        result: List of expressions found in the input, or None if nothing was found.

    :example:
        string = "Find digits 12345"
        pattern = r"\\d+"
        result = regex_findall(morpy_trace, app_dict, string, pattern)["result"]
    """
    import lib.common
    return lib.common.regex_findall(morpy_trace, app_dict, search_obj, pattern)

<<<<<<< Updated upstream
def regex_find1st(morpy_trace: dict, app_dict: dict, search_obj: object, pattern: str):
=======

def regex_find1st(trace: dict, app_dict: dict, search_obj: object, pattern: str) -> dict:
>>>>>>> Stashed changes
    r"""
    Searches the input string for the first occurrence of a specified regular expression pattern
    and returns that match, or None if there is no match.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to search in for the regular expression (converted to a string).
    :param pattern: The regular expression pattern to search for.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        result: The first match found in the input, or None if nothing was found.

    :example:
        string = "Find digits 12345"
        pattern = r"\\d+"
        result = regex_find1st(morpy_trace, app_dict, string, pattern)["result"]
    """
    import lib.common
    return lib.common.regex_find1st(morpy_trace, app_dict, search_obj, pattern)

<<<<<<< Updated upstream
def regex_split(morpy_trace: dict, app_dict: dict, search_obj: object, delimiter: str):
=======

def regex_split(trace: dict, app_dict: dict, search_obj: object, delimiter: str) -> dict:
>>>>>>> Stashed changes
    r"""
    Splits the input (converted to a string) into a list of substrings using the specified
    delimiter. Delimiters that are special characters in regex should be escaped appropriately.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to be split (converted to a string).
    :param delimiter: The character or string used to split `search_obj` into a list.
                      Special characters may require a preceding backslash (e.g., '\\.'
                      to use '.' as a delimiter).

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        result: The list of parts split from the input.

    :example:
        string = "apple.orange.banana"
        split = r"\\."
        result = morPy.regex_split(morpy_trace, app_dict, string, split)["result"]
    """
    import lib.common
    return lib.common.regex_split(morpy_trace, app_dict, search_obj, delimiter)

<<<<<<< Updated upstream
def regex_replace(morpy_trace: dict, app_dict: dict, search_obj: object, search_for: str, replace_by: str):
=======

def regex_replace(trace: dict, app_dict: dict, search_obj: object, search_for: str, replace_by: str) -> dict:
>>>>>>> Stashed changes
    r"""
    Replaces every occurrence of a regular expression pattern in the input string with a
    provided replacement string, returning the modified string.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object in which to search and replace (converted to a string).
    :param search_for: The regular expression pattern to search for.
    :param replace_by: The character or string to substitute in place of the matches.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        result: The modified string with substitutions applied.

    :example:
        string = "apple.orange.banana"
        search_for = r"\\."
        replace_by = r"-"
        result = regex_replace(morpy_trace, app_dict, string, search_for, replace_by)["result"]
    """
    import lib.common
    return lib.common.regex_replace(morpy_trace, app_dict, search_obj, search_for, replace_by)

<<<<<<< Updated upstream
def regex_remove_special(morpy_trace: dict, app_dict: dict, inp_string: str, spec_lst: list):
=======

def regex_remove_special(trace: dict, app_dict: dict, inp_string: str, spec_lst: list) -> dict:
>>>>>>> Stashed changes
    r"""
    Processes the input string to remove or replace special characters according to a list of
    (special, replacement) tuples. If a default list is requested (by specifying an empty tuple),
    a standard set of common special characters is used.

    This function can also perform multiple `regex_replace` actions on the same string,
    as any valid regular expression can be used in the `spec_lst`.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param inp_string: The string to be altered.
    :param spec_lst: A list of 2-tuples defining the special characters to replace and
                     their replacements. Example:
                     [(special1, replacement1), ...]. Use `[('', '')]` to invoke the
                     standard replacement list.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        result: The modified string with special characters replaced or removed.

    :example:
        result = regex_remove_special(
            morpy_trace, app_dict, "Hello!@#$%^&*()", [("@", "AT"), ("!", "")]
        )
    """
    import lib.common
    return lib.common.regex_remove_special(morpy_trace, app_dict, inp_string, spec_lst)


def runtime(in_ref_time):
    r"""
    Computes the elapsed time (as a timedelta) between the current time and a
    reference time provided as input.

    :param in_ref_time: Value of the reference time to calculate the actual runtime

    :return: dict
        rnt_delta - Value of the actual runtime.
    """
    import lib.fct
    return lib.fct.runtime(in_ref_time)


def sysinfo():
    r"""
    Returns a dictionary of system information including: operating system name, release and
    version, architecture and processor details, logical CPU count, total system memory in
    bytes, username, home directory, hostname, and the primary monitor’s resolution (width
    and height).

    :return: dict
        system - Operating system.
        release - Major version of the operating system.
        version - Major and sub-version of the operating system.
        arch - Architecture of the operating system.
        processor - Processor running the code.
        logical_cpus - Amount of processes, that could run in parallel.
        sys_memory_bytes - Physical system memory in bytes
        username - Returns the username.
        homedir - Returns the home directory.
        hostname - Returns the host name.
    """
    import lib.fct
    return lib.fct.sysinfo()

<<<<<<< Updated upstream
def textfile_write(morpy_trace: dict, app_dict: dict, filepath: str, content: str):
=======

def textfile_write(trace: dict, app_dict: dict, filepath: str, content: str) -> None:
>>>>>>> Stashed changes
    r"""
    Appends text content to a specified file. If the file does not exist, it is created.
    The content is converted to a string as needed.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param filepath: Path to the text file, including its name and file extension.
    :param content: The content to be written to the file, converted to a string if necessary.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).

    :example:
        result = textfile_write(morpy_trace, app_dict, "path/to/file.txt", "This is some text.")
    """
    import lib.common
    return lib.common.textfile_write(morpy_trace, app_dict, filepath, content)

<<<<<<< Updated upstream
def testprint(morpy_trace: dict, app_dict: dict, message: str):
    r"""
    Prints any value provided. This function is intended for debugging purposes.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param message: The value to be printed, converted to a string if necessary.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check - The function ended with no errors

    :example:
        mpy.testprint(morpy_trace, app_dict, "This is a test value.")
    """
    import lib.common
    return lib.common.testprint(morpy_trace, app_dict, message)

def tracing(module, operation, morpy_trace):
    r"""
    This function formats the trace to any given operation. This function is
    necessary to alter the morpy_trace as a pass down rather than pointing to the
    same morpy_trace passed down by the calling operation. If morpy_trace is to be altered
    in any way (i.e. 'log_enable') it needs to be done after calling this function.
    This is why this function is called at the top of any morPy-operation.

    :param module: Name of the module, the operation is defined in (i.e. 'common')
    :param operation: Name of the operation executed (i.e. 'tracing(~)')
    :param morpy_trace: operation credentials and tracing

    :return morpy_trace_passdown: operation credentials and tracing
    """
    import lib.fct
    return lib.fct.tracing(module, operation, morpy_trace)

def wait_for_input(morpy_trace: dict, app_dict: dict, message: str):
=======

def wait_for_input(trace: dict, app_dict: dict, message: str) -> dict:
>>>>>>> Stashed changes
    r"""
    Pauses execution until the user provides input at a command‑line prompt. The supplied message
    is displayed, and the user input (always returned as a string) is captured.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param message: The text to be displayed as a prompt before user input.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check - The function ended with no errors
        usr_input: The input provided by the user.

    :example:
        prompt = "Please enter your name: "
        result = wait_for_input(morpy_trace, app_dict, prompt)["usr_input"]
    """
    import lib.common
    return lib.common.wait_for_input(morpy_trace, app_dict, message)

<<<<<<< Updated upstream
def wait_for_select(morpy_trace: dict, app_dict: dict, message: str, collection: tuple=None):
=======

def wait_for_select(trace: dict, app_dict: dict, message: str, collection: tuple=None):
>>>>>>> Stashed changes
    r"""
    Prompts the user for input that must match one of the elements in a provided tuple. If the
    entered input is invalid, the prompt is repeated (or the process is aborted) until a valid
    option is selected.

    :param morpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param message: The text to be displayed as a prompt before user input.
    :param collection: Tuple, that holds all valid user input options. If None,
        evaluation will be skipped.

    :return: dict
        morpy_trace: Operation credentials and tracing.
        check - The function ended with no errors
        usr_input: The input provided by the user.

    :example:
        msg_text = "Select 1. this or 2. that"
        collection = (1, 2)
        result = wait_for_select(morpy_trace, app_dict, msg_text, collection)["usr_input"]
    """
    import lib.common
    return lib.common.wait_for_select(morpy_trace, app_dict, message, collection)
