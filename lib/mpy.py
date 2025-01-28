r"""
Author:     Bastian Neuwirth
Date:       12.08.2023
Version:    0.1
Descr.:     This module is the interface to the morPy framework.
    TODO Finish formatting in morPy standard
"""

import lib.mpy_bulk_ops as mpy_bulk_ops
import lib.mpy_common as mpy_common
import lib.mpy_csv as mpy_csv
import lib.mpy_fct as mpy_fct
import lib.mpy_mp as mpy_mp
import lib.mpy_mt as mpy_mt
import lib.mpy_ui_tk as mpy_ui_tk
# import lib.mpy_wscraper as mpy_wscraper
# TODO fix webscraper
import lib.mpy_xl as mpy_xl
from lib.mpy_decorators import log

import sys

def cl_priority_queue(mpy_trace: dict, app_dict: dict, name: str=None):
    r"""
    This class delivers a priority queue solution. Any task may be enqueued.
    When dequeueing, the highest priority task (lowest number) is dequeued
    first. In case there is more than one, the oldest is dequeued.

    :param mpy_trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param name: Name or description of the instance

    :methods:
        .enqueue(mpy_trace: dict, app_dict: dict, priority: int=100, task: tuple=None, autocorrect: bool=True,
            is_process: bool=True)
            Adds a task to the priority queue.

            :param priority: Integer representing task priority (lower is higher priority)
            :param task: Tuple of a callable, *args and **kwargs (func, *args, **kwargs)
            :param autocorrect: If False, priority can be smaller than zero. Priority
                smaller zero is reserved for the morPy Core.
            :param is_process: If True, task is run in a new process (not by morPy orchestrator)

        .dequeue(mpy_trace: dict, app_dict: dict)
            Removes and returns the highest priority task from the priority queue.

            :return: dict
                priority: Integer representing task priority (lower is higher priority)
                counter: Number of the task when enqueued
                task_id : Continuously incremented task ID (counter).
                task_sys_id : ID of the task determined by Python core
                task: The dequeued task list
                task_callable: The dequeued task callable
                is_process: If True, task is run in a new process (not by morPy orchestrator)

    :example:
        from functools import partial
        # Create queue instance
        queue = mpy.cl_priority_queue(mpy_trace, app_dict, name="example_queue")
        # Add a task to the queue
        queue.enqueue(mpy_trace, app_dict, priority=25, task=partial(task, mpy_trace, app_dict))
        # Fetch a task and run it
        task = queue.dequeue(mpy_trace, app_dict)['task']
        task()
    """

    try:
        return mpy_common.cl_priority_queue(mpy_trace, app_dict, name)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'cl_priority_queue(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def cl_progress(mpy_trace: dict, app_dict: dict, description: str=None, total: float=None, ticks: float=None):
    r"""
    This class instantiates a progress counter. If ticks, total or counter
    are floats, progress of 100 % may not be displayed.

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param description: Describe, what is being processed (i.e. file path or calculation)
    :param total: Mandatory - The total count for completion
    :param ticks: Mandatory - Percentage of total to log the progress. I.e. at ticks=10.7 at every
        10.7% progress exceeded the exact progress will be logged.

    .update(mpy_trace: dict, app_dict: dict, current: float=None)
        Method to update current progress and log progress if tick is passed.

        :return: dict
            prog_rel: Relative progress, float between 0 and 1
            message: Message generated. None, if no tick was hit.

    :example:
        progress = cl_progress(mpy_trace, app_dict, description='App Progress', total=total_count, ticks=10)["prog_rel"]
        progress.update(mpy_trace, app_dict, current=current_count)
    """

    try:
        return mpy_common.cl_progress(mpy_trace, app_dict, description, total, ticks)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'cl_progress(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def cl_progress_gui(mpy_trace: dict, app_dict: dict, frame_title: str = None, frame_width: int = 800,
                 frame_height: int = 0, headline_total: str = None, headline_stage: str = None,
                 headline_font_size: int = 10, description_stage: str=None, description_font_size: int=8,
                 font: str = "Arial", stages: int = 1, max_per_stage: int = 0, console: bool=False,
                 auto_close: bool = False, work=None):
    r"""
    A progress tracking GUI using tkinter to visualize the progress of a background task. The GUI can
    be adjusted with the arguments during construction.

    :param mpy_trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param frame_title: Window frame title as shown in the title bar.
    :param frame_width: Frame width in pixels.
                        Defaults to 800.
    :param frame_height: Frame height in pixels.
                         Defaults to a value depending on which widgets are displayed.
    :param headline_total: Descriptive name for the overall progress.
                           Defaults to morPy localization.
    :param headline_stage: Descriptive name for the actual stage.
                          Defaults to morPy localization.
    :param headline_font_size: Font size for both, overall and stage descriptive names.
                               Defaults to 10.
    :param description_stage: Description or status. Should be written whenever there is a progress update. Will
                             not be shown if None at construction.
                             Defaults to None.
    :param description_font_size: Font size for description/status.
                                  Defaults to 8.
    :param font: Font to be used in the GUI, except for the title bar and console widget.
                 Defaults to "Arial".
    :param stages: Sum of stages until complete. Will not show progress bar for overall progress if equal to 1.
                  Defaults to 1.
    :param max_per_stage: This is the maximum value of the stage progress. Set it to 0 to turn off the stage progress.
                         It represents the maximum value the stage progress will reach until 100%, which is
                         determined by which value you choose to increment the progress with (defaults to 1 per
                         increment). A value of 10 for example amounts to 10% per increment.
                         Defaults to 0.
    :param console: If True, will reroute console output to GUI.
                    Defaults to False.
    :param auto_close: If True, window automatically closes at 100%. If False, user must click "Close".
                       Defaults to False.
    :param work: A callable (e.g. functools.partial()). Will run in a new thread.

    :methods:
        .run(mpy_trace: dict, app_dict: dict)
            Start the GUI main loop.

        .update_progress(mpy_trace: dict, app_dict: dict, current: float = None, max_per_stage: int = None)
            Update stage progress & overall progress. If overall hits 100% and auto_close=True, close window. Else,
            switch button text to "Close" and stop console redirection.

            :param current: Current progress count. If None, each call of this method will add +1
                to the progress count. Defaults to None.
            :param max_per_stage: If the current stage to be finished has got a different amount of increments than the former
                                 stage, this value needs to be set when starting a new stage.

                                 This is the maximum value of the stage progress. Set it to 0 to turn off the stage progress.
                                 It represents the maximum value the stage progress will reach until 100%, which is
                                 determined by which value you choose to increment the progress with (defaults to 1 per
                                 increment). A value of 10 for example amounts to 10% per increment.
                                 Defaults to 0.

        .update_text(mpy_trace: dict, app_dict: dict, headline_total: str = None, headline_stage: str = None,
                    description_stage: str = None)
            Update the headline texts or description at runtime.

            :param headline_total: If not None, sets the overall progress headline text.
            :param headline_stage: If not None, sets the stage progress headline text.
            :param description_stage: If not None, sets the description text beneath the stage headline.

    :example:
        from functools import partial
        import time

        # Define a function or method to be progress tracked. It will be executed in a new thread, because
        # tkinter needs to run in main thread. The argument "gui" will be referenced automatically by the
        # GUI, no explicit assignment is needed.
        def my_func(mpy_trace, app_dict, gui=None):
            outer_loop_count = 2 # Amount stages, i.e. folders to walk
            inner_loop_count = 10 # Increments in the stage, i.e. files modified

            if gui:
                gui.update_text(headline_total=f'My Demo')

            # Loop to demo amount of stages
            for i in range(outer_loop_count):
                # Update Headline for overall progress
                if gui:
                    gui.update_text(headline_stage=f'Stage {i}')
                    gui.update_progress(current=0, max_per_stage=10) # Setup stage progress, "max_per_stage" may be dynamic

                time.sleep(.5) # Wait time, so progress can be viewed (mocking execution time)

                # Loop to demo stage progression
                for j in range(1, inner_loop_count + 1):
                    time.sleep(.2) # Wait time, so progress can be viewed (mocking execution time)

                    # Update progress and text for actual stage
                    if gui:
                        gui.update_text(description_stage=f'This describes progress no. {j} of the stage.')
                        gui.update_progress(mpy_trace, app_dict)

        if name == "__main__":
            # Run function with GUI. For full customization during construction see the
            # cl_progress_gui.__init__() description.

            # In this example the outer and inner loop stop values are set two times manually. However, you may
            # want to set it only a single time and point to these, but that depends on the use case.
            outer_loop_count = 2 # same as the value set in my_func()
            inner_loop_count = 10 # same as the value set in my_func()

            # Define a callable to be progress tracked
            work = partial(my_func, mpy_trace, app_dict)

            # Construct the GUI
            progress = mpy.cl_progress_gui(mpy_trace, app_dict,
                frame_title="My Demo Progress GUI",
                description_stage="Generic Progress stage",
                stages=outer_loop_count,
                max_per_stage=inner_loop_count,
                work=work)

            # Start GUI in main thread and run "work" in separate thread
            progress.run(mpy_trace, app_dict)
    """

    try:
        return mpy_ui_tk.cl_progress_gui(mpy_trace, app_dict, frame_title=frame_title, frame_width=frame_width,
                frame_height=frame_height, headline_total=headline_total, headline_stage=headline_stage,
                headline_font_size=headline_font_size, description_stage=description_stage,
                description_font_size=description_font_size, font=font, stages=stages,
                max_per_stage=max_per_stage, console=console, auto_close=auto_close, work=work,
            )
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'cl_progress_gui(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def cl_xl_workbook(mpy_trace: dict, app_dict: dict, workbook: str, create: bool=False,
              data_only: bool=False, keep_vba: bool=True):
    r"""
    This class constructs an API to an Excel workbook and delivers methods
    to read from and write to the workbook. It uses OpenPyXL and all those
    methods can be used on self.wb_obj if a more versatile API is required.

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param workbook: Path of the workbook
    :param create: If True and file does not yet exist, will create the workbook.
    :param data_only: If True, cells with formulae are represented by their calculated values.
                Closing and reopening the workbook is required for this to change.
    :param keep_vba: If True, preserves any Visual Basic elements in the workbook. Only has an effect
                on workbooks supporting vba (i.e. xlsm-files). These elements remain immutable. Closing
                and reopening the workbook is required to change behaviour.

    :methods:
        .save_workbook(mpy_trace: dict, app_dict: dict, close_workbook: bool=False)

            Saves the changes to the MS Excel workbook.
            :param close_workbook: If True, closes the workbook.

            :return: dict
                wb_obj: Returns None, if the object was closed. Else returns self. Used to delete the
                    reference to an instance.

        .close_workbook(mpy_trace: dict, app_dict: dict)

            Closes the MS Excel workbook.
            :return: dict
                wb_obj: Returns None, if the object was closed. Else returns self. Used to delete the
                    reference to an instance.

        .activate_worksheet(mpy_trace: dict, app_dict: dict, worksheet: str)

            Activates a specified worksheet in the workbook. If the sheet is not found,
            an error is logged.
            :param worksheet: The name of the worksheet to activate.

        .read_cells(self, mpy_trace: dict, app_dict: dict, cell_range: list=None,
                   cell_styles: bool=False, worksheet: str=None)

            Reads the cells of MS Excel workbooks. Overlapping ranges will get auto-formatted
            to ensure every cell is addressed only once.
            :param cell_range: The cell or range of cells to read from. Accepted formats:
                - not case-sensitive
                - Single cell: ["A1"]
                - Range of cells: ["A1:ZZ1000"]
                - Ranges of cells: ["A1:ZZ1000", "c2:fl342"]
            :param cell_styles: If True, cell styles will be retrieved. If False, get value only.
            :param worksheet: Name of the worksheet, where the cell is located. If None, the
                active sheet is addressed.

            :return: dict
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
                wb = mpy.cl_xl_workbook(mpy_trace, app_dict, wb_path)
                cl_dict = wb.read_cells(mpy_trace, app_dict, "Sheet1", ["A1", "B2:C3"])["cl_dict"]
                print(f'{cl_dict}')

        .write_ranges(self, mpy_trace: dict, app_dict: dict, worksheet: str=None, cell_range: list=None,
                     cell_writes: list=None, fill_range: bool=False, style_default: bool=False,
                     save_workbook: bool=True, close_workbook: bool=False)

            Writes data into cells of an Excel workbook.
            :param worksheet: Name of the worksheet, where the cell is located. If None, the
                active sheet is addressed.
            :param cell_range: The cell or range of cells to write. Accepted formats:
                - not case-sensitive
                - Single cell: ["A1"]
                - Range of cells: ["A1:ZZ1000"]
                - Ranges of cells: ["A1:ZZ1000", "c2:fl342"]
            :param cell_writes: WARNING this data structure is not equal to 'cl_dict' of .read_cells()
                List of cell content dictionaries to be written consecutively. If the list is shorter
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
                wb = wb.write_cells(mpy_trace, app_dict, worksheet=w_sh, cell_range=cl_rng, cell_writes=cl_list
                                    save_workbook=True, close_workbook=True)["wb_obj"]

    :example:
        # Construct a workbook instance
        wb_path = "C:\my.xlsx"
        wb = cl_xl_workbook(mpy_trace, app_dict, wb_path)

        # Activate a certain worksheet
        worksheet1 = "Sheet1"
        wb.activate_worksheet(mpy_trace, app_dict, worksheet1)

        # Read cells in range
        range1 = ["A1", "B2:C3"]
        worksheet2 = "Sheet2"
        cl_dict = wb.read_cells(mpy_trace, app_dict, worksheet=worksheet2, cell_range=range1)["cl_dict"]

        # Write to cells in a range and apply styles. Fill range in alternating pattern (fill_range=True).
        cell_writes = []
        cell_writes.append({"value": "Example"})
        cell_writes.append({"value" : r"=1+2", "font" : {"color" : "D1760C",}})
        wb = wb.write_cells(mpy_trace, app_dict, worksheet=worksheet1, cell_range=range1, cell_writes=cell_writes
                            save_workbook=False, close_workbook=False, fill_range=True)["wb_obj"]

        # Save the workbook.
        wb = wb.save_workbook(mpy_trace, app_dict, close=False)["wb_obj"]

        # Close the workbook. Write "None" to the reference "wb".
        wb = wb.close_workbook(mpy_trace, app_dict)["wb_obj"]
    """

    try:
        return mpy_xl.cl_xl_workbook(mpy_trace, app_dict, workbook, create=create,
                                     data_only=data_only, keep_vba=keep_vba)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'cl_xl_workbook(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def csv_read(mpy_trace: dict, app_dict: dict, src_file_path: str=None, delimiter: str=None,
             print_csv_dict: bool=False, log_progress: bool=False, progress_ticks: float=None) -> dict:
    r"""
    This function reads a csv file and returns a dictionary of
    dictionaries. The header row, first row of data and delimiter
    is determined automatically.

    :param mpy_trace: Operation credentials and tracing
    :param app_dict: morPy global dictionary containing app configurations
    :param src_file_path: Path to the csv file.
    :param delimiter: Delimiters used in the csv. None = Auto detection
    :param print_csv_dict: If true, the csv_dict will be printed to console. Should only
        be used for debugging with small example csv files. May take very long to complete.
    :param log_progress: If True, logs the progress.
    :param progress_ticks: Percentage of total to log the progress. I.e. at ticks=10.7 at every
        10.7% progress exceeded the exact progress will be logged. If None or greater 100, will default to 10.

    :return: dict
        mpy_trace: Operation credentials and tracing
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
        src_file_path = 'C:\myfile.csv'
        delimiter = '","'
        csv = mpy_csv.csv_read(mpy_trace, app_dict, src_file_path, delimiter)
        csv_dict = csv["csv_dict"]
        csv_header1 = csv["csv_dict"]["DATA1"]["header"]
        print(f'{csv_header1}')
    """

    try:
        return mpy_csv.csv_read(mpy_trace, app_dict, src_file_path=src_file_path, delimiter=delimiter,
            print_csv_dict=print_csv_dict, log_progress=log_progress, progress_ticks=progress_ticks)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'csv_read(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def csv_dict_to_excel(mpy_trace: dict, app_dict: dict, xl_path: str=None, overwrite: bool=False,
                      worksheet: str=None, close_workbook: bool=False, csv_dict: dict=None,
                      log_progress: bool=False, progress_ticks: float=None) -> dict:
    r"""
    This function takes da dictionary as provided by csv_read() and saves it as an MS Excel file.
    The csv_dict however may be evaluated and processed prior to executing csv_dict_to_excel().
    The file will be saved automatically, but closing the workbook is optional.

    :param mpy_trace: Operation credentials and tracing
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
        10.7% progress exceeded the exact progress will be logged. If None, will default to 10.

    :return: dict
        mpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        wb_obj: Returns None, if the object was closed. Else returns an instance of "mpy_xl.cl_xl_workbook()".
            Used to delete the reference to an instance.

    :example:
        src_file_path = 'C:\my.csv'
        delimiter = '","'
        csv = mpy_csv.csv_read(mpy_trace, app_dict, src_file_path, delimiter)

        # ... process data in csv["csv_dict"] ...

        target_path = 'C:\my.xlsx'
        wb_sht = 'Sheet1'
        wb = csv_dict_to_excel(mpy_trace, app_dict, csv_dict=csv["csv_dict"], xl_path=target_path,
            overwrite=True, worksheet=wb_sht)["wb_obj"]

        # ... modify 'C:\my.xlsx' ...

        # Save and close workbook
        wb.close_workbook(mpy_trac, app_dict, save_workbook=True, close_workbook=True)
    """

    try:
        return mpy_csv.csv_dict_to_excel(mpy_trace, app_dict, xl_path=xl_path, overwrite=overwrite,
            worksheet=worksheet, close_workbook=close_workbook, csv_dict=csv_dict, log_progress=log_progress,
            progress_ticks=progress_ticks)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'csv_dict_to_excel(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def decode_to_plain_text(mpy_trace: dict, app_dict: dict, src_input: str, encoding: str) -> dict:

    r""" This function decodes different types of data and returns
        a plain text to work with in python. The return result behaves
        like using the open(file, 'r') method.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        src_input - Any kind of data to be decoded. Binary expected. Example:
                    src_input = open(src_file, 'rb')
        encoding - String that defines encoding. Leave empty to auto detect. Examples:
                   '' - Empty. Encoding will be determined automatically. May be incorrect.
                   'utf-16-le' - Decode UTF-16 LE to buffered text.
    :return - dictionary
        result - Decoded result. Buffered object that my be used with the readlines() method.
        encoding - String containing the encoding of src_input.
        mpy_trace - [dictionary] operation credentials and tracing
    """

    try:
        return mpy_common.decode_to_plain_text(mpy_trace, app_dict, src_input, encoding)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'decode_to_plain_text(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def dialog_sel_file(mpy_trace: dict, app_dict: dict, init_dir: str=None, ftypes: tuple=None, title: str=None) -> dict:

    r"""
    This function opens a dialog for the user to select a file.

    :param mpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param ftypes: This tuple of 2-tuples specifies, which filetypes will be
        selectable in the dialog box.
    :param title: Title of the open file dialog

    :return: dict
        mpy_trace: [dictionary] operation credentials and tracing
        check: The function ended with no errors and a file was chosen
        file_path: Path of the selected file
        file_selected: True, if file was selected. False, if canceled.

    :example:
        init_dir = "C:\"
        ftypes = (('PDF','*.pdf'),('Textfile','*.txt'),('All Files','*.*'))
        title = 'Select a file...'
        file_path = mpy.dialog_sel_file(mpy_trace, app_dict, init_dir, ftypes, title)["file_path"]
    """

    try:
        return mpy_ui_tk.dialog_sel_file(mpy_trace, app_dict, init_dir, ftypes, title)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'dialog_sel_file(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def dialog_sel_dir(mpy_trace: dict, app_dict: dict, init_dir: str=None, title: str=None) -> dict:

    r"""
    This function opens a dialog for the user to select a directory.

    :param mpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param title: Title of the open directory dialog

    :return: dict
        mpy_trace: [dictionary] operation credentials and tracing
        check: The function ended with no errors and a file was chosen
        dir_path: Path of the selected directory
        dir_selected: True, if directory was selected. False, if canceled.

    :example:
        init_dir = "C:\"
        title = 'Select a directory...'
        dir_path = mpy.dialog_sel_dir(mpy_trace, app_dict, init_dir, title)["dir_path"]
    """

    try:
        return mpy_ui_tk.dialog_sel_dir(mpy_trace, app_dict, init_dir, title)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'dialog_sel_dir(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def fso_copy_file(mpy_trace, app_dict, source, dest, ovwr_perm):

    r""" This function is used to copy a single file from source to destination.
        A file check is already included and will be performed.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        source - Complete path to the source file including the file extension
        dest - Complete path to the destination file including the file extension
        ovwr_perm - If TRUE, the destination file may be overwritten.
    :return - dictionary
        check - The function ended with no errors
        source - Path to the source file as a path object
        dest - Path to the destination file as a path object
        mpy_trace - [dictionary] operation credentials and tracing
    """

    try:
        return mpy_common.fso_copy_file(mpy_trace, app_dict, source, dest, ovwr_perm)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'fso_copy_file(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def fso_create_dir(mpy_trace, app_dict, mk_dir):

    r""" This function creates a directory as well as it's parents
        recursively.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        mk_dir - Path to the directory/tree to be created
    :return - dictionary
        check - The function ended with no errors
        mpy_trace - [dictionary] operation credentials and tracing
    """

    try:
        return mpy_common.fso_create_dir(mpy_trace, app_dict, mk_dir)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'fso_create_dir(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def fso_delete_dir(mpy_trace, app_dict, del_dir):

    r""" This function is used to delete an entire directory including it's
        contents. A directory check is already included and will be performed.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        del_dir - Path to the directory to be deleted
    :return - dictionary
        check - The function ended with no errors
        mpy_trace - [dictionary] operation credentials and tracing
    """

    try:
        return mpy_common.fso_delete_dir(mpy_trace, app_dict, del_dir)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'fso_delete_dir(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def fso_delete_file(mpy_trace, app_dict, del_file):

    r"""
    This function is used to delete a file. A path check is
    already included and will be performed.

    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        del_file - Path to the directory to be deleted

    :return - dictionary
        check - The function ended with no errors
        mpy_trace - [dictionary] operation credentials and tracing
    """

    try:
        return mpy_common.fso_delete_file(mpy_trace, app_dict, del_file)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'fso_delete_file(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def fso_walk(mpy_trace, app_dict, path, depth):

    r""" This function returns the contents of a directory.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        path - Path to be analyzed
        depth - Limits the depth to be analyzed
                -1 - No Limit
                0 - path only
    :return - dictionary
        check - The function ended with no errors
        walk_dict - Dictionary of root directories and it's contents. Example:
                {'root0' : {'root' : root, \
                            'dirs' : [dir list], \
                            'files' : [file list]}
                 'root1' : {'root' : root, \
                            'dirs' : [dir list], \
                            'files' : [file list]}
                 ...
                }
        mpy_trace - [dictionary] operation credentials and tracing
    """

    try:
        return mpy_common.fso_walk(mpy_trace, app_dict, path, depth)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'fso_walk(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def process_q(task: tuple, priority: int=100, autocorrect: bool=True):

    r"""
    This function enqueues a task in the morPy multiprocessing queue. The task is a
    tuple, that demands the positional arguments (func, mpy_trace, app_dict, *args, **kwargs).

    :param task: Tuple of a callable, *args and **kwargs
    :param priority: Integer representing task priority (lower is higher priority)
    :param autocorrect: If False, priority can be smaller than zero. Priority
        smaller zero is reserved for the morPy Core. However, it is a devs choice
        to make.

    :return: process_qed: If True, process was queued successfully. If False, an error occurred.

    :example:
        from mpy import process_q
        message = "Gimme 5"
        def gimme_5(mpy_trace, app_dict, message):
            print(message)
            return message
        a_number = (gimme_5, mpy_trace, app_dict, message) # Tuple of a callable, *args and **kwargs
        enqueued = process_q(task=a_number, priority=20) #
        if not enqueued:
            print("No, thank you sir!")
    """

    process_qed = False
    mpy_trace = None
    app_dict = None

    try:
        mpy_trace = task[1]
        app_dict = task[2]

        try:
            app_dict["proc"]["mpy"]["process_q"].enqueue(
                mpy_trace, app_dict, priority=priority, task=task, autocorrect=autocorrect
            )

            process_qed = True

        except Exception as e:
            # Define operation credentials (see mpy_init.init_cred() for all dict keys)
            module = 'mpy'
            operation = 'process_q(~)'
            mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

            log(mpy_trace, app_dict, "critical",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    except Exception as e:
        if app_dict:
            raise ValueError(f'{app_dict["loc"]["mpy"]["ValueError"]}\n'
                             f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                             f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}'
                             )
        else:
            raise ValueError('A function got an argument of correct type but improper value.\n'
                             f'mpy_trace: {True if mpy_trace else False}\n'
                             f'app_dict: False')

    finally:
        return process_qed

