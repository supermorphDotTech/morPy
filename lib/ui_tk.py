r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module provides UI-building functions using the Tkinter.
"""

import lib.fct as morpy_fct
import lib.common as common
from morPy import log
from lib.decorators import morpy_wrap

import sys
import threading, queue
import ctypes
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import TclError
from PIL import Image, ImageTk
from queue import Empty


class FileDirSelectTk:
    r"""
    A tkinter GUI for file and directory selection. Each row represents a file or directory selection.
    Optionally displays a top row of icons (display only).
    """


    @morpy_wrap
    def __init__(self, trace: dict, app_dict: dict, rows_data: dict, title: str = None,
                 icon_data: dict = None) -> None:
        r"""
        Class constructor.

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
                    "position" : 1,         # placement, order (lowest first)
                    "img_path" : "path/to/image.png",     # image file path
                    "icon_size" : (width, height),        # (optional) size for the icon},
                    ...}

        :return: dict
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

        # Try to make the process DPI-aware
        # TODO port into os-class instead of hardcoding and make sure that each spawn will run this.
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except AttributeError | OSError:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except AttributeError | OSError:
                pass

        self.rows_data = rows_data
        self.title = title if title else app_dict["loc"]["morpy"]["FileDirSelectTk_title"]

        if icon_data:
            self.icon_data = icon_data
        else:
            self.icon_data = {
            "app_banner" : {
                "position" : 1,
                "img_path" : app_dict["morpy"]["conf"]["app_banner"],
                "icon_size" : (214, 48)
            }
        }

        # Set default icon size
        icon_dim = int(app_dict["morpy"]["sys"]["resolution_height"] // 64)
        self.default_icon_size = (icon_dim, icon_dim)

        # Set default entry width
        entry_dim = int(app_dict["morpy"]["sys"]["resolution_height"] // 24)
        self.default_entry_width = entry_dim

        # Set default link size
        link_dim = int(app_dict["morpy"]["sys"]["resolution_height"] // 48)
        self.default_link_size = (link_dim, link_dim)

        self.selections = {}  # Will hold the final user inputs keyed by row name.

        # Dictionary to hold references to PhotoImage objects.
        self._photos = {}
        self.app_dict = app_dict

        # Create the main tkinter window.
        self.root = tk.Tk()
        self.root.iconbitmap(app_dict["morpy"]["conf"]["app_icon"])
        self.root.title(self.title)
        # Allow the window to be resizable.
        self.root.resizable(True, True)

        # Build the UI.
        self._setup_ui(trace, app_dict)

        # Calculate coordinates for the window to be centered.
        x = (int(app_dict["morpy"]["sys"]["resolution_width"]) // 2) - (self.frame_width // 2)
        y = (int(app_dict["morpy"]["sys"]["resolution_height"]) * 2 // 5) - (self.frame_height // 2)
        self.root.geometry(f'{self.frame_width}x{self.frame_height}+{x}+{y}')

        # Bind the _on_close() method to closing the window
        self.root.protocol("WM_DELETE_WINDOW", lambda: self._on_close(trace, app_dict))


    @morpy_wrap
    def _setup_ui(self, trace: dict, app_dict: dict) -> None:
        r"""
        Constructs the grid layout with the provided configuration.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        from functools import partial

        # Optional top icon row.
        if self.icon_data:
            icon_frame = tk.Frame(self.root)
            icon_frame.pack(fill='x', anchor='e', padx=20, pady=(20, 10))
            resample_filter = Image.Resampling.LANCZOS

            for icon_name, config in sorted(self.icon_data.items(),
                                            key=lambda item: item[1].get("position", 0)):
                img_path = morpy_fct.pathtool(config.get("img_path"))["out_path"]
                icon_size = config.get("icon_size", self.default_icon_size)

                try:
                    img = Image.open(img_path)
                except Exception as e:
                    raise RuntimeError(
                        f'{app_dict["loc"]["morpy"]["FileDirSelectTk_img_fail"]}\n'
                        f'Icon {icon_name}: {img_path}\n{e}'
                    )

                img = img.resize(icon_size, resample_filter)
                photo = ImageTk.PhotoImage(img)
                self._photos[icon_name] = photo
                # ImageTk.PhotoImage instances work perfectly with Tkinter widgets. Lint ignore.
                label = tk.Label(icon_frame, image=photo)  # type: ignore
                label.pack(side=tk.RIGHT, padx=5)

        # Create a frame to contain all selection rows.
        rows_container = tk.Frame(self.root)
        rows_container.pack(fill='both', expand=True, padx=20, pady=20)

        # For each selection row, create a container frame.
        self.row_widgets = {}  # To store per-row widgets.
        for row_name, config in self.rows_data.items():
            # Prefill return dictionary in case of immediate exit
            self.selections[row_name] = None

            # Container for a single row (including its optional description).
            row_container = tk.Frame(rows_container)
            row_container.pack(fill='x', pady=10)

            # If a description is provided in the config, create a descriptive headline.
            if config.get("description"):
                desc_label = tk.Label(row_container, text=config["description"], font=("Arial", 8))
                desc_label.pack(anchor='w', pady=(0, 5))

            # Create a frame for the input widgets (entry and button) in this row.
            row_frame = tk.Frame(row_container)
            row_frame.pack(fill='x')

            # Entry widget.
            entry = tk.Entry(row_frame, width=self.default_entry_width)
            default_path = ''  # or config.get("default_path", "")
            entry.insert(0, default_path)
            entry.pack(side=tk.LEFT, fill='x', expand=True, padx=(0, 10))
            self.row_widgets[row_name] = {"entry": entry}

            # Determine which image to display.
            custom_img = config.get("image_path")
            image_size = config.get("image_size", self.default_link_size)

            # If no custom image is provided, use a default icon.
            if not custom_img:
                if config.get("is_dir", False):
                    custom_img = morpy_fct.pathtool(f'{app_dict["morpy"]["conf"]["main_path"]}\\res\\icons\\dir_open.png')["out_path"]
                else:
                    custom_img = morpy_fct.pathtool(f'{app_dict["morpy"]["conf"]["main_path"]}\\res\\icons\\file_open.png')["out_path"]

            # Load the image.
            try:
                img_path = morpy_fct.pathtool(custom_img)["out_path"]
                img = Image.open(img_path)
            except Exception as e:
                # Failed to load image.
                raise RuntimeError(
                    f'{app_dict["loc"]["morpy"]["FileDirSelectTk_img_fail"]}\n'
                    f'{app_dict["loc"]["morpy"]["FileDirSelectTk_row_name"]}: {row_name}\n'
                    f'{app_dict["loc"]["morpy"]["FileDirSelectTk_img"]}: {custom_img}\n{e}'
                )

            if image_size:
                resample_filter = Image.Resampling.LANCZOS
                img = img.resize(image_size, resample_filter)

            photo = ImageTk.PhotoImage(img)
            self._photos[row_name] = photo  # Keep a reference.

            # Button to trigger the selection dialog.
            # ImageTk.PhotoImage instances work perfectly with Tkinter widgets. Lint ignore.
            button = tk.Button(
                row_frame,
                # ImageTk.PhotoImage instances work perfectly with Tkinter widgets. Lint ignore.
                image=photo,   # type: ignore
                command=partial(self._on_select, trace, app_dict, row_name, config)
            )
            button.pack(side=tk.RIGHT)
            self.row_widgets[row_name]["button"] = button

        # At the bottom, add a confirmation button.
        confirm_button = ttk.Button(self.root, text=f'{app_dict["loc"]["morpy"]["FileDirSelectTk_confirm"]}',
                                 command=lambda: self._on_confirm(trace, app_dict))
        confirm_button.pack(pady=(10, 20))

        # Update frame dimensions.
        self.root.update_idletasks()  # Process pending geometry updates
        self.frame_width = self.root.winfo_width()
        self.frame_height = self.root.winfo_height()


    @morpy_wrap
    def _on_select(self, trace: dict, app_dict: dict, row_name: str, config: dict) -> None:
        r"""
        Callback for a selection row button. Opens a file or directory dialog based on the "is_dir" flag.
        Updates the corresponding Entry widget with the chosen path.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        if config.get("is_dir", False):
            # Directory selection.
            description = config.get("description", app_dict["loc"]["morpy"]["dialog_sel_dir_select"])
            init_dir = config.get("default_path", app_dict["morpy"]["conf"]["data_path"])

            path = dialog_sel_dir(trace, app_dict, init_dir=init_dir, title=description)["dir_path"]

        else:
            # File selection.
            file_types = config.get("file_types", (("All Files", "*.*"),))
            description = config.get("description", app_dict["loc"]["morpy"]["dialog_sel_file_select"])
            init_dir = config.get("default_path", app_dict["morpy"]["conf"]["data_path"])

            path = dialog_sel_file(trace, app_dict, init_dir=init_dir, file_types=file_types,
                                   title=description)["file_path"]

        if path:
            # Update the entry.
            self.row_widgets[row_name]["entry"].delete(0, tk.END)
            self.row_widgets[row_name]["entry"].insert(0, path)


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def _on_confirm(self, trace: dict, app_dict: dict) -> None:
        r"""
        Callback for the confirm button. Reads all the entries and stores them in self.selections.
        Then, quits the main loop.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        for row_name, widgets in self.row_widgets.items():
            self.selections[row_name] = widgets["entry"].get()
        self.root.quit()


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def _on_close(self, trace: dict, app_dict: dict) -> None:
        r"""
        Close or abort the GUI.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :example:
            self._on_close(trace, app_dict)
        """

        self.root.quit()

        # Initiate program exit
        # TODO conditional lock
        app_dict["morpy"]["exit"] = True

        # Release the global interrupts
        app_dict["morpy"]["interrupt"] = False


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def run(self, trace: dict, app_dict: dict) -> dict:
        r"""
        Launches the GUI and waits for the user to complete the selection.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            selections: A dictionary of user inputs keyed by row name.
        """

        self.root.mainloop()
        self.root.destroy()

        return {
            "selections": self.selections
        }


class GridChoiceTk:
    r"""
    A tkinter GUI displaying a dynamic grid of image tiles. Each tile shows an image
    with a text label below it. Clicking a tile returns its associated value.
    """


    @morpy_wrap
    def __init__(self, trace: dict, app_dict: dict, tile_data: dict, title: str=None,
              default_tile_size: tuple=None, icon_data: dict=None) -> None:
        r"""
        Class constructor.

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

        default_tile_size_ok: bool = False

        # Try to make the process DPI-aware
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except AttributeError | OSError:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except AttributeError | OSError:
                pass

        self.tile_data = tile_data
        self.title = title if title else app_dict["loc"]["morpy"]["GridChoiceTk_title"]

        # Set default tile size
        if default_tile_size:
            self.default_tile_size = default_tile_size
            # Default tile size
            if (isinstance(self.default_tile_size, tuple)
                and isinstance(self.default_tile_size[0], int)
                and isinstance(self.default_tile_size[1], int)):
                default_tile_size_ok = True

        if not default_tile_size_ok:
            tile_dim = int(app_dict["morpy"]["sys"]["resolution_height"] // 8)
            self.default_tile_size = (tile_dim, tile_dim)

        if icon_data:
            self.icon_data = icon_data
        else:
            self.icon_data = {
            "app_banner" : {
                "position" : 1,
                "img_path" : app_dict["morpy"]["conf"]["app_banner"],
                "icon_size" : (214, 48)
            }
        }

        # Set default icon size
        icon_dim = int(app_dict["morpy"]["sys"]["resolution_height"] // 64)
        self.default_icon_size = (icon_dim, icon_dim)

        self.choice = None
        self.frame_width = 0
        self.frame_height = 0

        # Create the main tkinter window.
        self.root = tk.Tk()
        self.root.iconbitmap(app_dict["morpy"]["conf"]["app_icon"])
        self.root.title(self.title)

        # A dictionary to keep references to PhotoImage objects. Prevents garbage collection of images.
        self._photos = {}

        self._setup_ui(trace, app_dict)

        # Calculate coordinates for the window to be centered.
        x = (int(app_dict["morpy"]["sys"]["resolution_width"]) // 2) - (self.frame_width // 2)
        y = (int(app_dict["morpy"]["sys"]["resolution_height"]) * 2 // 5) - (self.frame_height // 2)
        self.root.geometry(f'{self.frame_width}x{self.frame_height}+{x}+{y}')

        # Bind the _on_close() method to closing the window
        self.root.protocol("WM_DELETE_WINDOW", lambda: self._on_close(trace, app_dict))

        # Fix the frame size, since it's contents do not resize.
        self.root.resizable(False, False)


    @morpy_wrap
    def _setup_ui(self, trace: dict, app_dict: dict) -> None:
        r"""
        Constructs the grid layout with the provided tile data.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        # If icon_data is provided, create a top row for icons.
        if self.icon_data:
            # Create a frame for the icons (placed at the top of the window).
            icon_frame = tk.Frame(self.root)
            icon_frame.pack(fill='x', anchor='e', padx=20, pady=(20, 10))  # extra top padding if desired

            resample_filter = Image.Resampling.LANCZOS

            # Process icons in sorted order (using the "position" value).
            for icon_name, config in sorted(self.icon_data.items(),
                                              key=lambda item: item[1].get("position", 0)):
                img_path = morpy_fct.pathtool(config.get("img_path"))["out_path"]
                # If an icon size is provided, use it; else, use a reasonable default (e.g. same as tile size)
                icon_size = config.get("icon_size", self.default_icon_size)
                try:
                    img = Image.open(img_path)
                except Exception as e:
                    raise RuntimeError(
                        f'{app_dict["loc"]["morpy"]["GridChoiceTk_img_fail"]}\n'
                        f'{app_dict["loc"]["morpy"]["GridChoiceTk_path"]}: {img_path}\n'
                        f'{app_dict["loc"]["morpy"]["GridChoiceTk_tile"]}: {icon_name}\n{e}'
                    )
                if icon_size:
                    img = img.resize(icon_size, resample_filter)
                photo = ImageTk.PhotoImage(img)
                self._photos[icon_name] = photo  # Prevent garbage collection

                # Create a label to display the icon.
                # ImageTk.PhotoImage instances work perfectly with Tkinter widgets. Lint ignore.
                label = tk.Label(icon_frame, image=photo)  # type: ignore
                label.pack(side=tk.RIGHT, padx=5)

        # Create the container for the grid of tiles.
        container = tk.Frame(self.root)
        container.pack(padx=10, pady=10)

        for tile_name, config in self.tile_data.items():
            row, column = config.get("row_column", (0, 0))
            img_path = morpy_fct.pathtool(config.get("img_path"))["out_path"]
            text = config.get("text", "")
            return_value = config.get("return_value")
            tile_size = config.get("tile_size", self.default_tile_size)

            # Create a frame for this tile.
            tile_frame = tk.Frame(container)
            tile_frame.grid(row=row, column=column, padx=10, pady=10)

            resample_filter = Image.Resampling.LANCZOS

            # Load and resize the image.
            try:
                img = Image.open(img_path)
            except Exception as e:
                # Failed to load image.
                raise RuntimeError(
                    f'{app_dict["loc"]["morpy"]["GridChoiceTk_img_fail"]}\n'
                    f'{app_dict["loc"]["morpy"]["GridChoiceTk_path"]}: {img_path}\n'
                    f'{app_dict["loc"]["morpy"]["GridChoiceTk_tile"]}: {tile_name}\n{e}'
                )

            img = img.resize(tile_size, resample_filter)
            photo = ImageTk.PhotoImage(img)
            self._photos[tile_name] = photo  # Save a reference to avoid garbage collection.

            # Create a button with the image.
            button = tk.Button(
                tile_frame,
                # ImageTk.PhotoImage instances work perfectly with Tkinter widgets. Lint ignore.
                image=photo,   # type: ignore
                command=lambda val=return_value: self._on_select(trace, app_dict, val))
            button.pack()

            # Create a label below the image.
            label = tk.Label(tile_frame, text=text, font=("Arial", 8, "bold"))
            label.pack(pady=(5, 0))

            # Update frame dimensions.
            self.root.update_idletasks()  # Process pending geometry updates
            self.frame_width = self.root.winfo_width()
            self.frame_height = self.root.winfo_height()


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def _on_select(self, trace: dict, app_dict: dict, value) -> None:
        r"""
        Callback when a tile is clicked. Sets the selected value and quits the mainloop.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param value: Selected value relating to the clicked tile.
        """

        self.choice = value
        self.root.quit()


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def _on_close(self, trace: dict, app_dict: dict) -> None:
        r"""
        Close or abort the GUI.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        self.root.quit()

        # Initiate program exit
        # TODO conditional lock
        app_dict["morpy"]["exit"] = True

        # Release the global interrupts
        app_dict["morpy"]["interrupt"] = False


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def run(self, trace: dict, app_dict: dict):
        r"""
        Launches the GUI and waits for the user to make a selection.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
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

        self.root.mainloop()
        self.root.destroy()

        return {
            "choice" : self.choice
        }


class ProgressTrackerTk:
    r"""
    A progress tracking GUI using tkinter to visualize the progress of a task.
    If progress consists of several stages, a separate progress bar for the
    stages progress is displayed. The total count of progress steps is set by
    initializing a stage with the 'begin_stage()' method, regardless of the total
    amount of stages. Optionally allows to display console messages in a console
    widget.
    """


    @morpy_wrap
    def __init__(self, trace: dict, app_dict: dict, frame_title: str=None, frame_width: int=None,
              frame_height: int=None, headline_total: str=None, headline_font_size: int=10,
              detail_description_on: bool=False, description_font_size: int=8, font: str="Arial",
              stages: int=1, console: bool=False, auto_close: bool=False, work=None) -> None:
        r"""
        Class constructor.

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

        :example:
            progress_gui = morPy.ProgressTrackerTk(
                trace: dict, app_dict,
                frame_title="My Demo Progress GUI",
                detail_description="Generic Progress stage",
                stages=outer_loop_count,
                stage_limit=inner_loop_count,
                work=work
            )
        """

        self.frame_height_sizing: bool      = False
        self.height_factor_headlines: int   = 0
        self.height_factor_description: int = 0
        self.destroy: bool                  = False

        # Try to make the process DPI-aware
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except AttributeError | OSError:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except AttributeError | OSError:
                pass

        self.console_on = console
        self.auto_close = auto_close
        self.done = False  # Will be True once overall progress is 100%
        self.main_loop_interval = 50 # ms, how often we do the main loop

        # Default texts
        self.frame_title = (app_dict["loc"]["morpy"]["ProgressTrackerTk_prog"]
                            if not frame_title else frame_title)
        self.frame_width = frame_width
        self.headline_total_no_col = (f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_overall"]}'
                         if not headline_total else f'{headline_total}')
        self.detail_description_on = detail_description_on
        self.headline_font_size = headline_font_size
        self.description_font_size = description_font_size
        self.font = font
        self.button_text_abort = f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_abort"]}'
        self.button_text_close = f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_close"]}'

        self.ui_calls = queue.Queue()  # Queue for collecting UI update requests from background thread

        # Progress tracking
        self.stages = stages

        self.stages_finished = 0
        self.overall_progress_abs = 0

        # Set frame width
        if not frame_width:
            sys_width = int(app_dict["morpy"]["sys"]["resolution_width"])
            self.frame_width = sys_width // 3
        else:
            self.frame_width = frame_width

        # Calculate factors for frame height
        sys_height = int(app_dict["morpy"]["sys"]["resolution_height"])
        height_factor = sys_height * .03125 # Height of main monitor * 32dpi // 1024px
        if not frame_height:
            self.frame_height = 0
            self.frame_height_sizing = True
            self.height_factor_headlines = round(height_factor * self.headline_font_size / 10)
            self.height_factor_description = round(height_factor * self.description_font_size / 10)
        else:
            self.frame_height = frame_height
            self.frame_height_sizing = False

        # Overall progress bar
        if self.stages > 1:
            self.overall_progress_on = True

            # Set fraction of overall progress per stage
            self.fraction_per_stage  = 100.0 / self.stages

            # Add height for overall progress bar
            if self.frame_height_sizing:
                self.frame_height += self.height_factor_headlines

            # Construct the overall progress tracker
            self.overall_progress_tracker = common.ProgressTracker(
                trace, app_dict, description=self.headline_total_no_col, total=self.stages, ticks=.01,
                verbose=True
            )

            # Finalize overall headline
            self.headline_total = f'{self.headline_total_no_col}:'
        else:
            self.overall_progress_on = False

        # Add height for stage progress bar
        if self.frame_height_sizing:
            self.frame_height += self.height_factor_headlines

        # Detail description
        if self.detail_description_on:
            # Add height for description of latest update
            if self.frame_height_sizing:
                self.frame_height += self.height_factor_description

        # For capturing prints
        self.console_queue = None  # Always define, even if console_on=False
        if self.console_on:
            self.console_queue = queue.Queue()

            # Add frame height for console
            if self.frame_height_sizing:
                self.frame_height += app_dict["morpy"]["sys"]["resolution_height"] // 2

        # Calculate coordinates for the window to be centered.
        x = (int(app_dict["morpy"]["sys"]["resolution_width"]) // 2) - (self.frame_width // 2)
        y = (int(app_dict["morpy"]["sys"]["resolution_height"]) * 2 // 5) - (self.frame_height // 2)

        # Tk window
        self.root = tk.Tk()
        self.root.iconbitmap(app_dict["morpy"]["conf"]["app_icon"])
        self.root.title(self.frame_title)
        self.root.geometry(f'{self.frame_width}x{self.frame_height}+{x}+{y}')

        # Bind the _on_close() method to closing the window
        self.root.protocol("WM_DELETE_WINDOW", lambda: self._on_close(trace, app_dict))

        self._create_widgets(trace, app_dict)

        # The background work to run (if any)
        self.work_callable = work
        if self.work_callable is not None:
            self._start_work_thread(trace, app_dict)

        self.init_passed = True


    @morpy_wrap
    def _create_widgets(self, trace: dict, app_dict: dict) -> None:
        r"""
        Build and place all widgets in a grid layout.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        self.overall_progress_text = None
        self.stage_progress_text = None

        # Check, if running in main thread (if you have that function)
        check_main_thread(trace, app_dict)

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
        self.root.rowconfigure(1, weight=0)

        # Stage headline (ttk.Label)
        self.stage_headline_label = ttk.Label(
            self.root,
            text="",
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

        # Detail description at progress update
        if self.detail_description_on:
            self.root.rowconfigure(2, weight=0)
            # Still a ttk.Label
            self.stage_description_label = ttk.Label(
                self.root,
                text="",
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
            self.console_output["yscrollcommand"] = self.console_scrollbar.set # noqa: SPELLCHECK
        else:
            self.console_output = None

        # Grid config - Bottom row
        self.root.rowconfigure(4, weight=0)

        # Close/Abort button (ttk.Button)
        self.button_text = tk.StringVar(value=self.button_text_abort)
        self.close_button = ttk.Button(
            self.root,
            textvariable=self.button_text,
            command=lambda: self._on_close(trace, app_dict)
        )
        self.close_button.grid(row=4, column=2, columnspan=1, padx=10, pady=(0, 10), sticky="nse")

        # Enforce an update on the GUI
        self._enforce_update()

        # Redirect output to console
        if self.console_on:
            self._redirect_console(trace, app_dict)

    def _enforce_update(self) -> None:
        r"""
        Enforce an update of the GUI. If not leveraged after GUI update, might not display.

        :example:
            # Enforce an update on the GUI
            self._enforce_update()
        """

        # Guard this method against callbacks after closing
        if self.root.winfo_exists():
            self.root.update_idletasks()
            self.root.update()


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def _redirect_console(self, trace: dict, app_dict: dict) -> None:
        r"""
        Redirect sys.stdout/sys.stderr to self.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            trace: Operation credentials and tracing
            check: Indicates whether initialization completed without errors

        :example:
            self._redirect_console(trace, app_dict)
        """

        sys.stdout = self
        sys.stderr = self

    def write(self, message: str) -> None:
        r"""
        Captured print statements go into a queue.

        :param message: Message to be printed to console

        FIXME fix writes to console. Messages are not arriving at GUI due to
            sequential threading.
        """

        if self.console_queue is not None:
            self.console_queue.put(message)

    def flush(self) -> None:
        r"""
        Required for stdout redirection.
        """
        pass


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def _stop_console_redirection(self, trace: dict, app_dict: dict) -> None:
        r"""
        Stop capturing print statements in the GUI console.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


    @morpy_wrap
    def _main_loop(self, trace, app_dict) -> None:
        r"""
        Main repeating loop for GUI refreshes. Read console queue to update text widget (unless we are done &
        auto_close=False). Update the progress bars (unless done), then schedule itself again.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :example:
            self._main_loop(trace, app_dict)
        """

        # Immediately exit if done/closing.
        if self.done or not self.root.winfo_exists():
            return

        # Process console output if needed
        if self.console_on and not self.done:
            self._update_console(trace, app_dict)

        # Process any pending UI updates from the background thread
        while not self.ui_calls.empty():
            call_type, kwargs = self.ui_calls.get_nowait()

            # Update displayed information and widgets in GUI
            match call_type:
                case "update_text":     self._real_update_text(trace, app_dict, **kwargs)
                case "update_progress": self._real_update_progress(trace, app_dict, **kwargs)
                case "begin_stage":     self._real_begin_stage(trace, app_dict, **kwargs)

        # Only schedule the next loop if still alive
        if not self.done and self.root.winfo_exists():
            self.root.after(self.main_loop_interval, self._main_loop, trace, app_dict)


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def _update_console(self, trace: dict, app_dict: dict) -> None:
        r"""
        One-time call to read from the queue and add text to the widget.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        # Check, if running in main thread
        check_main_thread(trace, app_dict)
        while not self.console_queue.empty():
            msg = self.console_queue.get_nowait()
            if self.console_output is not None:
                self.console_output.insert(tk.END, msg)
                self.console_output.see(tk.END)

            # Enforce an update on the GUI
            self._enforce_update()


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def begin_stage(self, trace: dict, app_dict: dict, stage_limit: (int, float) = 1, headline_stage: str = None,
                    detail_description: str=None, ticks: float=.01) -> None:
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

        # Prevent updates after the GUI is closed.
        if not self.done:

            call_kwargs = {
                "stage_limit" : stage_limit,
                "headline_stage" : headline_stage,
                "detail_description" : detail_description,
                "ticks" : ticks
            }
            self.ui_calls.put(("begin_stage", call_kwargs))
            self._enforce_update()


    @morpy_wrap
    def _real_begin_stage(self, trace: dict, app_dict: dict, stage_limit: (int, float) = 1, headline_stage: str = None,
                    detail_description: str=None, ticks: float=.01) -> None:
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

        :example:
            # Set up the next stage
            headline = "Currently querying"
            description = "Starting stage..."
            progress.begin_stage(trace, app_dict, stage_limit=10, headline_stage=headline,
            detail_description=description)
        """

        # Prevent updates after the progress is complete.
        if not self.done:
            # Try resetting progress
            if hasattr(self, "stage_progress_tracker"):
                self._real_update_progress(trace, app_dict, current=0)

            # Stage headline
            self.headline_stage_no_col = (
                f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_curr"]}'
                if not headline_stage else f'{headline_stage}'
            )
            # Finalize stage headline
            self.headline_stage = f'{self.headline_stage_no_col}:'

            self.detail_description = detail_description
            self.stage_limit = stage_limit

            # Construct the stage progress tracker
            self.stage_progress_tracker = common.ProgressTracker(
                trace, app_dict, description=self.headline_stage_no_col, total=self.stage_limit,
                ticks=ticks, verbose=True
            )

            # Send text updates to the queue
            call_kwargs = {
                "headline_stage" : self.headline_stage_no_col,
                "detail_description" : self.detail_description,
            }
            self.ui_calls.put(("update_text", call_kwargs))

            # Enforce an update on the GUI
            self._enforce_update()


    @morpy_wrap
    def end_stage(self, trace: dict, app_dict: dict) -> None:
        r"""
        End the current stage by setting it to 100%.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :example:
            progress_gui.end_stage(trace, app_dict)
        """

        self.update_progress(trace, app_dict, current=self.stage_limit)


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def update_progress(self, trace: dict, app_dict: dict, current: float = None) -> None:
        r"""
        Update stage progress & overall progress. If overall hits 100% and auto_close=True, close window. Else,
        switch button text to "Close" and stop console redirection. Enqueues a UI request for the
        main thread to process. Safe to call from any thread.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param current: Current progress count. If None, each call of this method will add +1
            to the progress count. Defaults to None.

        :example:
            progress_gui = morPy.ProgressTrackerTk(
                trace, app_dict,
                frame_title="My Demo Progress GUI",
                detail_description="Starting stage 1",
                stages=2,
                stage_limit=10,
                work=work
            )

            progress_gui.run(trace, app_dict)

            curr_cnt = 5.67
            msg = f'Currently at {curr_cnt}'
            progress_gui.update_progress(trace, app_dict, current=curr_cnt, detail_description=msg)

            # stage 1 is at 100%
            curr_cnt = 10
            msg = f'Currently at {curr_cnt}'
            progress_gui.update_progress(trace, app_dict, current=curr_cnt, detail_description=msg)

            # Setup stage 2
            progress_gui.update_text(trace, app_dict,
                headline_stage="Starting stage 2",
                detail_description="Now copying data...",
            )
            progress_gui.update_progress(trace, app_dict, current=0, stage_limit=15)

            # stage 2 is at 100%
            curr_cnt = 15
            msg = f'Currently at {curr_cnt}'
            progress_gui.update_progress(trace, app_dict, current=curr_cnt, detail_description=msg)
        """

        # Prevent updates after the GUI is closed.
        if not self.done:

            call_kwargs = {
                "current" : current,
            }
            self.ui_calls.put(("update_progress", call_kwargs))


    @morpy_wrap
    def _real_update_progress(self, trace: dict, app_dict: dict, current: float = None) -> None:
        """
        Update stage progress & overall progress. If overall hits 100% and auto_close=True, close window. Else,
        switch button text to "Close" and stop console redirection. Enqueues a UI request for the
        main thread to process. Safe to call from any thread. Actually updates Tk widgets. Must be called only
        from the main thread.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param current: Current progress count. If None, each call of this method will add +1
            to the progress count. Defaults to None.
        """

        reset_stage_progress = False

        try:
            # Check, if running in main thread
            check_main_thread(trace, app_dict)

            # If we're already done, just clamp visually
            if self.done:
                if self.overall_progress_on and self.overall_progress is not None:
                    self.overall_progress["value"] = 100.0
                    self.overall_label_var.set("100.00%")

                    # Enforce an update on the GUI
                    self._enforce_update()
            else:
                # 1) stage progress
                self.stage_info = self.stage_progress_tracker.update(trace, app_dict, current=current)
                self.stage_abs = self.stage_info["prog_abs"]  # Absolute float value representing 0..100%

                if self.stage_progress is not None and self.stage_abs:
                    self.stage_progress["value"] = self.stage_abs
                if self.stage_label_var is not None and self.stage_abs:
                    self.stage_label_var.set(f"{self.stage_abs:.2f}%")

                # If stage hits 100%, increment the stage count, reset stage bar
                if (self.stage_abs is not None) and self.stage_abs >= 100.0:
                    if self.overall_progress_on:
                        reset_stage_progress = True
                        self.stages_finished += 1
                    else:
                        self.stages_finished += 1
                        # If all stages are finished, mark as done
                        self.done = True
                        if self.auto_close:
                            self._stop_console_redirection(trace, app_dict)
                            self._on_close(trace, app_dict)
                        else:
                            self.button_text.set(self.button_text_close)
                            self._enforce_update()
                            self._stop_console_redirection(trace, app_dict)

                # Enforce an update on the GUI
                self._enforce_update()

                # 2) Overall fraction
                if self.overall_progress_on:
                    # Add fraction of stage to overall progress
                    overall_progress = self.stages_finished * self.fraction_per_stage
                    if (self.stage_abs is not None) and self.stage_abs < 100.0:
                        overall_progress += (self.stage_abs / 100.0) * self.fraction_per_stage

                    # Update the GUI elements for overall progress
                    self.overall_progress["value"] = overall_progress
                    self.overall_label_var.set(f"{overall_progress:.2f}%")

                    # If overall progress reaches 100%, handle completion
                    if overall_progress >= 100.0:
                        # If all stages are finished, mark as done
                        self.done = True
                        if self.auto_close:
                            self._stop_console_redirection(trace, app_dict)
                            self._on_close(trace, app_dict)
                        else:
                            self.button_text.set(self.button_text_close)
                            self._stop_console_redirection(trace, app_dict)

                        # All done for ##
                        log(trace, app_dict, "info",
                        lambda: f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_done"]} "{self.frame_title}".')

                    # Enforce an update on the GUI
                    self._enforce_update()

                # 3) Reset stage progress last to avoid lag in between update of stage and overall progress.
                if reset_stage_progress:
                    if self.stages_finished < self.stages:
                        if self.stage_progress is not None:
                            self.stage_progress["value"] = 0.0
                        if self.stage_label_var is not None:
                            self.stage_label_var.set("0.00%")
                    else:
                        # If all stages are finished, mark as done
                        self.done = True

                    # Enforce an update on the GUI
                    self._enforce_update()

            # Decrement self.unfinished_tasks
            self.ui_calls.task_done()

            # Enforce an update on the GUI
            self._enforce_update()

        # Handle errors from GUI after aborting
        except TclError as tcl_e:
            # GUI ended ungracefully.
            log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_exit_dirty"]}\n'
                    f'{type(tcl_e).__name__}: {tcl_e}')


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def update_text(self, trace: dict, app_dict: dict, headline_total: str = None, headline_stage: str = None,
                    detail_description: str = None) -> None:
        r"""
        Update the headline texts or description at runtime. Enqueues a UI request for the
        main thread to process. Safe to call from any thread.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param headline_total: If not None, sets the overall progress headline text.
        :param headline_stage: If not None, sets the stage progress headline text.
        :param detail_description: If not None, sets the description text beneath the stage headline.

        :example:
            progress_gui.update_text(trace, app_dict,
                headline_total="Processing Outer Loop 3",
                headline_stage="Processing File 5",
                detail_description="Now copying data...")
        """

        # Prevent updates after the GUI is closed.
        if not self.destroy:

            # Send text updates to the queue
            call_kwargs = {
                "headline_total" : headline_total,
                "headline_stage" : headline_stage,
                "detail_description" : detail_description,
            }
            self.ui_calls.put(("update_text", call_kwargs))
            self._enforce_update()


    @morpy_wrap
    def _real_update_text(self, trace: dict, app_dict: dict, headline_total: str = None,
                          headline_stage: str = None, detail_description: str = None) -> None:
        r"""
        Update the headline texts or description at runtime. Actually updates Tk widgets.
        Must be called only from the main thread.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        :param headline_total: If not None, sets the overall progress headline text.
        :param headline_stage: If not None, sets the stage progress headline text.
        :param detail_description: If not None, sets the description text beneath the stage headline.

        :example:
            gui.update_text(trace, app_dict,
                headline_total="Processing Outer Loop 3",
                headline_stage="Processing File 5",
                detail_description="Now copying data...")
        """

        try:
            # Avoid updates after "abort"
            if not self.done:
                # Check, if running in main thread
                check_main_thread(trace, app_dict)

                # Update overall headline
                if headline_total is not None and self.overall_progress_on:
                    # Retain the final colon to stay consistent with constructor
                    self.headline_total_no_col = headline_total
                    self.headline_total = self.headline_total_no_col + ":"
                    if hasattr(self, "overall_progress_tracker"):
                        self.overall_progress_tracker.description = self.headline_total_no_col
                    if self.total_headline_label is not None:
                        self.total_headline_label.config(text=self.headline_total)

                    # Enforce an update on the GUI
                    self._enforce_update()

                # Update stage headline
                if headline_stage is not None:
                    # Retain the final colon to stay consistent with constructor
                    self.headline_stage_no_col = headline_stage
                    self.headline_stage = self.headline_stage_no_col + ":"
                    if hasattr(self, "stage_progress_tracker"):
                        self.stage_progress_tracker.description = self.headline_stage_no_col
                    if self.stage_headline_label is not None:
                        self.stage_headline_label.config(text=self.headline_stage)

                    # Enforce an update on the GUI
                    self._enforce_update()

                # Update description
                if detail_description is not None:
                    self.detail_description = detail_description
                    # If the label didn't exist but was called, we don't create it on the fly.
                    # We only update if the widget is already present:
                    if self.stage_description_label is not None:
                        self.stage_description_label.config(text=self.detail_description)

                    # Enforce an update on the GUI
                    self._enforce_update()

        # Handle errors from GUI after aborting
        except TclError as tcl_e:
            # GUI ended ungracefully.
            log(trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_exit_dirty"]}\n'
                    f'{type(tcl_e).__name__}: {tcl_e}')


    @morpy_wrap
    def run(self, trace: dict, app_dict: dict) -> None:
        r"""
        Start the GUI main loop and run the Tk mainloop on the main thread.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :example:
            progress_gui = morPy.ProgressTrackerTk(
                trace, app_dict,
                frame_title="My Demo Progress GUI",
                detail_description="Generic Progress stage",
                stages=1,
                stage_limit=10,
                work=work
            )

            progress_gui.run(trace, app_dict)
        """

        # Start our custom loop
        self._main_loop(trace, app_dict)
        self.root.mainloop()


    @morpy_wrap
    def _start_work_thread(self, trace: dict, app_dict: dict) -> None:
        r"""
        TODO implement morPy threading and use it here
            > right now interrupt/abort does not work as desired: background threads shall be terminated immediately.

        Launch the user-supplied function in a background thread.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        def _thread_wrapper():
            try:
                # Automatically pass gui=self to the work_callable
                self.work_callable(gui=self)
            except Exception as thread_e:
                # Exception in the worker thread.
                log(trace, app_dict, "error",
                    lambda: f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_start_work_thread_err"]}\n'
                            f'{app_dict["loc"]["morpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno} '
                            f'{app_dict["loc"]["morpy"]["err_module"]} {trace["module"]}\n'
                            f'{type(thread_e).__name__}: {thread_e}')

        self.worker_thread = threading.Thread(target=_thread_wrapper, daemon=True)
        self.worker_thread.start()


    @morpy_wrap
    def _on_close(self, trace: dict, app_dict: dict) -> None:
        r"""
        Close or abort the GUI.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        # In case of aborting progress quit the program.
        if not self.done:

            # Set done to omit pulling from GUI queue after close
            self.done = True

            # Initiate global exit
            app_dict["morpy"]["exit"] = True

            # Release the global interrupts to proceed with exit
            app_dict["morpy"]["interrupt"] = False


        # Clear any pending UI update calls.
        while not self.ui_calls.empty():
            try:
                self.ui_calls.get_nowait()
            except Empty:
                break

        # Clear any pending console messages.
        if self.console_queue is not None:
            while not self.console_queue.empty():
                try:
                    self.console_queue.get_nowait()
                except Empty:
                    break

        # Finally stop any text updates
        self.destroy = True

        # Restore original console if not already done
        self._stop_console_redirection(trace, app_dict)
        self.root.quit()
        self.root.destroy()


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def get_console_output(self, trace: dict, app_dict: dict) -> dict:
        r"""
        Retrieve the current text from the console widget.

        :param trace: Operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations
        """

        console_text = ""

        if self.console_output is not None:
            console_text = self.console_output.get("1.0", tk.END).strip()

        return {
            "console_output" : console_text,
        }


# Suppress linting for mandatory arguments.
# noinspection PyUnusedLocal
@morpy_wrap
def check_main_thread(trace: dict, app_dict: dict) -> None:
    r"""
    Check, if GUI runs in main thread and raise error if so. Otherwise,
    instabilities are introduced with tkinter.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary containing app configurations
    """

    # UI must run in main thread. Current thread ###
    if threading.current_thread() is not threading.main_thread():
        raise RuntimeError(
            f'{app_dict["loc"]["morpy"]["ProgressTrackerTk_check_main"]}: {threading.current_thread()}'
        )


@morpy_wrap
def dialog_sel_file(trace: dict, app_dict: dict, init_dir: str=None, file_types: tuple=None, title: str=None) -> dict:
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

    file_path = None
    file_selected = False

    if not init_dir:
        init_dir = app_dict["morpy"]["conf"]["main_path"]
    if not file_types:
        file_types = (f'{app_dict["loc"]["morpy"]["dialog_sel_file_all_files"]}', '*.*')
    if not title:
        title = f'{app_dict["loc"]["morpy"]["dialog_sel_file_select"]}'

    # Invoke the Tkinter root window and withdraw it to force the
    # dialog to be opened in the foreground
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    root.iconbitmap(app_dict["morpy"]["conf"]["app_icon"])

    # Open the actual dialog in the foreground and store the chosen folder
    file_path = filedialog.askopenfilename(
        parent = root,
        title = f'{title}',
        initialdir = init_dir,
        filetypes = file_types,
    )

    if not file_path:
        # No file was chosen by the user.
        log(trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["dialog_sel_file_no_sel"]}\n'
                f'{app_dict["loc"]["morpy"]["dialog_sel_file_choice"]}: {app_dict["loc"]["morpy"]["dialog_sel_file_cancel"]}')

    else:
        file_selected = True
        # A file was chosen by the user.
        log(trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["dialog_sel_file_sel"]}\n'
                f'{app_dict["loc"]["morpy"]["dialog_sel_file_path"]}: {file_path}\n'
                f'{app_dict["loc"]["morpy"]["dialog_sel_file_choice"]}: {app_dict["loc"]["morpy"]["dialog_sel_file_open"]}')

        # Create a path object
        morpy_fct.pathtool(file_path)

    return{
        'file_path' : file_path,
        'file_selected' : file_selected,
        }

@morpy_wrap
def dialog_sel_dir(trace: dict, app_dict: dict, init_dir: str=None, title: str=None) -> dict:
    r"""
    This function opens a dialog for the user to select a directory.

    :param trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param title: Title of the open directory dialog

    :return: dict
        dir_path: Path of the selected directory
        dir_selected: True, if directory was selected. False, if canceled.

    :example:
        init_dir = "C:\"
        title = 'Select a directory...'
        dir_path = morPy.dialog_sel_dir(trace, app_dict, init_dir=init_dir, title=title)["dir_path"]
    """

    dir_path = None
    dir_selected = False

    if not init_dir:
        init_dir = app_dict["morpy"]["conf"]["main_path"]
    if not title:
        title = f'{app_dict["loc"]["morpy"]["dialog_sel_dir_select"]}'

    # Invoke the Tkinter root window and withdraw it to force the
    # dialog to be opened in the foreground
    root = tk.Tk()
    root.withdraw()
    root.iconbitmap(app_dict["morpy"]["conf"]["app_icon"])

    # Open the actual dialog in the foreground and store the chosen folder
    root.dir_name = filedialog.askdirectory(
        parent = root,
        title = f'{title}',
        initialdir = init_dir,
    )
    dir_path = root.dir_name

    if not dir_path:
        # No directory was chosen by the user.
        log(trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["dialog_sel_dir_no_sel"]}\n'
            f'{app_dict["loc"]["morpy"]["dialog_sel_dir_choice"]}: {app_dict["loc"]["morpy"]["dialog_sel_dir_cancel"]}')
    else:
        dir_selected = True
        # A directory was chosen by the user.
        log(trace, app_dict, "debug",
        lambda: f'{app_dict["loc"]["morpy"]["dialog_sel_dir_sel"]}\n'
                f'{app_dict["loc"]["morpy"]["dialog_sel_dir_path"]}: {dir_path}\n'
                f'{app_dict["loc"]["morpy"]["dialog_sel_dir_choice"]}: {app_dict["loc"]["morpy"]["dialog_sel_dir_open"]}')

        # Create a path object
        morpy_fct.pathtool(dir_path)

    return{
        'dir_path' : dir_path,
        'dir_selected' : dir_selected,
        }
