r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Frontend of the morPy framework.
"""

from collections.abc import Callable

class FileDirSelectTk:
    r"""
    A tkinter GUI for file and directory selection. Each row represents a file or directory selection.
    Optionally displays a top row of icons (display only).
    """

    def __init__(self, trace: dict, app_dict: dict, rows_data: dict, title: str = None,
                 icon_data: dict = None) -> None:
        r"""
        A tkinter GUI for file and directory selection. Each row represents a file or directory selection.
        Optionally displays a top row of icons (display only).
        selection rows.

        :param trace: Operation credentials and tracing information.
        :param app_dict: morPy global dictionary containing app configurations.
        :param rows_data: Dictionary defining the selection rows.
            Expected structure:
                {"selection_name" : {
                    "is_dir" : True | False,  # True for directory selection, False for file selection.
                    "file_types" : (('PDF','*.pdf'), ('Textfile','*.txt'), ('All Files','*.*')),  # For file dialogs.
                    "image_path" : "path/to/image.png",  # Optional custom image.
                    "image_size" : (width, height),  # Optional; defaults to (48, 48) if not provided.
                    "default_path" : "prefilled/default/path"  # Optional prefill for the input.},
                    ...}
        :param title: Title of the tkinter window. Defaults to morPy localization if not provided.
        :param icon_data: (Optional) Dictionary containing configuration for top row icons. Defaults to None.
            Expected structure:
                {"icon_name" : {
                    "position" : 1,                       # placement, order (lowest first)
                    "img_path" : "path/to/image.png",     # image file path
                    "icon_size" : (width, height),        # (optional) size for the icon},
                    ...}

        :return: dict
            trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
            selections: Dictionary with selections made, keyed with the row name. Example:
                {"selection_name" : value}

        :example:
            import morPy

            icon_data = {
                "company_logo1" : {
                    "position" : 1,                                         # placement, order (lowest first)
                    "img_path" : app_dict["morpy"]["conf"]["app_icon"],     # image file path
                }
            }
            selection_config = {
                "file_select" : {
                    "is_dir" : False,
                    "file_types" : (('Textfile','*.txt'), ('All Files','*.*')),
                    "default_path" : app_dict["morpy"]["conf"]["data_path"]
                },
                "dir_select" : {
                    "is_dir" : True,
                    "default_path" : app_dict["morpy"]["conf"]["data_path"]
                }
            }
            gui = morPy.FileDirSelectTk(trace, app_dict, selection_config, title="Select...")
            results = gui.run(trace, app_dict)["selections"]
            file = results["file_selected"]
            directory = results["dir_selected"]
        """
        import lib.ui_tk
        self._impl = lib.ui_tk.FileDirSelectTk(
            trace, app_dict, rows_data=rows_data, title=title, icon_data=icon_data
        )

    def run(self, trace: dict, app_dict: dict):
        r"""
        Launches the GUI and waits for the user to complete the selection.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
            selections: A dictionary of user inputs keyed by row name.
        """
        return self._impl.run(trace, app_dict)

class GridChoiceTk:
    r"""
    A tkinter GUI displaying a dynamic grid of image tiles. Each tile shows an image
    with a text label below it. Clicking a tile returns its associated value.
    """

    def __init__(self, trace: dict, app_dict: dict, tile_data: dict, title: str=None,
                 default_tile_size: tuple=None, icon_data: dict=None):
        r"""
        A tkinter GUI displaying a dynamic grid of image tiles. Each tile shows an image
        with a text label below it. Clicking a tile returns its associated value.

        :param trace: Operation credentials and tracing information
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
            trace: Operation credentials and tracing
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
            gui = morPy.GridChoiceTk(trace, app_dict, tile_data,
                title="Start Menu",
                default_tile_size=(128, 128),
                icon_data=icon_data
            )
            result = gui.run(trace, app_dict)["choice"]
        """
        import lib.ui_tk
        self._impl = lib.ui_tk.GridChoiceTk(
            trace, app_dict, tile_data=tile_data, title=title, default_tile_size=default_tile_size,
            icon_data=icon_data
        )

    def run(self, trace: dict, app_dict: dict):
        r"""
        Launches the GUI and waits for the user to make a selection.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            trace: Operation credentials and tracing
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
            gui = morPy.GridChoiceTk(trace, app_dict, tile_data,
                title="Start Menu",
                default_tile_size=(128, 128),
            )
            result = gui.run(trace, app_dict)["choice"]
        """
        return self._impl.run(trace, app_dict)

class MorPyException(Exception):
    r"""
    This wraps errors in the standard morPy fashion. If one of the arguments
    required for logging is missing, this wrapper will raise other errors in
    order to reduce tracebacks and specifically point to the issue at hand.
    """

    def __init__(self, trace: dict, app_dict: dict, exception_obj: BaseException, line: int,
                 log_level: str, message: str = None) -> None:
        r"""
        :param trace: Operation credentials and tracing information.
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
                    trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "info",
                    message="Specifics regarding the error"
                )
        """
        import lib.exceptions
        self._impl = lib.exceptions.MorPyException(
            trace, app_dict, exception_obj, line, log_level, message=message
        )

class PriorityQueue:
    r"""
    PriorityQueue implements a task queue with priority handling.
    When tasks are enqueued, the task with the lowest (highest priority) number
    is pulled first.
    """

    def __init__(self, trace: dict, app_dict: dict, name: str = None) -> None:
        r"""
        Class constructor.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param name: Name or description of the instance
        """
        import lib.common
        self._impl = lib.common.PriorityQueue(trace, app_dict, name=name)

    def enqueue(self, trace: dict, app_dict: dict, priority: int=100, task: tuple=None) -> None:
        r"""
        Adds a task to the priority queue.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param priority: Integer representing task priority (lower is higher priority)
        :param task: Tuple of a callable, *args and **kwargs (func, *args, **kwargs)

        :example:
            from functools import partial
            queue = PriorityQueue(trace, app_dict, name="example_queue")
            task = partial(my_func, trace, app_dict)
            queue.enqueue(trace, app_dict, priority=25, task=task)
        """
        return self._impl.enqueue(trace, app_dict, priority=priority, task=task)

    def pull(self, trace: dict, app_dict: dict) -> dict:
        r"""
        Removes and returns the highest priority task from the priority queue.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            trace: Operation credentials and tracing
            check: Indicates if the task was pulled successfully
            priority: Integer representing task priority (lower is higher priority)
            counter: Number of the task when enqueued
            task_id : Continuously incremented task ID (counter).
            task_sys_id : ID of the task determined by Python core
            task: The pulled task list
            task_callable: The pulled task callable

        :example:
            from functools import partial
            queue = PriorityQueue(trace, app_dict, name="example_queue")
            task = queue.pull(trace, app_dict)['task']
            task()
        """
        return self._impl.pull(trace, app_dict)

class ProgressTracker:
    r"""
    Progress counter to continuously keep track of operations.
    """

    def __init__(self, trace: dict, app_dict: dict, description: str=None, total: float=None, ticks: float=None,
                 float_progress: bool=False, verbose: bool=False) -> None:
        r"""
        Class constructor.

        :param trace: operation credentials and tracing information
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
            prog_tracker = morPy.ProgressTracker(trace, app_dict, description=description, total=total, ticks=ticks)
        """
        import lib.common
        self._impl = lib.common.ProgressTracker(
            trace, app_dict, description=description, total=total, ticks=ticks,
            float_progress=float_progress, verbose=verbose
        )

    def update(self, trace: dict, app_dict: dict, current: float = None) -> dict:
        r"""
        Method to update current progress and log progress if tick is passed.

        :param trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param current: Current progress count. If None, each call of this method will add +1
            to the progress count. Defaults to None.

        :return: dict
            prog_rel: Relative progress, float between 0 and 1
            prog_abs: Absolute progress, float between 0.00 and 100.00
            message: Message generated. None, if no tick was hit.

        :example:
            import morPy

            tot_cnt = 100
            tks = 12.5
            prog_tracker = morPy.ProgressTracker(trace, app_dict, description='App Progress', total=total_count, ticks=tks)

            curr_cnt = 37
            prog_tracker.update(trace, app_dict, current=curr_cnt)
        """
        return self._impl.update(trace, app_dict, current=current)

class ProgressTrackerTk:
    r"""
    A progress tracking GUI using tkinter to visualize the progress of a task.
    If progress consists of several stages, a separate progress bar for the
    stages progress is displayed. The total count of progress steps is set by
    initializing a stage with the 'begin_stage()' method, regardless of the total
    amount of stages. Optionally allows to display console messages in a console
    widget.
    """

    def __init__(self, trace: dict, app_dict: dict, frame_title: str=None, frame_width: int=None,
              frame_height: int=None, headline_total: str=None, headline_font_size: int=10,
              detail_description_on: bool=False, description_font_size: int=8, font: str="Arial",
              stages: int=1, console: bool=False, auto_close: bool=False, work=None):

        r"""
        Initializes the GUI with progress tracking.

        :param trace: Operation credentials and tracing information
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
            trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            gui = morPy.ProgressTrackerTk(trace: dict, app_dict,
                frame_title="My Demo Progress GUI",
                detail_description="Generic Progress stage",
                stages=outer_loop_count,
                stage_limit=inner_loop_count,
                work=work)
        """
        import lib.ui_tk
        self._impl = lib.ui_tk.ProgressTrackerTk(
            trace, app_dict, frame_title=frame_title, frame_width=frame_width, frame_height=frame_height,
            headline_total=headline_total, headline_font_size=headline_font_size,
            detail_description_on=detail_description_on, description_font_size=description_font_size, font=font,
            stages=stages, console=console, auto_close=auto_close, work=work
        )

    def run(self, trace: dict, app_dict: dict):
        r"""
        Start the GUI main loop and run the Tk mainloop on the main thread.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            progress = morPy.ProgressTrackerTk(trace: dict, app_dict,
                frame_title="My Demo Progress GUI",
                detail_description="Generic Progress stage",
                stages=1,
                stage_limit=10,
                work=work)

            progress.run(trace, app_dict)
        """
        return self._impl.run(trace, app_dict)

    def begin_stage(self, trace: dict, app_dict: dict, stage_limit: (int, float) = 1, headline_stage: str = None,
                    detail_description: str=None, ticks: float=.01):
        r"""
        Start a new stage of progress. Will set the stage prior to 100%, if
        not already the case.

        :param trace: Operation credentials and tracing information
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
            trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            # Set up the next stage
            headline = "Currently querying"
            description = "Starting stage..."
            progress.begin_stage(trace, app_dict, stage_limit=10, headline_stage=headline,
            detail_description=description)
        """
        return self._impl.run(
            trace, app_dict, stage_limit=stage_limit, headline_stage=headline_stage,
            detail_description=detail_description, ticks=ticks
        )

    def update_progress(self, trace: dict, app_dict: dict, current: float = None) -> dict:
        r"""
        Update stage progress & overall progress. If overall hits 100% and auto_close=True, close window. Else,
        switch button text to "Close" and stop console redirection. Enqueues a UI request for the
        main thread to process. Safe to call from any thread.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param current: Current progress count. If None, each call of this method will add +1
            to the progress count. Defaults to None.

        :return: dict
            trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            progress = morPy.ProgressTrackerTk(trace: dict, app_dict,
                frame_title="My Demo Progress GUI",
                detail_description="Starting stage 1",
                stages=2,
                stage_limit=10,
                work=work)

            progress.run(trace, app_dict)

            curr_cnt = 5.67
            msg = f'Currently at {curr_cnt}'
            progress.update_progress(trace, app_dict, current=curr_cnt, detail_description=msg)

            # stage 1 is at 100%
            curr_cnt = 10
            msg = f'Currently at {curr_cnt}'
            progress.update_progress(trace, app_dict, current=curr_cnt, detail_description=msg)

            # Setup stage 2
            progress.update_text(trace, app_dict,
                headline_stage="Starting stage 2",
                detail_description="Now copying data...",
            )
            progress.update_progress(trace, app_dict, current=0, stage_limit=15)

            # stage 2 is at 100%
            curr_cnt = 15
            msg = f'Currently at {curr_cnt}'
            progress.update_progress(trace, app_dict, current=curr_cnt, detail_description=msg)
        """
        return self._impl.update_progress(trace, app_dict, current=current)

    def update_text(self, trace: dict, app_dict: dict, headline_total: str = None, headline_stage: str = None,
                    detail_description: str = None):
        r"""
        Update the headline texts or description at runtime. Enqueues a UI request for the
        main thread to process. Safe to call from any thread.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param headline_total: If not None, sets the overall progress headline text.
        :param headline_stage: If not None, sets the stage progress headline text.
        :param detail_description: If not None, sets the description text beneath the stage headline.

        :return: dict
            trace: Operation credentials and tracing
            check: Indicates whether text update completed without errors

        :example:
            gui.update_text(trace, app_dict,
                headline_total="Processing Outer Loop 3",
                headline_stage="Processing File 5",
                detail_description="Now copying data...")
        """
        return self._impl.update_text(
            trace, app_dict, headline_total=headline_total, headline_stage=headline_stage,
            detail_description=detail_description
        )

    def end_stage(self, trace: dict, app_dict: dict):
        r"""
        End the current stage by setting it to 100%.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self.end_stage(trace, app_dict)
        """
        return self._impl.end_stage(trace, app_dict)

class XlWorkbook:
    r"""
    Instantiates an Excel workbook to edit, read from and write to it.
    It uses OpenPyXL as the API to the workbooks.
    """

    def __init__(self, trace: dict, app_dict: dict, workbook: str, create: bool=False,
              data_only: bool=False, keep_vba: bool=True) -> None:
        r"""
        Helper method for initialization to ensure @metrics decorator usage.

        :param trace: operation credentials and tracing information
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
            trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self._init(trace, app_dict)
        """

        import lib.xl
        self._impl = lib.xl.XlWorkbook(
            trace, app_dict, workbook, create=create, data_only=data_only, keep_vba=keep_vba
        )

    def save_workbook(self, trace: dict, app_dict: dict, close_workbook: bool=False) -> dict:
        r"""
        Saves the changes to the MS Excel workbook.

        :param trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param close_workbook: If True, closes the workbook.

        :return: dict
            trace: Operation credentials and tracing.
            check: Indicates whether the function executed successfully (True/False).
            wb_obj: Returns None, if the object was closed. Else returns self. Used to delete the
                reference to an instance.

        :example:
            wb_path = "C:\my.xlsx"
            wb = XlWorkbook(trace, app_dict, wb_path)

            # Save and close the workbook. Write "None" to the reference "wb".
            wb = wb.save_workbook(trace, app_dict, close=True)["wb_obj"]
            print(f'{wb}')
        """
        return self._impl.save_workbook(trace, app_dict, close_workbook=close_workbook)

    def close_workbook(self, trace: dict, app_dict: dict) -> dict:
        r"""
        Closes the MS Excel workbook.

        :param trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.

        :return: dict
            wb_obj: Returns None, if the object was closed. Else returns self. Used to delete the
                reference to an instance.

        :example:
            wb_path = "C:\my.xlsx"
            wb = XlWorkbook(trace, app_dict, wb_path)

            # Close the workbook. Write "None" to the reference "wb".
            wb = wb.close_workbook(trace, app_dict)["wb_obj"]
            print(f'{wb}')
        """
        return self._impl.close_workbook(trace, app_dict)

    def activate_worksheet(self, trace: dict, app_dict: dict, worksheet: str) -> dict:
        r"""
        Activates a specified worksheet in the workbook. If the sheet is not found,
        an error is logged.

        :param trace: Operation credentials and tracing information.
        :param app_dict: The morPy global dictionary containing app configurations.
        :param worksheet: The name of the worksheet to activate.

        :example:
            wb_path = "C:\my.xlsx"
            wb = XlWorkbook(trace, app_dict, wb_path)
            w_sht = "Sheet1"
            wb.activate_worksheet(trace, app_dict, w_sht)
        """
        return self._impl.activate_worksheet(trace, app_dict, worksheet)

    def read_cells(self, trace: dict, app_dict: dict, cell_range: list=None,
                   cell_styles: bool=False, worksheet: str=None, gui=None) -> dict:
        r"""
        Reads the cells of MS Excel workbooks. Overlapping ranges will get auto-formatted
        to ensure every cell is addressed only once.

        :param trace: Operation credentials and tracing information.
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
            trace: Operation credentials and tracing.
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
            wb = morPy.XlWorkbook(trace, app_dict, wb_path)
            cl_dict = wb.read_cells(trace, app_dict, worksheet="Sheet1", cell_range=["A1", "B2:C3"])["cl_dict"]
            print(f'{cl_dict}')
        """
        return self._impl.read_cells(
            trace, app_dict, cell_range=cell_range, cell_styles=cell_styles, worksheet=worksheet, gui=gui
        )

    def write_ranges(self, trace: dict, app_dict: dict, worksheet: str=None, cell_range: list=None,
                     cell_writes: list=None, fill_range: bool=False, style_default: bool=False,
                     save_workbook: bool=True, close_workbook: bool=False) -> dict:
        r"""
        Writes data into cells of an Excel workbook. OpenPyXL documentation:
        https://openpyxl.readthedocs.io/en/stable/api/openpyxl.cell.cell.html#openpyxl.cell.cell.Cell
        https://openpyxl.readthedocs.io/en/3.1.3/styles.html

        :param trace: Operation credentials and tracing information.
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
            wb = wb.write_cells(trace, app_dict, worksheet=w_sh, cell_range=cl_rng, cell_writes=cell_writes
                                save_workbook=True, close_workbook=True)["wb_obj"]
        """
        return self._impl.write_ranges(
            trace, app_dict, worksheet=worksheet, cell_range=cell_range, cell_writes=cell_writes,
            fill_range=fill_range, style_default=style_default, save_workbook=save_workbook,
            close_workbook=close_workbook
        )

def app_dict_to_string(app_dict):
    r"""
    This function creates a string for the entire app_dict. May exceed memory.

    :param app_dict: morPy global dictionary

    :return app_dict_str: morPy global dictionary as a UTF-8 string

    :example:
        morPy.app_dict_to_string(app_dict) # Do not specify depth!
    """
    import lib.fct
    return lib.fct.app_dict_to_string(app_dict)

def csv_read(trace: dict, app_dict: dict, src_file_path: str=None, delimiter: str=None,
             print_csv_dict: bool=False, log_progress: bool=False, progress_ticks: float=None, gui=None) -> dict:
    r"""
    This function reads a csv file and returns a dictionary of
    dictionaries. The header row, first row of data and delimiter
    is determined automatically.

    :param trace: Operation credentials and tracing
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
        csv = morPy.csv_read(trace, app_dict, src_file_path, delimiter)
        csv_header1 = csv["csv_dict"]["DATA1"]["header"]
    """
    import lib.csv
    return lib.csv.csv_read(
        trace, app_dict, src_file_path=src_file_path, delimiter=delimiter,
        print_csv_dict=print_csv_dict, log_progress=log_progress, progress_ticks=progress_ticks, gui=gui
    )

def csv_dict_to_excel(trace: dict, app_dict: dict, xl_path: str=None, overwrite: bool=False,
                      worksheet: str=None, close_workbook: bool=False, csv_dict: dict=None,
                      log_progress: bool=False, progress_ticks: float=None) -> dict:
    r"""
    This function takes da dictionary as provided by csv_read() and saves it as an MS Excel file.
    The csv_dict however may be evaluated and processed prior to executing csv_dict_to_excel().
    The file will be saved automatically, but closing the workbook is optional.

    :param trace: Operation credentials and tracing
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
        wb_obj: Returns None, if the object was closed. Else returns an instance of "xl.XlWorkbook()".
            Used to delete the reference to an instance.

    :example:
        src_file_path = 'C:\my.csv'
        delimiter = '","'
        csv = morPy.csv_read(trace, app_dict, src_file_path, delimiter)

        # ... process data in csv["csv_dict"] ...

        target_path = 'C:\my.xlsx'
        wb_sht = 'Sheet1'
        wb = morPy.csv_dict_to_excel(trace, app_dict, csv_dict=csv["csv_dict"], xl_path=target_path,
            overwrite=True, worksheet=wb_sht)["wb_obj"]

        # ... modify 'C:\my.xlsx' ...

        # Save and close workbook
        wb.close_workbook(mpy_trac, app_dict, save_workbook=True, close_workbook=True)
    """
    import lib.csv
    return lib.csv.csv_dict_to_excel(
        trace, app_dict, xl_path=xl_path, overwrite=overwrite, worksheet=worksheet, close_workbook=close_workbook,
        csv_dict=csv_dict, log_progress=log_progress, progress_ticks=progress_ticks
    )

def datetime_now():
    r"""
    This function reads the current date and time and returns formatted
    stamps.

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

def decode_to_plain_text(trace: dict, app_dict: dict, src_input: str, encoding: str=''):
    r"""
    This function decodes different types of data and returns
    a plain text to work with in python. The return result behaves
    like using the open(file, 'r') method.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param src_input: Any kind of data to be decoded. Binary expected.
    :param encoding: String that defines encoding. Leave empty to auto-detect.

    :return: dict
        result: Decoded result. Buffered object that may be used with the readlines() method.
        encoding: String containing the encoding of src_input.
        lines: Number of lines in the file.

    :example:
        src_file = "C:\my_file.enc"
        src_input = open(src_file, 'rb')
        encoding: str = 'utf-16-le'
        retval = decode_to_plain_text(trace, app_dict, src_input, encoding)
    """
    import lib.common
    return lib.common.decode_to_plain_text(trace, app_dict, src_input, encoding=encoding)

def dialog_sel_file(trace: dict, app_dict: dict, init_dir: str=None, file_types: tuple=None, title: str=None):
    r"""
    This function opens a dialog for the user to select a file.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param file_types: This tuple of 2-tuples specifies, which filetypes will be
        selectable in the dialog box.
    :param title: Title of the open file dialog

    :return: dict
        file_path: Path of the selected file
        file_selected: True, if file was selected. False, if canceled.

    :example:
        init_dir = "C:\"
        file_types = (('PDF','*.pdf'),('Textfile','*.txt'),('All Files','*.*'))
        title = 'Select a file...'
        file_path = morPy.dialog_sel_file(trace, app_dict, init_dir=init_dir,
                        file_types=file_types, title=title)["file_path"]
    """
    import lib.ui_tk
    return lib.ui_tk.dialog_sel_file(trace, app_dict, init_dir, file_types, title)

def dialog_sel_dir(trace: dict, app_dict: dict, init_dir: str=None, title: str=None):
    r"""
    This function opens a dialog for the user to select a directory.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param title: Title of the open directory dialog

    :return: dict
        trace: [dictionary] operation credentials and tracing
        check: The function ended with no errors and a file was chosen
        dir_path: Path of the selected directory
        dir_selected: True, if directory was selected. False, if canceled.

    :example:
        init_dir = "C:\"
        title = 'Select a directory...'
        dir_path = morPy.dialog_sel_dir(trace, app_dict, init_dir=init_dir, title=title)["dir_path"]
    """
    import lib.ui_tk
    return lib.ui_tk.dialog_sel_dir(trace, app_dict, init_dir, title)

def find_replace_save_as(trace: dict, app_dict: dict, search_obj, replace_tpl: tuple, save_as: str,
                        overwrite: bool=False) -> None:
    r"""
    This function finds and replaces strings in a readable object
    line by line. The result is saved into a file specified.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param search_obj: Can be any given object to search in for regular expressions. Searches line by line.
    :param replace_tpl: Tuple of tuples. Includes every tuple of regular expressions and what they are supposed
                        to be replaced by.
    :param save_as: Complete path of the file to be saved.
    :param overwrite: True if new files shall overwrite existing ones, if there are any. False otherwise.
                      Defaults to False.

    :example:
        search_obj = "Let's replace1 and replace2!"
        replace_tpl = (("replace1", "with1"), ("replace2", "with2"))
        save_as = "C:\my_replaced_strings.txt"
        overwrite = True
        retval = morPy.find_replace_save_as(trace, app_dict, search_obj, replace_tpl, save_as, overwrite)
    """
    import lib.bulk_ops
    return lib.bulk_ops.find_replace_save_as(
        trace, app_dict, search_obj, replace_tpl, save_as, overwrite=overwrite
    )

def fso_copy_file(trace: dict, app_dict: dict, source: str, dest: str, overwrite: bool=False) -> None:
    r"""
    Copies a single file from the source to the destination. Includes a file
    check to ensure the operation's validity.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param source: Complete path to the source file, including the file extension.
    :param dest: Complete path to the destination file, including the file extension.
    :param overwrite: Boolean indicating if the destination file may be overwritten. Defaults to False.

    :example:
        morPy.fso_copy_file(trace, app_dict, "path/to/source.txt", "path/to/destination.txt", True)
    """
    import lib.common
    return lib.common.fso_copy_file(trace, app_dict, source, dest, overwrite=overwrite)

def fso_create_dir(trace: dict, app_dict: dict, mk_dir: str) -> None:
    r"""
    Creates a directory and its parent directories recursively.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param mk_dir: Path to the directory or directory tree to be created.

    :example:
        morPy.fso_create_dir(trace, app_dict, "path/to/new_directory")
    """
    import lib.common
    return lib.common.fso_create_dir(trace, app_dict, mk_dir)

def fso_delete_dir(trace: dict, app_dict: dict, del_dir: str) -> None:
    r"""
    Deletes an entire directory, including its contents. A directory check
    is performed before deletion.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param del_dir: Path to the directory to be deleted.

    :example:
        morPy.fso_delete_dir(trace, app_dict, "path/to/directory_to_delete")
    """
    import lib.common
    return lib.common.fso_delete_dir(trace, app_dict, del_dir)

def fso_delete_file(trace: dict, app_dict: dict, del_file: str) -> None:
    r"""
    Deletes a file. Will check path before deletion.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param del_file: Path to the file to be deleted.

    :example:
        morPy.fso_delete_file(trace, app_dict, "path/to/file_to_delete.txt")
    """
    import lib.common
    return lib.common.fso_delete_file(trace, app_dict, del_file)

def fso_walk(trace: dict, app_dict: dict, path: str, depth: int=1) -> dict:
    r"""
    Returns the contents of a directory.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param path: Path to the directory to be analyzed.
    :param depth: Limits the depth of the analysis. Defaults to 1. Examples:
                  -1: No limit.
                   0: Path only.

    :return: dict
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
        result = morPy.fso_walk(trace, app_dict, "path/to/directory", -1)["walk_dict"]
    """
    import lib.common
    return lib.common.fso_walk(trace, app_dict, path, depth=depth)

def interrupt(trace: dict, app_dict: dict):
    r"""
    This function sets a global interrupt flag. Processes and threads
    will halt once they pass (the most recurring) morPy functions.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        trace: Operation credentials and tracing
        check: Indicates if the task was pulled successfully

    :example:
        mp.interrupt(trace, app_dict)
    """
    import lib.mp
    return lib.mp.interrupt(trace, app_dict)

def log(trace: dict, app_dict: dict, log_level: str, message: callable, verbose: bool=False):
    r"""
    Wrapper for conditional logging based on log level. To benefit from
    this logic, it is necessary to construct "message" in the lambda shown
    in the example, whereas <message> refers to a localized string like

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

def path_join(path_parts, file_extension):
    r"""
    This function joins components of a tuple to an OS path.

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
    This function takes a string and converts it to a path. Additionally,
    it returns path components and checks.

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

def perf_info():
    r"""
    This function returns performance metrics.

    :return: dict
        boot_time - Timestamp of the latest recorded boot process.
        cpu_count_phys - Return the number of physical CPUs in the system.
        cpu_count_log - Return the number of logical CPUs in the system.
        cpu_freq_max - Return the maximum CPU frequency expressed in Mhz.
        cpu_freq_min - Return the minimum CPU frequency expressed in Mhz.
        cpu_freq_comb - Return the combined CPU frequency expressed in Mhz.
        cpu_perc_comb - Returns the current combined system-wide CPU utilization as a percentage.
        cpu_percent_individual - Returns the current individual system-wide CPU utilization as a percentage.
        mem_total_mb - Total physical memory in MB (exclusive swap).
        mem_available_mb - Memory in MB that can be given instantly to processes without the system going into swap.
        mem_used_mb - Memory used in MB.
        mem_free_mb - Memory not being used at all (zeroed) that is readily available in MB.
    """
    import lib.fct
    return lib.fct.perf_info()

def process_q(trace: dict, app_dict: dict, task: Callable | list | tuple=None, priority: int=100,
              autocorrect: bool=True):
    r"""
    This function enqueues a task in the morPy multiprocessing queue. The task is a
    tuple, that demands the positional arguments (func, trace, app_dict, *args, **kwargs).

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param task: Callable, list or tuple packing the task. Native is 'list' type. Formats:
        callable: partial(func, *args, **kwargs)
        list: [func, *args, {"kwarg1": val1, "kwarg2": val2, ...}]
        tuple: (func, *args, {"kwarg1": val1, "kwarg2": val2, ...})
    :param priority: Integer representing task priority (lower is higher priority)
    :param autocorrect: If False, priority can be smaller than zero. Priority
        smaller zero is reserved for the morPy Core. However, it is a devs choice
        to make.

    :example:
        from morPy import process_q
        from functools import partial
        message = "Gimme 5"
        def gimme_5(trace, app_dict, message):
            print(message)
            return message
        a_number = partial(gimme_5, trace, app_dict, message) # List of a callable, *args and **kwargs
        enqueued = process_q(trace, app_dict, task=a_number, priority=20) #
        if not enqueued:
            print("No, thank you!")
    """

    import lib.mp
    return lib.mp.heap_shelve(trace, app_dict, priority=priority, task=task, autocorrect=autocorrect)

def qrcode_generator_wifi(trace: dict, app_dict: dict, ssid: str = None, password: str = None,
                          file_path: str = None, file_name: str = None, overwrite: bool = True) -> None:
    r"""
    Create a QR-code for a Wi-Fi network. Scanning the QR-Code will offer a quick-connect to
    the regarding Wi-Fi network. Output file will be overwritten by default.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param ssid: Name of the Wi-Fi network.
    :param password: WPA2 password of the network. Consider handing the password via prompt instead
        of in code for better security.
    :param file_path: Path where the qr-code generated will be saved. If None, save in '.\data'.
    :param file_name: Name of the file without file extension (always PNG). Default to '.\qrcode.png'.
    :param overwrite: If False, will not overwrite existing files. Defaults to True.

    :example:
        # Never save a password in the source code!
        morPy.qrcode_generator_wifi(trace, app_dict,
            ssid="ExampleNET",
            password="3x4mp13pwd"
        )
    """
    import lib.common
    return lib.common.qrcode_generator_wifi(
        trace, app_dict, ssid=ssid, password=password, file_path=file_path, file_name=file_name,
        overwrite=overwrite
    )

def regex_findall(trace: dict, app_dict: dict, search_obj: object, pattern: str) -> dict:
    r"""
    Searches for a regular expression in a given object and returns a list of found expressions.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to search in for the regular expression (converted to a string).
    :param pattern: The regular expression pattern to search for.

    :return: dict
        result: List of expressions found in the input, or None if nothing was found.

    :example:
        string = "Find digits 12345"
        pattern = r"\\d+"
        result = morPy.regex_findall(trace, app_dict, string, pattern)["result"]
    """
    import lib.common
    return lib.common.regex_findall(trace, app_dict, search_obj, pattern)

def regex_find1st(trace: dict, app_dict: dict, search_obj: object, pattern: str) -> dict:
    r"""
    Searches for a regular expression in a given object and returns the first match.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to search in for the regular expression (converted to a string).
    :param pattern: The regular expression pattern to search for.

    :return: dict
        result: The first match found in the input, or None if nothing was found.

    :example:
        string = "Find digits 12345"
        pattern = r"\\d+"
        result = morPy.regex_find1st(trace, app_dict, string, pattern)["result"]
    """
    import lib.common
    return lib.common.regex_find1st(trace, app_dict, search_obj, pattern)

def regex_split(trace: dict, app_dict: dict, search_obj: object, delimiter: str) -> dict:
    r"""
    Splits an object into a list using a given delimiter.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to be split (converted to a string).
    :param delimiter: The character or string used to split `search_obj` into a list.
                      Special characters may require a preceding backslash (e.g., '\\.'
                      to use '.' as a delimiter).

    :return: dict
        result: The list of parts split from the input.

    :example:
        string = "apple.orange.banana"
        split = r"\\."
        result = morPy.regex_split(trace, app_dict, string, split)["result"]
    """
    import lib.common
    return lib.common.regex_split(trace, app_dict, search_obj, delimiter)

def regex_replace(trace: dict, app_dict: dict, search_obj: object, search_for: str, replace_by: str) -> dict:
    r"""
    Substitutes characters or strings in an input object based on a regular expression.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object in which to search and replace (converted to a string).
    :param search_for: The regular expression pattern to search for.
    :param replace_by: The character or string to substitute in place of the matches.

    :return: dict
        result: The modified string with substitutions applied.

    :example:
        string = "apple.orange.banana"
        search_for = r"\\."
        replace_by = r"-"
        result = morPy.regex_replace(trace, app_dict, string, search_for, replace_by)["result"]
    """
    import lib.common
    return lib.common.regex_replace(trace, app_dict, search_obj, search_for, replace_by)

def regex_remove_special(trace: dict, app_dict: dict, inp_string: str, spec_lst: list) -> dict:
    r"""
    Removes or replaces special characters in a given string. The `spec_lst` parameter
    specifies which characters to replace and their replacements. If no replacement is
    specified, a standard list is used to remove special characters without substitution.

    This function can also perform multiple `regex_replace` actions on the same string,
    as any valid regular expression can be used in the `spec_lst`.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param inp_string: The string to be altered.
    :param spec_lst: A list of 2-tuples defining the special characters to replace and
                     their replacements. Example:
                     [(special1, replacement1), ...]. Use `[('', '')]` to invoke the
                     standard replacement list.

    :return: dict
        result: The modified string with special characters replaced or removed.

    :example:
        my_string: str          = "Hello!@#$%^&*()"
        specials_filter: list   = [("@", "AT"), ("!", "")]
        result = morPy.regex_remove_special(trace, app_dict, my_string, specials_filter)
    """
    import lib.common
    return lib.common.regex_remove_special(trace, app_dict, inp_string, spec_lst)

def runtime(in_ref_time):
    r"""
    This function calculates the time delta between now and a reference time.

    :param in_ref_time: Value of the reference time to calculate the actual runtime

    :return: dict
        rnt_delta - Value of the actual runtime.
    """
    import lib.fct
    return lib.fct.runtime(in_ref_time)

def sysinfo():
    r"""
    This function returns information about the hardware and operating system.

    :return: dict
        system - Operating system.
        release - Major version of the operating system.
        version - Major and sub-version of the operating system.
        arch - Architecture of the operating system.
        processor - Processor running the code.
        logical_cpus - Amount of processes, that could run in parallel.
        sys_memory_bytes - Physical system memory in bytes
        username - Returns the username.
        home_dir - Returns the home directory.
        hostname - Returns the host name.
    """
    import lib.fct
    return lib.fct.sysinfo()

def textfile_write(trace: dict, app_dict: dict, filepath: str, content: str) -> None:
    r"""
    Appends content to a text file, creating the file if it does not already exist.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param filepath: Path to the text file, including its name and file extension.
    :param content: The content to be written to the file, converted to a string if necessary.

    :example:
        morPy.textfile_write(trace, app_dict, "path/to/file.txt", "This is some text.")
    """
    import lib.common
    return lib.common.textfile_write(trace, app_dict, filepath, content)

def wait_for_input(trace: dict, app_dict: dict, message: str) -> dict:
    r"""
    Pauses program execution until a user provides input. The input is then
    returned to the calling module. Take note, that the returned user input
    will always be a string.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param message: The text to be displayed as a prompt before user input.

    :return: dict
        usr_input: The input provided by the user.

    :example:
        prompt = "Please enter your name: "
        result = morPy.wait_for_input(trace, app_dict, prompt)["usr_input"]
    """
    import lib.common
    return lib.common.wait_for_input(trace, app_dict, message)

def wait_for_select(trace: dict, app_dict: dict, message: str, collection: tuple=None):
    r"""
    Pauses program execution until a user provides input. The input needs to
    be part of a tuple, otherwise it is repeated or aborted. Take note, that the
    returned user input will always be a string.

    :param trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param message: The text to be displayed as a prompt before user input.
    :param collection: Tuple, that holds all valid user input options. If None,
        evaluation will be skipped.

    :return: dict
        usr_input: The input provided by the user.

    :example:
        msg_text = "Select 1. this or 2. that"
        collection = (1, 2)
        result = morPy.wait_for_select(trace, app_dict, msg_text, collection)["usr_input"]
    """
    import lib.common
    return lib.common.wait_for_select(trace, app_dict, message, collection)