def interrupt(mpy_trace: dict, app_dict: dict) -> dict:

    r"""
    This function sets a global interrupt flag. Processes and threads
    will halt once they pass (the most recurring) morPy functions.

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        mpy_trace: Operation credentials and tracing
        check: Indicates if the task was dequeued successfully

    :example:
        mpy_mp.interrupt(mpy_trace, app_dict)


    TODO finish this function
    """

    try:
        return mpy_mp.interrupt(mpy_trace, app_dict)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'interrupt(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def regex_findall(mpy_trace, app_dict, search_obj, pattern):

    r"""
    Searches for a regular expression in a given object and returns a list of found expressions.

    :param mpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to search in for the regular expression (converted to a string).
    :param pattern: The regular expression pattern to search for.

    :return: dict
        result: List of expressions found in the input, or None if nothing was found.
        mpy_trace: Operation credentials and tracing.

    :example:
        string = "Find digits 12345"
        pattern = r"\\d+"
        result = regex_findall(mpy_trace, app_dict, string, pattern)["result"]
    """

    try:
        return mpy_common.regex_findall(mpy_trace, app_dict, search_obj, pattern)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'regex_findall(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def regex_find1st(mpy_trace, app_dict, search_obj, pattern):

    r"""
    Searches for a regular expression in a given object and returns the first match.

    :param mpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to search in for the regular expression (converted to a string).
    :param pattern: The regular expression pattern to search for.

    :return: dict
        result: The first match found in the input, or None if nothing was found.
        mpy_trace: Operation credentials and tracing.

    :example:
        string = "Find digits 12345"
        pattern = r"\\d+"
        result = regex_find1st(mpy_trace, app_dict, string, pattern)["result"]
    """

    try:
        return mpy_common.regex_find1st(mpy_trace, app_dict, search_obj, pattern)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'regex_find1st(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def regex_split(mpy_trace, app_dict, search_obj, delimiter):

    r"""
    Splits an object into a list using a given delimiter.

    :param mpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object to be split (converted to a string).
    :param delimiter: The character or string used to split `search_obj` into a list.
                      Special characters may require a preceding backslash (e.g., '\\.'
                      to use '.' as a delimiter).

    :return: dict
        result: The list of parts split from the input.
        mpy_trace: Operation credentials and tracing.

    :example:
        string = "apple.orange.banana"
        split = r"\\."
        result = regex_split(mpy_trace, app_dict, string, split)["result"]
    """

    try:
        return mpy_common.regex_split(mpy_trace, app_dict, search_obj, delimiter)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'regex_split(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def regex_replace(mpy_trace, app_dict, search_obj, search_for, replace_by):

    r"""
    Substitutes characters or strings in an input object based on a regular expression.

    :param mpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param search_obj: The object in which to search and replace (converted to a string).
    :param search_for: The regular expression pattern to search for.
    :param replace_by: The character or string to substitute in place of the matches.

    :return: dict
        mpy_trace: Operation credentials and tracing.
        result: The modified string with substitutions applied.

    :example:
        string = "apple.orange.banana"
        search_for = r"\\."
        replace_by = r"-"
        result = regex_replace(mpy_trace, app_dict, string, search_for, replace_by)["result"]
    """

    try:
        return mpy_common.regex_replace(mpy_trace, app_dict, search_obj, search_for, replace_by)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'regex_replace(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def regex_remove_special(mpy_trace, app_dict, inp_string, spec_lst):

    r""" This function removes special characters of a given string and instead inserts
        any character if defined. The spec_lst is a list consiting of tuples
        consisting of special characters and what they are supposed to get exchanged
        with. Using a blank list will invoke a standard list where specials will be
        removed and not replaced by any other character. This function may even be used
        to perform a number of regex_replace actions on the same string, because it
        will replace what ever is given to the tuples-list. Essentially, you can use
        any valid regular expression instead of the special character.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        inp_string - The string to be altered
        spec_lst - List consisting of 2-tuples as a definition of which special character
                   is to be replaced by which [(special1,replacement1),...]. Set the
                   list to [('','')] to invoke the standard replace list.
    :return
        result - The substituted chracter or string
    """

    try:
        return mpy_common.regex_remove_special(mpy_trace, app_dict, inp_string, spec_lst)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'regex_remove_special(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def textfile_write(mpy_trace, app_dict, filepath, content):

    r""" This function appends any textfile and creates it, if there
        is no such file.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        filepath - Path to the textfile including its name and filetype
        content - Something that will be printed as a string.

    :return
        -
    """

    try:
        return mpy_common.textfile_write(mpy_trace, app_dict, filepath, content)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'textfile_write(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def testprint(mpy_trace, input):

    r""" This function prints any value given. It is intended to be used for debugging.
    :param
        mpy_trace - operation credentials and tracing
        input - Something that will be printed as a string.
    :return
        -
    """

    return mpy_common.testprint(mpy_trace, input)

