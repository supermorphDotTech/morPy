r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module provides UI-building functions using the Tkinter.
"""

import lib.fct as morpy_fct
import lib.common as common
from lib.decorators import metrics, log

import sys
import threading, queue
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import TclError
from PIL import Image, ImageTk

class GridChoiceTk:
    """
    A tkinter GUI displaying a dynamic grid of image tiles. Each tile shows an image
    with a text label below it. Clicking a tile returns its associated value.

    :param morpy_trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param tile_data: Dictionary containing configuration for each tile.
        The expected structure is:
        {
            "tile_name" : {
                "row_column" : (row, column),         # grid placement
                "img_path" : "path/to/image.png",     # image file path
                "text" : "Descriptive text",          # label under the image
                "return_value" : some_value,          # value returned when clicked
                "tile_size" : (width, height),        # (optional) size for the image tile
            },
            ...
        }
    :param title: Title of the tkinter window.
    :param default_tile_size: Default (width, height) if a tile does not specify its own size.

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether initialization completed without errors

    :example:
        import lib.morPy

        tile_data = {
            "start" : {
                "row_column" : (row, column),
                "img_path" : "path/to/image.png",
                "text" : "Start the App",
                "return_value" : 1,
            },
            ...
        }
        gui = morPy.GridChoiceTk(morpy_trace, app_dict, tile_data,
            title="Start Menu",
            default_tile_size=(128, 128),
        )
        result = gui.run(morpy_trace, app_dict)["choice"]
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, tile_data: dict, title: str=None,
                 default_tile_size: tuple=None):
        r"""
        Initializes the GUI for grid of image tiles.

        In order to get metrics for __init__(), call helper method _init()
        for the @metrics decorator to work. It relies on the returned
        {'morpy_trace' : morpy_trace}, which __init__() can not do (needs to be None).

        :param: See ._init() for details

        :return: self
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk.__init__(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        try:
            self._init(morpy_trace, app_dict, tile_data, title=title, default_tile_size=default_tile_size)

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

    @metrics
    def _init(self, morpy_trace: dict, app_dict: dict, tile_data: dict, title: str=None,
              default_tile_size: tuple=(256, 256)):
        """
        Initialize GUI with support for metrics collection.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param tile_data: Dictionary containing configuration for each tile.
            The expected structure is:
            {
                "tile_name" : {
                    "row_column" : (row, column),         # grid placement
                    "img_path" : "path/to/image.png",     # image file path
                    "text" : "Descriptive text",          # label under the image
                    "return_value" : some_value,          # value returned when clicked
                    "tile_size" : (width, height),        # (optional) size for the image tile
                },
                ...
            }
        :param title: Title of the tkinter window. Defaults to morPy localization.
        :param default_tile_size: Default (width, height) if a tile does not specify its own size.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            import lib.morPy

            tile_data = {
                "start" : {
                    "row_column" : (row, column),
                    "img_path" : "path/to/image.png",
                    "text" : "Start the App",
                    "return_value" : 1,
                },
                ...
            }
            gui = morPy.GridChoiceTk(morpy_trace, app_dict, tile_data,
                title="Start Menu",
                default_tile_size=(128, 128),
            )
            result = gui.run()
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk.__init__(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:
            self.tile_data = tile_data
            self.title = title if title else app_dict["loc"]["morpy"]["GridChoiceTk_title"]
            self.default_tile_size = default_tile_size
            self.choice = None
            self.frame_width = 0
            self.frame_height = 0

            # Create the main tkinter window.
            self.root = tk.Tk()
            self.root.iconbitmap(app_dict["conf"]["app_icon"])
            self.root.title(self.title)

            # A dictionary to keep references to PhotoImage objects. Prevents garbage collection of images.
            self._photos = {}

            self._setup_ui(morpy_trace, app_dict)

            # Calculate coordinates for the window to be centered.
            x = (app_dict["sys"]["resolution_width"] // 2) - (self.frame_width // 2)
            y = (app_dict["sys"]["resolution_height"] * 2 // 5) - (self.frame_height // 2)
            self.root.geometry(f'{self.frame_width}x{self.frame_height}+{x}+{y}')

            # Bind the _on_close() method to closing the window
            self.root.protocol("WM_DELETE_WINDOW", lambda: self._on_close(morpy_trace, app_dict))

            # Fix the frame size, since it's contents do not resize.
            self.root.resizable(False, False)

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        finally:
            return {
                "morpy_trace" : morpy_trace,
                "check" : check,
            }

    def _setup_ui(self, morpy_trace: dict, app_dict: dict):
        """
        Constructs the grid layout with the provided tile data.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk._setup_ui(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:
            container = tk.Frame(self.root)
            container.pack(padx=20, pady=20)

            for tile_name, config in self.tile_data.items():
                row, column = config.get("row_column", (0, 0))
                img_path = morpy_fct.pathtool(config.get("img_path"))["out_path"]
                text = config.get("text", "")
                return_value = config.get("return_value")
                tile_size = config.get("tile_size", self.default_tile_size)

                # Create a frame for this tile.
                tile_frame = tk.Frame(container)
                tile_frame.grid(row=row, column=column, padx=10, pady=10)

                # Determine the appropriate resampling filter.
                if hasattr(Image, "Resampling"):
                    resample_filter = Image.Resampling.LANCZOS
                else:
                    resample_filter = Image.ANTIALIAS

                # Load and resize the image.
                try:
                    img = Image.open(img_path)
                except Exception as e:
                    # Failed to load image.
                    raise RuntimeError(
                        f'{app_dict["loc"]["morpy"]["GridChoiceTk_img_fail"]}\n'
                        f'{app_dict["loc"]["morpy"]["GridChoiceTk_path"]}: {img_path}\n'
                        f'{app_dict["loc"]["morpy"]["GridChoiceTk_tile"]}: {tile_name}'
                    )

                img = img.resize(tile_size, resample_filter)
                photo = ImageTk.PhotoImage(img)
                self._photos[tile_name] = photo  # Save a reference to avoid garbage collection.

                # Create a button with the image.
                btn = tk.Button(tile_frame, image=photo,
                    command=lambda val=return_value: self._on_select(morpy_trace, app_dict, val)
                )
                btn.pack()

                # Create a label below the image.
                lbl = tk.Label(tile_frame, text=text)
                lbl.pack(pady=(5, 0))

                # Get frame width and height
                self.root.update_idletasks()  # Process pending geometry updates
                self.frame_width = self.root.winfo_width()
                self.frame_height = self.root.winfo_height()

                check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        finally:
            return {
                "morpy_trace" : morpy_trace,
                "check" : check,
            }

    def _on_select(self, morpy_trace: dict, app_dict: dict, value):
        """
        Callback when a tile is clicked. Sets the selected value and quits the mainloop.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param value: Selected value relating to the clicked tile.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk._on_select(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:
            self.choice = value
            self.root.quit()

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        finally:
            return {
                "morpy_trace" : morpy_trace,
                "check" : check,
            }

    @metrics
    def _on_close(self, morpy_trace: dict, app_dict: dict):
        r"""
        Close or abort the GUI.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._on_close(morpy_trace, app_dict)
        """

        module = 'ui_tk'
        operation = 'GridChoiceTk._on_close(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:
            self.root.quit()

            # Initiate program exit
            app_dict["global"]["morpy"]["exit"] = True

            # Release the global interrupts
            app_dict["global"]["morpy"]["interrupt"] = False

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    def run(self, morpy_trace: dict, app_dict: dict):
        """
        Launches the GUI and waits for the user to make a selection.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
            choice: The value associated with the selected tile.

        :example:
            import lib.morPy

            tile_data = {
                "start" : {
                    "row_column" : (row, column),
                    "img_path" : "path/to/image.png",
                    "text" : "Start the App",
                    "return_value" : 1,
                },
                ...
            }
            gui = morPy.GridChoiceTk(morpy_trace, app_dict, tile_data,
                title="Start Menu",
                default_tile_size=(128, 128),
            )
            result = gui.run(morpy_trace, app_dict)["choice"]
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk.run(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:
            self.root.mainloop()
            self.root.destroy()

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        finally:
            return {
                "morpy_trace" : morpy_trace,
                "check" : check,
                "choice" : self.choice
            }

class ProgressTrackerTk:
    r"""
    A progress tracking GUI using tkinter to visualize the progress of a background task. The GUI can
    be adjusted with the arguments during construction.

    :param morpy_trace: Operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations
    :param frame_title: Window frame title as shown in the title bar.
    :param frame_width: Frame width in pixels.
                        Defaults to 1080.
    :param frame_height: Frame height in pixels.
                         Defaults to a value depending on which widgets are displayed.
    :param headline_total: Descriptive name for the overall progress.
                           Defaults to morPy localization.
    :param headline_stage: Descriptive name for the actual stage.
                          Defaults to morPy localization.
    :param headline_font_size: Font size for both, overall and stage descriptive names.
                               Defaults to 10.
    :param description_stage: Description or status. Will
                             not be shown if None at construction.
                             Defaults to None.
    :param description_font_size: Font size for description/status.
                                  Defaults to 10.
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
        .run(morpy_trace: dict, app_dict: dict)
            Start the GUI main loop.

        .update_progress(morpy_trace: dict, app_dict: dict, current: float = None, max_per_stage: int = None)
            Update stage progress & overall progress. If overall hits 100% and auto_close=True, close window. Else,
            switch button text to "Close" and stop console redirection. Enqueues a UI request for the
            main thread to process. Safe to call from any thread.

            :param current: Current progress count. If None, each call of this method will add +1
                to the progress count. Defaults to None.
            :param max_per_stage: If the current stage to be finished has got a different amount of increments than the former
                                 stage, this value needs to be set when starting a new stage.

                                 This is the maximum value of the stage progress. Set it to 0 to turn off the stage progress.
                                 It represents the maximum value the stage progress will reach until 100%, which is
                                 determined by which value you choose to increment the progress with (defaults to 1 per
                                 increment). A value of 10 for example amounts to 10% per increment.
                                 Defaults to 0.

        .update_text(morpy_trace: dict, app_dict: dict, headline_total: str = None, headline_stage: str = None,
                    description_stage: str = None)
            Update the headline texts or description at runtime. Enqueues a UI request for the
            main thread to process. Safe to call from any thread.

            :param headline_total: If not None, sets the overall progress headline text.
            :param headline_stage: If not None, sets the stage progress headline text.
            :param description_stage: If not None, sets the description text beneath the stage headline.

    :example:
        from functools import partial
        import time

        # Define a function or method to be progress tracked. It will be executed in a new thread, because
        # tkinter needs to run in main thread. The argument "gui" will be referenced automatically by the
        # GUI, no explicit assignment is needed.
        def my_func(morpy_trace, app_dict, gui=None):
            outer_loop_count = 2 # Amount stages, i.e. folders to walk
            inner_loop_count = 10 # Increments in the stage, i.e. files modified

            if gui:
                gui.update_text(morpy_trace, app_dict, headline_total=f'My Demo')

            # Loop to demo amount of stages
            for i in range(outer_loop_count):
                # Update Headline for overall progress
                if gui:
                    gui.update_text(morpy_trace, app_dict, headline_stage=f'Stage {i}')
                    gui.update_progress(morpy_trace, app_dict, current=0, max_per_stage=10) # Setup stage progress, "max_per_stage" may be dynamic

                time.sleep(.5) # Wait time, so progress can be viewed (mocking execution time)

                # Loop to demo stage progression
                for j in range(1, inner_loop_count + 1):
                    time.sleep(.2) # Wait time, so progress can be viewed (mocking execution time)

                    # Update progress and text for actual stage
                    if gui:
                        gui.update_text(morpy_trace, app_dict, description_stage=f'This describes progress no. {j} of the stage.')
                        gui.update_progress(morpy_trace, app_dict)

        if name == "__main__":
            # Run function with GUI. For full customization during construction see the
            # ProgressTrackerTk.__init__() description.

            # In this example the outer and inner loop stop values are set two times manually. However, you may
            # want to set it only a single time and point to these, but that depends on the use case.
            outer_loop_count = 2 # same as the value set in my_func()
            inner_loop_count = 10 # same as the value set in my_func()

            # Define a callable to be progress tracked
            work = partial(my_func, morpy_trace, app_dict)

            # Construct the GUI
            progress = morPy.ProgressTrackerTk(morpy_trace, app_dict,
                frame_title="My Demo Progress GUI",
                description_stage="Generic Progress stage",
                stages=outer_loop_count,
                max_per_stage=inner_loop_count,
                work=work)

            # Start GUI in main thread and run "work" in separate thread
            progress.run(morpy_trace, app_dict)
    """

    def __init__(self, morpy_trace: dict, app_dict: dict, frame_title: str = None, frame_width: int = 1080,
                 frame_height: int = 0, headline_total: str = None, headline_stage: str = None,
                 headline_font_size: int = 10, description_stage: str=None, description_font_size: int=8,
                 font: str = "Arial", stages: int = 1, max_per_stage: int = 0, console: bool=False,
                 auto_close: bool = False, work=None):
        r"""
        Initializes the GUI with progress tracking.

        In order to get metrics for __init__(), call helper method _init()
        for the @metrics decorator to work. It relies on the returned
        {'morpy_trace' : morpy_trace}, which __init__() can not do (needs to be None).

        :param: See ._init() for details

        :return: self
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk.__init__(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        try:
            self._init(morpy_trace, app_dict, frame_title=frame_title, frame_width=frame_width, frame_height=frame_height,
                headline_total=headline_total, headline_stage=headline_stage, headline_font_size=headline_font_size,
                description_stage=description_stage, description_font_size=description_font_size, font=font, stages=stages,
                max_per_stage=max_per_stage, console=console, auto_close=auto_close, work=work,
            )

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

    @metrics
    def _init(self, morpy_trace: dict, app_dict: dict, frame_title: str = None, frame_width: int = 800,
              frame_height: int = 0, headline_total: str = None, headline_stage: str = None,
              headline_font_size: int = 10, description_stage: str=None, description_font_size: int=8,
              font: str = "Arial", stages: int = 1, max_per_stage: int = 0, console: bool=False,
              auto_close: bool = False, work=None):
        r"""
        Initializes the GUI with progress tracking.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param frame_title: Window frame title as shown in the title bar.
        :param frame_width: Frame width in pixels.
                            Defaults to 1080.
        :param frame_height: Frame height in pixels.
                             Defaults to a value depending on which widgets are displayed.
        :param headline_total: Descriptive name for the overall progress.
                               Defaults to morPy localization.
        :param headline_stage: Descriptive name for the actual stage.
                              Defaults to morPy localization.
        :param headline_font_size: Font size for both, overall and stage descriptive names.
                                   Defaults to 10.
        :param description_stage: Description or status. Will
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

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            progress = morPy.ProgressTrackerTk(morpy_trace: dict, app_dict,
                frame_title="My Demo Progress GUI",
                description_stage="Generic Progress stage",
                stages=outer_loop_count,
                max_per_stage=inner_loop_count,
                work=work)
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk._init(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False
        frame_height_sizing = False
        height_factor_headlines = 0
        height_factor_description = 0

        try:
            self.console_on = console
            self.auto_close = auto_close
            self.done = False  # Will be True once overall progress is 100%
            self.main_loop_interval = 50 # ms, how often we do the main loop

            # Default texts
            self.frame_title = (app_dict["loc"]["morpy"]["ProgressTrackerTk_prog"]
                                if not frame_title else frame_title)
            self.frame_width = frame_width
            self.frame_height = frame_height
            self.headline_total_nocol = (f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_overall"]}'
                             if not headline_total else f'{headline_total}')
            self.headline_stage_nocol = (f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_curr"]}'
                             if not headline_stage else f'{headline_stage}')
            self.description_stage = description_stage
            self.headline_font_size = headline_font_size
            self.description_font_size = description_font_size
            self.font = font
            self.button_text_abort = f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_abort"]}'
            self.button_text_close = f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_close"]}'

            self.ui_calls = queue.Queue()  # Queue for collecting UI update requests from background thread

            # Progress tracking
            self.stages = stages
            self.max_per_stage = max_per_stage

            self.stages_finished = 0
            self.overall_progress_abs = 0

            # Calculate factors for frame height
            if self.frame_height == 0:
                frame_height_sizing = True
                height_factor_headlines = round(50 * self.headline_font_size / 10)
                height_factor_description = round(50 * self.description_font_size / 10)

            if self.stages > 1:
                self.overall_progress_on = True

                # Set fraction of overall progress per stage
                self.fraction_per_stage  = 100.0 / self.stages

                # Add height for overall progress bar
                if frame_height_sizing:
                    self.frame_height += height_factor_headlines

                # Construct the overall progress tracker
                self.overall_progress_tracker = common.ProgressTracker(
                    morpy_trace, app_dict, description=self.headline_total_nocol, total=self.stages, ticks=.01,
                    verbose=True
                )

                # Finalize overall headline
                self.headline_total = f'{self.headline_total_nocol}:'
            else:
                self.overall_progress_on = False

            if self.max_per_stage > 0:
                self.stage_progress_on = True

                # Add height for stage progress bar
                if frame_height_sizing:
                    self.frame_height += height_factor_headlines

                # Construct the stage progress tracker
                self.stage_progress_tracker = common.ProgressTracker(
                    morpy_trace, app_dict, description=self.headline_stage_nocol, total=self.max_per_stage, ticks=.01,
                    verbose=True
                )

                # Finalize stage headline
                self.headline_stage = f'{self.headline_stage_nocol}:'
            else:
                self.stage_progress_on = False

            if self.description_stage:
                self.description_stage_on = True
                # Add height for description of latest update
                if frame_height_sizing:
                    self.frame_height += height_factor_description
            else:
                self.description_stage_on = False

            # For capturing prints
            self.console_queue = None  # Always define, even if console_on=False
            if self.console_on:
                self.console_queue = queue.Queue()

                # Add height for overall progress bar
                if frame_height_sizing:
                    self.frame_height += 375

            # Calculate coordinates for the window to be centered.
            x = (app_dict["sys"]["resolution_width"] // 2) - (self.frame_width // 2)
            y = (app_dict["sys"]["resolution_height"] * 2 // 5) - (self.frame_height // 2)

            # Tk window
            self.root = tk.Tk()
            self.root.iconbitmap(app_dict["conf"]["app_icon"])
            self.root.title(self.frame_title)
            self.root.geometry(f'{self.frame_width}x{self.frame_height}+{x}+{y}')

            # Bind the _on_close() method to closing the window
            self.root.protocol("WM_DELETE_WINDOW", lambda: self._on_close(morpy_trace, app_dict))

            self._create_widgets(morpy_trace, app_dict)

            if self.console_on:
                self._redirect_console(morpy_trace, app_dict)

            # The background work to run (if any)
            self.work_callable = work
            if self.work_callable is not None:
                self._start_work_thread(morpy_trace, app_dict)

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        finally:
            return {
                "morpy_trace" : morpy_trace,
                "check" : check,
            }

    @metrics
    def _create_widgets(self, morpy_trace: dict, app_dict: dict):
        r"""
        Build and place all widgets in a grid layout.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._create_widgets(morpy_trace, app_dict)
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk._create_widgets(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False
        self.overall_progress_text = None
        self.stage_progress_text = None

        try:
            # Check, if running in main thread (if you have that function)
            check_main_thread(app_dict)

            # Grid config - columns
            self.root.columnconfigure(0, weight=1)
            self.root.columnconfigure(1, weight=0)
            self.root.columnconfigure(2, weight=0)

            # Overall Progress
            if self.overall_progress_on:
                # Grid config
                self.root.rowconfigure(0, weight=0)

                # Overall headline (ttk.Label)
                self.total_headline_label = ttk.Label(
                    self.root,
                    text=self.headline_total,
                    font=(self.font, self.headline_font_size)
                )
                self.total_headline_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")

                # Overall percentage (ttk.Label)
                self.overall_label_var = tk.StringVar(value="0.00%")
                self.overall_label = ttk.Label(self.root, textvariable=self.overall_label_var)
                self.overall_label.grid(row=0, column=1, padx=0, pady=(10, 0), sticky="nsw")

                # Overall progress bar (ttk.Progressbar)
                self.overall_progress = ttk.Progressbar(
                    self.root,
                    orient=tk.HORIZONTAL,
                    length=int(self.frame_width * 0.6),
                    mode="determinate"
                )
                self.overall_progress.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="nsew")
            else:
                self.total_headline_label = None
                self.overall_progress = None
                self.overall_label_var = None
                self.overall_label = None

            # Stage Progress
            if self.stage_progress_on:
                self.root.rowconfigure(1, weight=0)

                # Stage headline (ttk.Label)
                self.stage_headline_label = ttk.Label(
                    self.root,
                    text=self.headline_stage,
                    font=(self.font, self.headline_font_size)
                )
                self.stage_headline_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsw")

                # Stage percentage (ttk.Label)
                self.stage_label_var = tk.StringVar(value="0.00%")
                self.stage_label = ttk.Label(self.root, textvariable=self.stage_label_var)
                self.stage_label.grid(row=1, column=1, padx=0, pady=(10, 0), sticky="nsew")

                # Stage progress bar (ttk.Progressbar)
                self.stage_progress = ttk.Progressbar(
                    self.root,
                    orient=tk.HORIZONTAL,
                    length=int(self.frame_width * 0.6),
                    mode="determinate"
                )
                self.stage_progress.grid(row=1, column=2, padx=10, pady=(10, 0), sticky="nsew")
            else:
                self.stage_headline_label = None
                self.stage_progress = None
                self.stage_label_var = None
                self.stage_label = None

            # Detail description at progress update
            if self.description_stage_on:
                self.root.rowconfigure(2, weight=0)
                # Still a ttk.Label
                self.stage_description_label = ttk.Label(
                    self.root,
                    text=self.description_stage,
                    font=(self.font, self.description_font_size)
                )
                self.stage_description_label.grid(row=2, column=0, columnspan=3, padx=10, pady=(5, 5), sticky="nsw")

            # Console widget (tk.Text has no direct TTK equivalent)
            if self.console_on:
                self.root.rowconfigure(3, weight=1)
                self.console_output = tk.Text(self.root, height=10, wrap="word")
                self.console_output.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
                self.console_output.configure(bg="black", fg="white")

                # Create a vertical Scrollbar
                self.console_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.console_output.yview)
                self.console_scrollbar.grid(row=3, column=3, sticky="ns", padx=(0, 10), pady=5)
                self.console_output["yscrollcommand"] = self.console_scrollbar.set
            else:
                self.console_output = None

            # Grid config - Bottom row
            self.root.rowconfigure(4, weight=0)

            # Close/Abort button (ttk.Button)
            self.button_text = tk.StringVar(value=self.button_text_abort)
            self.close_button = ttk.Button(
                self.root,
                textvariable=self.button_text,
                command=lambda: self._on_close(morpy_trace, app_dict)
            )
            self.close_button.grid(row=4, column=2, columnspan=1, padx=10, pady=(0, 10), sticky="nse")

            # Enforce an update on the GUI
            self._enforce_update()

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    def _enforce_update(self):
        r"""
        Enforce an update of the GUI. If not leveraged after GUI update, might not display.

        :example:
            # Enforce an update on the GUI
            self._enforce_update()
        """

        self.root.update_idletasks()
        self.root.update()

    @metrics
    def _redirect_console(self, morpy_trace: dict, app_dict: dict):
        r"""
        Redirect sys.stdout/sys.stderr to self.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._redirect_console(morpy_trace, app_dict)
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk._redirect_console(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:
            sys.stdout = self
            sys.stderr = self

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        return {
            "morpy_trace": morpy_trace,
            "check": check,
        }

    def write(self, message: str):
        r"""
        Captured print statements go into a queue.

        :param message: Message to be printed to console

        TODO fix writes to console. Somehow not arriving at GUI.
        """

        if self.console_queue is not None:
            self.console_queue.put(message)

    def flush(self):
        r"""
        Required for stdout redirection.
        """
        pass

    @metrics
    def _stop_console_redirection(self, morpy_trace: dict, app_dict: dict):
        r"""
        Stop capturing print statements in the GUI console.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._stop_console_redirection(morpy_trace, app_dict)
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk._stop_console_redirection(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
                lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                        f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                        f'{type(e).__name__}: {e}')

        return {
            "morpy_trace": morpy_trace,
            "check": check,
        }

    @metrics
    def _main_loop(self, morpy_trace, app_dict):
        r"""
        Main repeating loop for GUI refreshes. Read console queue to update text widget (unless we are done &
        auto_close=False). Update the progress bars (unless done), then schedule itself again.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._main_loop(morpy_trace, app_dict)
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk._main_loop(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:
            # Process console output if needed
            if self.console_on and not self.done:
                self._update_console(morpy_trace, app_dict)

            # Process any pending UI updates from the background thread
            while not self.ui_calls.empty():
                call_type, kwargs = self.ui_calls.get_nowait()

                if call_type == "update_text":
                    self._real_update_text(morpy_trace, app_dict, **kwargs)
                elif call_type == "update_progress":
                    self._real_update_progress(morpy_trace, app_dict, **kwargs)

            # Schedule next loop
            self.root.after(self.main_loop_interval, lambda: self._main_loop(morpy_trace, app_dict))

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
                lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                        f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                        f'{type(e).__name__}: {e}')

        return {
            "morpy_trace": morpy_trace,
            "check": check,
        }

    @metrics
    def _update_console(self, morpy_trace: dict, app_dict: dict):
        r"""
        One-time call to read from the queue and add text to the widget.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._update_console(morpy_trace, app_dict)
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk._update_console(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:
            # Check, if running in main thread
            check_main_thread(app_dict)

            while not self.console_queue.empty():
                msg = self.console_queue.get_nowait()
                if self.console_output is not None:
                    self.console_output.insert(tk.END, msg)
                    self.console_output.see(tk.END)

                # Enforce an update on the GUI
                self._enforce_update()

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    @metrics
    def update_progress(self, morpy_trace: dict, app_dict: dict, current: float = None, max_per_stage: int = None):
        r"""
        Update stage progress & overall progress. If overall hits 100% and auto_close=True, close window. Else,
        switch button text to "Close" and stop console redirection. Enqueues a UI request for the
        main thread to process. Safe to call from any thread.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param current: Current progress count. If None, each call of this method will add +1
            to the progress count. Defaults to None.
        :param max_per_stage: If the current stage to be finished has got a different amount of increments than the former
                             stage, this value needs to be set when starting a new stage.

                             This is the maximum value of the stage progress. Set it to 0 to turn off the stage progress.
                             It represents the maximum value the stage progress will reach until 100%, which is
                             determined by which value you choose to increment the progress with (defaults to 1 per
                             increment). A value of 10 for example amounts to 10% per increment.
                             Defaults to 0.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            progress = morPy.ProgressTrackerTk(morpy_trace: dict, app_dict,
                frame_title="My Demo Progress GUI",
                description_stage="Starting stage 1",
                stages=2,
                max_per_stage=10,
                work=work)

            progress.run(morpy_trace, app_dict)

            curr_cnt = 5.67
            msg = f'Currently at {curr_cnt}'
            progress.update_progress(morpy_trace, app_dict, current=curr_cnt, description_stage=msg)

            # stage 1 is at 100%
            curr_cnt = 10
            msg = f'Currently at {curr_cnt}'
            progress.update_progress(morpy_trace, app_dict, current=curr_cnt, description_stage=msg)

            # Setup stage 2
            progress.update_text(morpy_trace, app_dict,
                headline_stage="Starting stage 2",
                description_stage="Now copying data...",
            )
            progress.update_progress(morpy_trace, app_dict, current=0, max_per_stage=15)

            # stage 2 is at 100%
            curr_cnt = 15
            msg = f'Currently at {curr_cnt}'
            progress.update_progress(morpy_trace, app_dict, current=curr_cnt, description_stage=msg)
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk.update_progress(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:
            call_kwargs = {
                "current" : current,
                "max_per_stage" : max_per_stage,
            }
            self.ui_calls.put(("update_progress", call_kwargs))

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    def _real_update_progress(self, morpy_trace: dict, app_dict: dict, current: float = None,
                              max_per_stage: int = None):
        """
        Update stage progress & overall progress. If overall hits 100% and auto_close=True, close window. Else,
        switch button text to "Close" and stop console redirection. Enqueues a UI request for the
        main thread to process. Safe to call from any thread. Actually updates Tk widgets. Must be called only
        from the main thread.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param current: Current progress count. If None, each call of this method will add +1
            to the progress count. Defaults to None.
        :param max_per_stage: If the current stage to be finished has got a different amount of increments than the former
                             stage, this value needs to be set when starting a new stage.

                             This is the maximum value of the stage progress. Set it to 0 to turn off the stage progress.
                             It represents the maximum value the stage progress will reach until 100%, which is
                             determined by which value you choose to increment the progress with (defaults to 1 per
                             increment). A value of 10 for example amounts to 10% per increment.
                             Defaults to 0.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk._real_update_progress(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False
        stage_abs = None
        overall_progress = None
        reset_stage_progress = False

        try:
            # Avoid updates after "abort"
            if not self.done:
                # Check, if running in main thread
                check_main_thread(app_dict)

                if max_per_stage and max_per_stage != self.max_per_stage:
                    self.max_per_stage = max_per_stage

                # If we're already done, just clamp visually
                if self.done:
                    if self.overall_progress_on and self.overall_progress is not None:
                        self.overall_progress["value"] = 100.0
                        self.overall_label_var.set("100.00%")

                        # Enforce an update on the GUI
                        self._enforce_update()
                else:
                    # 1) stage progress
                    if self.stage_progress_on:
                        stage_info = self.stage_progress_tracker.update(morpy_trace, app_dict, current=current)
                        stage_abs = stage_info["prog_abs"]  # 0..100.0%

                        if self.stage_progress is not None and stage_abs:
                            self.stage_progress["value"] = stage_abs
                        if self.stage_label_var is not None and stage_abs:
                            self.stage_label_var.set(f"{stage_abs:.2f}%")

                        # If stage hits 100%, increment the stage count, reset stage bar
                        if stage_abs and stage_abs >= 100.0:
                            if self.overall_progress_on:
                                reset_stage_progress = True
                                self.stages_finished += 1
                            else:
                                self.stages_finished += 1
                                # If all stages are finished, mark as done
                                self.done = True
                                if self.auto_close:
                                    self._stop_console_redirection(morpy_trace, app_dict)
                                    self._on_close(morpy_trace, app_dict)
                                else:
                                    self.button_text.set(self.button_text_close)
                                    self._enforce_update()
                                    self._stop_console_redirection(morpy_trace, app_dict)

                        # Decrement self.unfinished_tasks
                        self.ui_calls.task_done()

                        # Enforce an update on the GUI
                        self._enforce_update()

                    # 2) Overall fraction
                    if self.overall_progress_on:
                        # Add fraction of stage to overall progress
                        if self.stage_progress_on:
                            overall_progress = self.stages_finished * self.fraction_per_stage
                            if stage_abs:
                                if self.stage_progress_on and stage_abs < 100.0:
                                    overall_progress += (stage_abs / 100.0) * self.fraction_per_stage

                        # Update the GUI elements for overall progress
                        self.overall_progress["value"] = overall_progress
                        self.overall_label_var.set(f"{overall_progress:.2f}%")

                        # If overall progress reaches 100%, handle completion
                        if overall_progress >= 100.0:
                            # If all stages are finished, mark as done
                            self.done = True
                            if self.auto_close:
                                self._stop_console_redirection(morpy_trace, app_dict)
                                self._on_close(morpy_trace, app_dict)
                            else:
                                self.button_text.set(self.button_text_close)
                                self._stop_console_redirection(morpy_trace, app_dict)

                        # Decrement self.unfinished_tasks
                        self.ui_calls.task_done()

                        # Enforce an update on the GUI
                        self._enforce_update()

                    # 3) Reset stage progress last to avoid lag in between update of stage and overall progress.
                    if self.stage_progress_on and reset_stage_progress:
                        self.stage_progress_tracker._init(
                            morpy_trace, app_dict, description=self.headline_stage_nocol, total=self.max_per_stage,
                            ticks=.01, verbose=True
                        )
                        if self.stages_finished < self.stages:
                            if self.stage_progress is not None:
                                self.stage_progress["value"] = 0.0
                            if self.stage_label_var is not None:
                                self.stage_label_var.set("0.00%")
                        else:
                            # If all stages are finished, mark as done
                            self.done = True

                        # Decrement self.unfinished_tasks
                        self.ui_calls.task_done()

                        # Enforce an update on the GUI
                        self._enforce_update()

                # Enforce an update on the GUI
                self._enforce_update()

            check = True

        # Handle errors from GUI after aborting
        except TclError as tcl_e:
            # GUI ended ungracefully.
            log(morpy_trace, app_dict, "warning",
            lambda: f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_exit_dirty"]}\n'
                    f'{type(tcl_e).__name__}: {tcl_e}')

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    @metrics
    def update_text(self, morpy_trace: dict, app_dict: dict, headline_total: str = None, headline_stage: str = None,
                    description_stage: str = None):
        r"""
        Update the headline texts or description at runtime. Enqueues a UI request for the
        main thread to process. Safe to call from any thread.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param headline_total: If not None, sets the overall progress headline text.
        :param headline_stage: If not None, sets the stage progress headline text.
        :param description_stage: If not None, sets the description text beneath the stage headline.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether text update completed without errors

        :example:
            gui.update_text(morpy_trace, app_dict,
                headline_total="Processing Outer Loop 3",
                headline_stage="Processing File 5",
                description_stage="Now copying data...",
            )
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk.update_text(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:
            # Send text updates to the queue
            call_kwargs = {
                "headline_total" : headline_total,
                "headline_stage" : headline_stage,
                "description_stage" : description_stage,
            }
            self.ui_calls.put(("update_text", call_kwargs))

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        return {
            "morpy_trace": morpy_trace,
            "check": check,
        }

    @metrics
    def _real_update_text(self, morpy_trace: dict, app_dict: dict, headline_total: str = None,
                          headline_stage: str = None, description_stage: str = None):
        r"""
        Update the headline texts or description at runtime. Actually updates Tk widgets.
        Must be called only from the main thread.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param headline_total: If not None, sets the overall progress headline text.
        :param headline_stage: If not None, sets the stage progress headline text.
        :param description_stage: If not None, sets the description text beneath the stage headline.

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether text update completed without errors

        :example:
            gui.update_text(morpy_trace, app_dict,
                headline_total="Processing Outer Loop 3",
                headline_stage="Processing File 5",
                description_stage="Now copying data...",
            )
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk._real_update_text(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:
            # Avoid updates after "abort"
            if not self.done:
                # Check, if running in main thread
                check_main_thread(app_dict)

                # Update overall headline
                if headline_total is not None and self.overall_progress_on:
                    # Retain the final colon to stay consistent with constructor
                    self.headline_total_nocol = headline_total
                    self.headline_total = self.headline_total_nocol + ":"
                    self.overall_progress_tracker.description = self.headline_total_nocol
                    if self.total_headline_label is not None:
                        self.total_headline_label.config(text=self.headline_total)

                    # Enforce an update on the GUI
                    self._enforce_update()

                # Update stage headline
                if headline_stage is not None and self.stage_progress_on:
                    # Retain the final colon to stay consistent with constructor
                    self.headline_stage_nocol = headline_stage
                    self.headline_stage = self.headline_stage_nocol + ":"
                    self.stage_progress_tracker.description = self.headline_stage_nocol
                    if self.stage_headline_label is not None:
                        self.stage_headline_label.config(text=self.headline_stage)

                    # Enforce an update on the GUI
                    self._enforce_update()

                # Update description
                if description_stage is not None:
                    self.description_stage = description_stage
                    # If the label didn't exist but was called, we don't create it on the fly.
                    # We only update if the widget is already present:
                    if self.stage_description_label is not None:
                        self.stage_description_label.config(text=self.description_stage)

                    # Enforce an update on the GUI
                    self._enforce_update()

            check = True

        # Handle errors from GUI after aborting
        except TclError as tcl_e:
            # GUI ended ungracefully.
            log(morpy_trace, app_dict, "warning",
            lambda: f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_exit_dirty"]}\n'
                    f'{type(tcl_e).__name__}: {tcl_e}')

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        return {"morpy_trace": morpy_trace, "check": check}

    @metrics
    def run(self, morpy_trace: dict, app_dict: dict):
        r"""
        Start the GUI main loop and run the Tk mainloop on the main thread.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            progress = morPy.ProgressTrackerTk(morpy_trace: dict, app_dict,
                frame_title="My Demo Progress GUI",
                description_stage="Generic Progress stage",
                stages=1,
                max_per_stage=10,
                work=work)

            progress.run(morpy_trace, app_dict)
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk.run(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:
            # Start our custom loop
            self._main_loop(morpy_trace, app_dict)
            self.root.mainloop()

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    @metrics
    def _start_work_thread(self, morpy_trace: dict, app_dict: dict):
        r"""
        TODO implement morPy threading and use it here
            > right now interrupt/abort does not work as desired: background threads shall be terminated immediately.

        Launch the user-supplied function in a background thread.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._start_work_thread(morpy_trace, app_dict)
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk._start_work_thread(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        def _thread_wrapper():
            try:
                # Automatically pass gui=self to the work_callable
                self.work_callable(gui=self)
            except Exception as e:
                # Exception in the worker thread.
                log(morpy_trace, app_dict, "error",
                lambda: f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_start_work_thread_err"]}\n'
                        f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno} '
                        f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                        f'{type(e).__name__}: {e}')

        try:
            self.worker_thread = threading.Thread(target=_thread_wrapper, daemon=True)
            self.worker_thread.start()

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    @metrics
    def _on_close(self, morpy_trace: dict, app_dict: dict):
        r"""
        Close or abort the GUI.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._on_close(morpy_trace, app_dict)
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk._on_close(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False

        try:
            # Restore original console if not already done
            self._stop_console_redirection(morpy_trace, app_dict)
            self.root.quit()
            self.root.destroy()

            # In case of aborting progress quit the program.
            if not self.done:
                # Initiate program exit
                app_dict["global"]["morpy"]["exit"] = True

                # Release the global interrupts
                app_dict["global"]["morpy"]["interrupt"] = False

                # Set done to omit pulling from GUI queue after close
                self.done = True

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
        }

    @metrics
    def get_console_output(self, morpy_trace: dict, app_dict: dict):
        r"""
        Retrieve the current text from the console widget.

        :param morpy_trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self.get_console_output(morpy_trace, app_dict)
        """

        module = 'ui_tk'
        operation = 'ProgressTrackerTk.get_console_output(~)'
        morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

        check = False
        console_text = ""

        try:
            if self.console_output is not None:
                console_text = self.console_output.get("1.0", tk.END).strip()

            check = True

        except Exception as e:
            log(morpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                    f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                    f'{type(e).__name__}: {e}')

        return {
            "morpy_trace" : morpy_trace,
            "check" : check,
            "console_output" : console_text,
        }

def check_main_thread(app_dict: dict):
    r"""
    Check, if GUI runs in main thread. Otherwise, instabilities are introduced
    with tkinter.

    :param app_dict: morPy global dictionary containing app configurations

    :return:
        -

    :example:
        check_main_thread(app_dict)
    """

    # UI must run in main thread. Currently in ###
    if threading.current_thread() is not threading.main_thread():
        raise RuntimeError(
            f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_check_main"]}: {threading.current_thread()}'
        )

@metrics
def dialog_sel_file(morpy_trace: dict, app_dict: dict, init_dir: str=None, ftypes: tuple=None, title: str=None) -> dict:

    r"""
    This function opens a dialog for the user to select a file.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param ftypes: This tuple of 2-tuples specifies, which filetypes will be
        selectable in the dialog box.
    :param title: Title of the open file dialog

    :return: dict
        morpy_trace: operation credentials and tracing
        check: The function ended with no errors and a file was chosen
        file_path: Path of the selected file
        file_selected: True, if file was selected. False, if canceled.

    :example:
        init_dir = "C:\"
        ftypes = (('PDF','*.pdf'),('Textfile','*.txt'),('All Files','*.*'))
        title = 'Select a file...'
        file_path = morPy.dialog_sel_file(morpy_trace, app_dict, init_dir, ftypes, title)["file_path"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'ui_tk'
    operation = 'dialog_sel_file(~)'
    morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

    check = False
    file_path = None
    file_selected = False

    try:
        if not init_dir:
            init_dir = app_dict["conf"]["main_path"]
        if not ftypes:
            ftypes = (f'{app_dict["loc"]["morpy"]["dialog_sel_file_all_files"]}','*.*')
        if not title:
            title = f'{app_dict["loc"]["morpy"]["dialog_sel_file_select"]}'

        # Invoke the Tkinter root window and withdraw it to force the
        # dialog to be opened in the foreground
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        root.iconbitmap(app_dict["conf"]["app_icon"])

        # Open the actual dialog in the foreground and store the chosen folder
        file_path = filedialog.askopenfilename(
            parent = root,
            title = f'{title}',
            initialdir = init_dir,
            filetypes = ftypes,
        )

        if not file_path:
            # No file was chosen by the user.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["dialog_sel_file_nosel"]}\n'
                    f'{app_dict["loc"]["morpy"]["dialog_sel_file_choice"]}: {app_dict["loc"]["morpy"]["dialog_sel_file_cancel"]}')

        else:
            file_selected = True
            # A file was chosen by the user.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["dialog_sel_file_asel"]}\n'
                    f'{app_dict["loc"]["morpy"]["dialog_sel_file_path"]}: {file_path}\n'
                    f'{app_dict["loc"]["morpy"]["dialog_sel_file_choice"]}: {app_dict["loc"]["morpy"]["dialog_sel_file_open"]}')

            # Create a path object
            morpy_fct.pathtool(file_path)

        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'file_path' : file_path,
        'file_selected' : file_selected,
        }

@metrics
def dialog_sel_dir(morpy_trace: dict, app_dict: dict, init_dir: str=None, title: str=None) -> dict:

    r"""
    This function opens a dialog for the user to select a directory.

    :param morpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param title: Title of the open directory dialog

    :return: dict
        morpy_trace: operation credentials and tracing
        check: The function ended with no errors and a file was chosen
        dir_path: Path of the selected directory
        dir_selected: True, if directory was selected. False, if canceled.

    :example:
        init_dir = "C:\"
        title = 'Select a directory...'
        dir_path = morPy.dialog_sel_dir(morpy_trace, app_dict, init_dir, title)["dir_path"]
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'ui_tk'
    operation = 'dialog_sel_dir(~)'
    morpy_trace = morpy_fct.tracing(module, operation, morpy_trace)

    check = False
    dir_path = None
    dir_selected = False

    try:
        if not init_dir:
            init_dir = app_dict["conf"]["main_path"]
        if not title:
            title = f'{app_dict["loc"]["morpy"]["dialog_sel_dir_select"]}'

        # Invoke the Tkinter root window and withdraw it to force the
        # dialog to be opened in the foreground
        root = tk.Tk()
        root.withdraw()
        root.iconbitmap(app_dict["conf"]["app_icon"])

        # Open the actual dialog in the foreground and store the chosen folder
        root.dir_name = filedialog.askdirectory(
            parent = root,
            title = f'{title}',
            initialdir = init_dir,
        )
        dir_path = root.dir_name

        if not dir_path:
            # No directory was chosen by the user.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["dialog_sel_dir_nosel"]}\n'
                f'{app_dict["loc"]["morpy"]["dialog_sel_dir_choice"]}: {app_dict["loc"]["morpy"]["dialog_sel_dir_cancel"]}')
        else:
            dir_selected = True
            # A directory was chosen by the user.
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["dialog_sel_dir_asel"]}\n'
                    f'{app_dict["loc"]["morpy"]["dialog_sel_dir_path"]}: {dir_path}\n'
                    f'{app_dict["loc"]["morpy"]["dialog_sel_dir_choice"]}: {app_dict["loc"]["morpy"]["dialog_sel_dir_open"]}')

            # Create a path object
            morpy_fct.pathtool(dir_path)

        check = True

    except Exception as e:
        log(morpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morpy"]["err_line"]} {sys.exc_info()[-1].tb_lineno} '
                f'{app_dict["loc"]["morpy"]["err_module"]} {module}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        'dir_path' : dir_path,
        'dir_selected' : dir_selected,
        }