def wait_for_input(mpy_trace, app_dict, msg_text):

    r"""
    Pauses program execution until a user provides input. The input is then
    returned to the calling module. Take note, that the returned user input
    will always be a string.

    :param mpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param msg_text: The text to be displayed as a prompt before user input.

    :return: dict
        usr_input: The input provided by the user.
        mpy_trace: Operation credentials and tracing.

    :example:
        result = wait_for_input(mpy_trace, app_dict, "Please enter your name: ")["usr_input"]
    """

    try:
        return mpy_common.wait_for_input(mpy_trace, app_dict, msg_text)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'wait_for_input(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def wait_for_select(mpy_trace: dict, app_dict: dict, msg_text: str, collection: tuple=None) -> dict:

    r"""
    Pauses program execution until a user provides input. The input needs to
    be part of a tuple, otherwise it is repeated or aborted. Take note, that the
    returned user input will always be a string. Take note, that the
    returned user input will always be a string.

    :param mpy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param msg_text: The text to be displayed as a prompt before user input.
    :param collection: Tuple, that holds all valid user input options. If None,
        evaluation will be skipped.

    :return: dict
        usr_input: The input provided by the user.
        mpy_trace: Operation credentials and tracing.

    :example:
        msg_text = "Select 1. this or 2. that"
        collection = (1, 2)
        result = wait_for_select(mpy_trace, app_dict, msg_text, collection)["usr_input"]
    """

    try:
        return mpy_common.wait_for_select(mpy_trace, app_dict, msg_text, collection)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'wait_for_select(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def datetime_now(mpy_trace):

    r""" This function reads the current date and time and returns formatted
        stamps.
    :param
        mpy_trace - operation credentials and tracing
    :return - dictionary
        datetime_value - Date and time in the format YYYY-MM-DD hh:mm:ss.ms as value
                        (used to determine runtime).
        date - Date DD.MM.YYY as a string.
        datestamp - Datestamp YYYY-MM-DD as a string.
        time - Time hh:mm:ss as a string.
        timestamp - Timestamp hhmmss as a string.
        datetimestamp - Date- and timestamp YYY-MM-DD_hhmmss as a string.
        loggingstamp - Date- and timestamp for logging YYYMMDD_hhmmss as a string.
    """

    return mpy_fct.datetime_now(mpy_trace)

def runtime(mpy_trace, in_ref_time):

    r""" This function calculates the actual runtime and returns it.
    :param
        mpy_trace - operation credentials and tracing
        in_ref_time - Value of the reference time to calculate the actual runtime
    :return - dictionary
        rnt_delta - Value of the actual runtime.
    """

    import mpy_fct

    return mpy_fct.runtime(mpy_trace, in_ref_time)

def sysinfo(mpy_trace):

    r""" This function returns various informations about the hardware and operating system.
    :param
        mpy_trace - operation credentials and tracing
    :return - dictionary
        system - Operating system.
        release - Major version of the operating system.
        version - Major and subversions of the operating system.
        arch - Architecture of the operating system.
        processor - Processor running the code.
        logical_cpus - Amount of processes, that could run in parallel.
        sys_memory_bytes - Physical system memory in bytes
        username - Returns the username.
        homedir - Returns the home directory.
        hostname - Returns the host name.
    """

    import mpy_fct

    return mpy_fct.sysinfo(mpy_trace)

def pathtool(mpy_trace, in_path):
    r"""
    This function takes a string and converts it to a path. Additionally,
    it returns path components and checks.

    :param mpy_trace: operation credentials and tracing
    :param in_path: Path to be converted

    :return: dictionary
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
        file_path = mpy.pathtool(mpy_trace, file_path)["out_path"]
    """

    import mpy_fct

    return mpy_fct.pathtool(mpy_trace, in_path)

def path_join(mpy_trace, path_parts, file_extension):

    r""" This function joins components of a tuple to an OS path.
    :param
        mpy_trace - operation credentials and tracing
        path_parts - Tuple of parts to be joined. Exact order is critical. Examples:
                     ('C:', 'This', 'is', 'my', 'path', '.txt') - C:\This\is\my\path.txt
                     ('T:This_Fol', 'der_Will_Be_Split', 'this_Way') - T:\This_Fol\der_Will_Be_Split\this_Way
                     ('Y:', 'myFile.txt') - Y:\myFile.txt
        file_extension - String of the file extension (i.e. '.txt'). Leave
                         empty if path is a directory (None or '') or if the tuple already includes the
                         file extension.
    :return
        path_obj - OS path object of the joined path parts.
    """

    import mpy_fct

    return mpy_fct.path_join(mpy_trace, path_parts, file_extension)

def perfinfo(mpy_trace):

    r""" This function returns performance metrics.
    :param
        mpy_trace - operation credentials and tracing
    :return - dictionary
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

    import mpy_fct

    return mpy_fct.perfinfo(mpy_trace)

def app_dict_to_string(app_dict):

    r""" This function prints the entire app dictionary in Terminal.
    :param
        app_dict - morPy global dictionary
    :return
        -
    """

    import mpy_fct

    return mpy_fct.app_dict_to_string(app_dict)

def tracing(module, operation, mpy_trace):

    r""" This function formats the trace to any given operation. This function is
        necessary to alter the mpy_trace as a pass down rather than pointing to the
        same mpy_trace passed down by the calling operation. If mpy_trace is to altered
        in any way (i.e. 'log_enable') it needs to be done after calling this function.
        This is why this function is called at the top of any operation.
    :param
        module - Name of the module, the operation is defined in (i.e. 'mpy_common')
        operation - Name of the operation executed (i.e. 'tracing(~)')
        mpy_trace - operation credentials and tracing
    :return
        mpy_trace_passdown - operation credentials and tracing
    """

    import mpy_fct

    return mpy_fct.tracing(module, operation, mpy_trace)

def mpy_thread_queue(mpy_trace, app_dict, name, priority, task):

    r""" This function handles the task queue (instance 'mpy_mt_priority_queue' of cl_mtPriorityQueue)
        of this framework. Its main purpose is to provide an easy handling of multithreaded
        programming in the way, that the developer just needs to fill the queue with tasks
        and tailor the multithreading parameters to the apps needs. However, when being
        bound to single threaded execution the queue will just execute sequentially, while
        prioritizing the tasks.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        name - Name of the task/thread.
        priority - Integer value. Sets the priority of the given task. Lower numbers indicate
                   a higher priority. Negative integers should be avoided.
        task - Statement, function or class/module to be run by the thread. A string
               is expected and will be executed via the exec()-function. The module has
               got to be referenced (if any) in order to work. Example:

                   task = 'app_module1.app_function1([mpy_trace], [app_dict], [...], [log])'
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        return mpy_mt.mpy_thread_queue(mpy_trace, app_dict, name, priority, task)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'mpy_thread_queue(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
            f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def mpy_threads_joinall(mpy_trace, app_dict):

    r""" This function stops execution of the code until all threads have finished their work.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        return mpy_mt.mpy_threads_joinall(mpy_trace, app_dict)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'mpy_threads_joinall(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
            f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def mpy_mt_abort(mpy_trace, app_dict):

    r""" This function aborts all pending tasks. However, the priority queue still exists and new threads
        would eventually pick up the aborted tasks.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        return mpy_mt.mpy_mt_abort(mpy_trace, app_dict)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'mpy_mt_abort(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

# TODO MS Excel API

def tk_progbar_indeterminate(mpy_trace, app_dict, GUI_dict):

    r""" This function invokes a window with an indeterminate progress bar
        and status messages.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - The mpy-specific global dictionary
        GUI_dict - Dictionary holding all needed parameters:

            GUI_dict = {'frame_title' : 'TITLE' , \
                        'frame_width' : 450 , \
                        'frame_height' : 300 , \
                        'headline_txt' : 'HEADLINE' , \
                        'headline_font_size' : 35 , \
                        'status_font_size' : 25
                        }
    # TODO finish progressbar

    :return - dictionary
        check - The function ended with no errors and a file was chosen
    """

    try:
        return mpy_ui_tk.tk_progbar_indeterminate(mpy_trace, app_dict, GUI_dict)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'tk_progbar_indeterminate(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

def find_replace_saveas(mpy_trace, app_dict, search_obj, replace_tpl, save_as, overwrite):

    r""" This function finds and replaces strings in a readable object
        line by line. This may be text or csv files, but even strings
        would be converted so they are read line by line. This function
        does not repeat, but it's easy to iterate it. Once every line
        was evaluated and regular expressions got replaced, a file
        will be saved including all changes.
    :param
        mpy_trace - operation credentials and tracing
        app_dict - morPy global dictionary
        search_obj - Any given object to search in for regular
                     expressions.
        replace_tpl - Tuple of tuples. Includes every tuple of regular
                      expressions and what they are supposed to be
                      replaced by. Example:
                    ((replace 1, by 1), (replace 2, by 2), ...)
        save_as - Complete path of the file to be saved.
        overwrite - True, if new files shall overwrite existing ones,
                    if there are any. False otherwise.
    :return - dictionary
        check - The function ended with no errors
    """

    try:
        return mpy_bulk_ops.find_replace_saveas(mpy_trace, app_dict, search_obj, replace_tpl, save_as, overwrite)
    except Exception as e:
        # Define operation credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy'
        operation = 'find_replace_saveas(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        log(mpy_trace, app_dict, "critical",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')