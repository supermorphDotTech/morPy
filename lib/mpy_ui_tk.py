r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module provides UI-building functions using the TKinter
            libraries.

ToDo:       - GUI Instanz im app_dict anmelden
                > Referenzierung durch Unterprogramme ermöglichen
                > Bei Error, Critical oder sonstige das Fenster schließen
                > Bei Exit-Routine schließen
"""

import lib.mpy_fct as mpy_fct
import lib.mpy_common as mpy_common
from lib.mpy_decorators import metrics, log

import sys
import queue
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class progress_2bars_console:
    r"""
    This class instantiates a GUI window with tkinter. It shows a headline, an overall
    progress, a step progress and console output.
    """

    def __init__(self, mpy_trace: dict, app_dict: dict, frame_title: str=None, frame_width: int=None, frame_height: int=None,
              headline: str=None, headline_font_size: int=None, font: str=None, steps: int=None, step_total: int=None):
        """
        In order to get metrics for __init__(), call helper method _init() for
        the @metrics decorator to work. It relies on the returned
        {'mpy_trace' : mpy_trace}, which __init__() can not do (needs to be None).


        :param mpy_trace: Operation credentials and tracing.
        :param app_dict: The mpy-specific global dictionary.
        :param frame_title: Title of the GUI (window).
        :param frame_width: Width of the GUI (window). Defaults to 800.
        :param frame_height: Height of the GUI (window). Defaults to 600.
        :param headline: Headline of the first step (not overall progress).
        :param headline_font_size: Font size of the step headline. Defaults to 14.
        :param font: Font of the text in this GUI. Defaults to Arial.
        :param steps: Total amount of steps to be progress tracked. This number represents 100% of total progress.
        :param step_total: The step total count reflecting 100.00% progress.

        :return:
            -

        :example:
            progress = progress_2bars_console(mpy_trace, app_dict,
                frame_title="My App Progress",
                headline="Current Step Progress",
                font="Calibri",
                steps=12)
        """

        # morPy credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_ui_tk'
        operation = 'progress_2bars_console.__init__(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        try:
            # Use self._init() for initialization
            self._init(mpy_trace, app_dict, frame_title=frame_title, frame_width=frame_width, frame_height=frame_height,
                       headline=headline, headline_font_size=headline_font_size, font=font, steps=steps,
                       step_total=step_total)

        except Exception as e:
            log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    @metrics
    def _init(self, mpy_trace: dict, app_dict: dict, frame_title: str=None, frame_width: int=None, frame_height: int=None,
              headline: str=None, headline_font_size: int=None, font: str=None, steps: int=None, step_total: int=None):
        """
        Initializes the progress bar GUI.

        :param mpy_trace: Operation credentials and tracing.
        :param app_dict: The mpy-specific global dictionary.
        :param frame_title: Title of the GUI (window).
        :param frame_width: Width of the GUI (window). Defaults to 800.
        :param frame_height: Height of the GUI (window). Defaults to 600.
        :param headline: Headline of the first step (not overall progress).
        :param headline_font_size: Font size of the step headline. Defaults to 14.
        :param font: Font of the text in this GUI. Defaults to Arial.
        :param steps: Total amount of steps to be progress tracked. This number represents 100% of total progress.
        :param step_total: The step total count reflecting 100.00% progress.

        :return: dict
            mpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            progress = progress_2bars_console(mpy_trace, app_dict,
                frame_title="My App Progress",
                headline="Current Step Progress",
                font="Calibri",
                steps=12)
        """

        # morPy credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_ui_tk'
        operation = 'progress_2bars_console._init(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        check = False

        try:
            # Set defaults
            self.frame_title = frame_title if frame_title is not None else app_dict["loc"]["mpy"]["progress_2bars_console_prog"]
            self.frame_width = 800 if not frame_width else frame_width
            self.frame_height = 600 if not frame_height else frame_height
            self.headline = f'{app_dict["loc"]["mpy"]["progress_2bars_console_curr"]}' if not headline else headline
            self.headline_font_size = 14 if not headline_font_size else headline_font_size
            self.font = "Arial" if not font else font
            self.steps = steps if steps is not None else 100
            self.step_total = step_total if step_total is not None else 100
            self.steps_finished = 0 # Counts steps finished to calculate overall progress
            self.overall_progress_abs = 0
            self.finished = False # Is True, once overall progress reaches 100%

            # Setup overall progress tracker
            self.overall_progress_tracker = mpy_common.cl_progress(mpy_trace, app_dict, description=frame_title,
                total=steps, ticks=.01)

            # Setup step progress tracker
            self.step_progress_tracker = mpy_common.cl_progress(mpy_trace, app_dict, description=headline,
                total=step_total, ticks=.01)

            # Construct a queue for console messages
            self.console_queue = queue.Queue()

            self.root = tk.Tk()
            self.root.iconbitmap(app_dict["conf"]["app_icon"])
            self.root.title(frame_title)
            self.root.geometry(f'{frame_width}x{frame_height}')

            self._create_widgets(mpy_trace, app_dict)
            self._redirect_console_output(mpy_trace, app_dict)

            check = True

        except Exception as e:
            log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

        return{
            'mpy_trace' : mpy_trace,
            'check' : check,
            }

    @metrics
    def _create_widgets(self, mpy_trace: dict, app_dict: dict):
        r"""
        Creates and places widgets in the window.

        :param mpy_trace: Operation credentials and tracing.
        :param app_dict: The mpy-specific global dictionary.

        :return: dict
            mpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self._create_widgets(mpy_trace, app_dict)
        """

        # morPy credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_ui_tk'
        operation = 'progress_2bars_console._create_widgets(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        check = False

        try:
            # Headline label
            self.headline_label = tk.Label(
                self.root,
                text=self.headline,
                font=(self.font, self.headline_font_size)
            )
            self.headline_label.pack(pady=5)

            # Overall progress bar
            self.overall_progress = ttk.Progressbar(
                self.root,
                orient=tk.HORIZONTAL,
                length=self.frame_width * 0.8,
                mode="determinate"
            )
            self.overall_progress.pack(pady=20)

            # Step progress bar
            self.step_progress = ttk.Progressbar(
                self.root,
                orient=tk.HORIZONTAL,
                length=self.frame_width * 0.8,
                mode="determinate"
            )
            self.step_progress.pack(pady=20)

            # Console output display
            self.console_output = tk.Text(self.root, height=10, wrap="word")
            self.console_output.pack(pady=5, fill=tk.BOTH, expand=True)

            # Close button
            self.close_button = tk.Button(self.root, text="Close", command=lambda: self._on_close(mpy_trace, app_dict))
            self.close_button.pack(pady=5)

            check = True

        except Exception as e:
            log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

        return{
            'mpy_trace' : mpy_trace,
            'check' : check,
            }

    @metrics
    def _redirect_console_output(self, mpy_trace: dict, app_dict: dict):
        r"""
        Redirects console output to the text widget.

        :param mpy_trace: Operation credentials and tracing.
        :param app_dict: The mpy-specific global dictionary.

        :return: dict
            mpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self._redirect_console_output(mpy_trace, app_dict)
        """

        # morPy credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_ui_tk'
        operation = 'progress_2bars_console._redirect_console_output(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        check = False

        try:
            sys.stdout = self
            sys.stderr = self

            check = True

        except Exception as e:
            log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

        return{
            'mpy_trace' : mpy_trace,
            'check' : check,
            }

    @metrics
    def write(self, mpy_trace: dict, app_dict: dict, message: str):
        r"""
        Writes console output to the text widget.

        :param mpy_trace: Operation credentials and tracing.
        :param app_dict: The mpy-specific global dictionary.
        :param message: Message to be displayed in the console frame.

        :return: dict
            mpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            message = "Hello World!"
            self.write(mpy_trace, app_dict, message)
        """

        # morPy credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_ui_tk'
        operation = 'progress_2bars_console.write(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        check = False

        try:
            self.console_queue.put(message)

            check = True

        except Exception as e:
            log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

        return{
            'mpy_trace' : mpy_trace,
            'check' : check,
            }

    @metrics
    def flush(self, mpy_trace: dict, app_dict: dict):
        r"""
        Required for stdout redirection.

        :param mpy_trace: Operation credentials and tracing.
        :param app_dict: The mpy-specific global dictionary.

        :return: dict
            mpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self.flush(mpy_trace, app_dict)
        """

        # morPy credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_ui_tk'
        operation = 'progress_2bars_console.flush(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        check = False

        try:
            check = True

        except Exception as e:
            log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

        return{
            'mpy_trace' : mpy_trace,
            'check' : check,
            }

    @metrics
    def _update_console(self, mpy_trace: dict, app_dict: dict):
        r"""
        Updates the console output in the text widget periodically.

        :param mpy_trace: Operation credentials and tracing.
        :param app_dict: The mpy-specific global dictionary.

        :return: dict
            mpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self._update_console(mpy_trace, app_dict)
        """

        # morPy credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_ui_tk'
        operation = 'progress_2bars_console._update_console(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        check = False

        try:
            if not self.console_queue.empty():
                message = self.console_queue.get_nowait()
                self.console_output.insert(tk.END, message)
                self.console_output.see(tk.END)
            self.root.after(100, lambda: self._update_console(mpy_trace, app_dict))

            check = True

        except Exception as e:
            log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

        return{
            'mpy_trace' : mpy_trace,
            'check' : check,
            }

    @metrics
    def update_progress(self, mpy_trace: dict, app_dict: dict, current: float=None):
        r"""
        Updates the progress bars from cl_progress instance.

        :param mpy_trace: Operation credentials and tracing.
        :param app_dict: The mpy-specific global dictionary.
        :param current: Current progress count. If None, each call of this method will add +1
            to the progress count.

        :return: dict
            mpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self.update_progress(mpy_trace, app_dict)
        """

        # morPy credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_ui_tk'
        operation = 'progress_2bars_console.update_progress(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        check = False

        try:
            step_progress = self.step_progress_tracker.update(mpy_trace, app_dict, current=current)
            step_progress_abs = step_progress["prog_abs"]
            step_progress_rel = step_progress["prog_rel"]

            # Evaluate step progression/finish
            if step_progress_abs >= 100:
                self.steps_finished += 1
                self.overall_progress_abs = round((self.steps_finished / self.steps) * 100, 2)
                current_overall = self.steps_finished
            else:
                current_overall = self.steps_finished + (step_progress_rel / self.steps)

            # Reflect step progress in overall progress
            overall_progress = self.overall_progress_tracker.update(mpy_trace, app_dict,
                current=current_overall)["prog_abs"]

            self.overall_progress["value"] = overall_progress
            self.step_progress["value"] = step_progress_abs

            self.root.after(500, self.update_progress(mpy_trace, app_dict))

            if self.overall_progress_abs >= 100:
                self._on_close(mpy_trace, app_dict)

            check = True

        except Exception as e:
            log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

        return{
            'mpy_trace' : mpy_trace,
            'check' : check,
            }

    @metrics
    def run(self, mpy_trace: dict, app_dict: dict):
        r"""
        Starts the GUI loop and periodic updates.

        :param mpy_trace: Operation credentials and tracing.
        :param app_dict: The mpy-specific global dictionary.

        :return: dict
            mpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self.run(mpy_trace, app_dict)
        """

        # morPy credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_ui_tk'
        operation = 'progress_2bars_console.run(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        check = False

        try:
            self.update_progress(mpy_trace, app_dict)
            self._update_console(mpy_trace, app_dict)
            self.root.mainloop()

            check = True

        except Exception as e:
            log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

        return{
            'mpy_trace' : mpy_trace,
            'check' : check,
            }

    @metrics
    def _on_close(self, mpy_trace: dict, app_dict: dict):
        r"""
        Handles window closure and restores console output.

        :param mpy_trace: Operation credentials and tracing.
        :param app_dict: The mpy-specific global dictionary.

        :return: dict
            mpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self.run(mpy_trace, app_dict)
        """

        # morPy credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_ui_tk'
        operation = 'progress_2bars_console._on_close(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        check = False

        try:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            self.root.quit()
            self.root.destroy()

            check = True

        except Exception as e:
            log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

        return{
            'mpy_trace' : mpy_trace,
            'check' : check,
            }

    @metrics
    def get_console_output(self, mpy_trace: dict, app_dict: dict):
        r"""
        Returns the captured console output.

        :param mpy_trace: Operation credentials and tracing.
        :param app_dict: The mpy-specific global dictionary.

        :return: dict
            mpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors
            console_output: captured console output

        :example:
            console_output = self.get_console_output(mpy_trace, app_dict)["console_output"]
        """

        # morPy credentials (see mpy_init.init_cred() for all dict keys)
        module = 'mpy_ui_tk'
        operation = 'progress_2bars_console.get_console_output(~)'
        mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

        check = False
        console_output = None

        try:
            console_output = self.console_output.get("1.0", tk.END).strip()

            check = True

        except Exception as e:
            log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

        return{
            'mpy_trace' : mpy_trace,
            'check' : check,
            'console_output' : console_output,
            }

@metrics
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
        mpy_trace: operation credentials and tracing
        check: The function ended with no errors and a file was chosen
        file_path: Path of the selected file
        file_selected: True, if file was selected. False, if canceled.

    :example:
        init_dir = "C:\"
        ftypes = (('PDF','*.pdf'),('Textfile','*.txt'),('All Files','*.*'))
        title = 'Select a file...'
        file_path = mpy.dialog_sel_file(mpy_trace, app_dict, init_dir, ftypes, title)["file_path"]
    """

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_ui_tk'
    operation = 'dialog_sel_file(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    check = False
    file_path = None
    file_selected = False

    try:
        if not init_dir:
            init_dir = app_dict["conf"]["main_path"]
        if not ftypes:
            ftypes = (f'{app_dict["loc"]["mpy"]["dialog_sel_file_all_files"]}','*.*')
        if not title:
            title = f'{app_dict["loc"]["mpy"]["dialog_sel_file_select"]}'

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
            log(mpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["mpy"]["dialog_sel_file_nosel"]}\n'
                    f'{app_dict["loc"]["mpy"]["dialog_sel_file_choice"]}: {app_dict["loc"]["mpy"]["dialog_sel_file_cancel"]}')

        else:
            file_selected = True
            # A file was chosen by the user.
            log(mpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["mpy"]["dialog_sel_file_asel"]}\n'
                    f'{app_dict["loc"]["mpy"]["dialog_sel_file_path"]}: {file_path}\n'
                    f'{app_dict["loc"]["mpy"]["dialog_sel_file_choice"]}: {app_dict["loc"]["mpy"]["dialog_sel_file_open"]}')

            # Create a path object
            mpy_fct.pathtool(mpy_trace, file_path)

        check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        'file_path' : file_path,
        'file_selected' : file_selected,
        }

@metrics
def dialog_sel_dir(mpy_trace: dict, app_dict: dict, init_dir: str=None, title: str=None) -> dict:

    r"""
    This function opens a dialog for the user to select a directory.

    :param mpy_trace: operation credentials and tracing
    :param app_dict: morPy global dictionary
    :param init_dir: The directory in which the dialog will initially be opened
    :param title: Title of the open directory dialog

    :return: dict
        mpy_trace: operation credentials and tracing
        check: The function ended with no errors and a file was chosen
        dir_path: Path of the selected directory
        dir_selected: True, if directory was selected. False, if canceled.

    :example:
        init_dir = "C:\"
        title = 'Select a directory...'
        dir_path = mpy.dialog_sel_dir(mpy_trace, app_dict, init_dir, title)["dir_path"]
    """

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_ui_tk'
    operation = 'dialog_sel_dir(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    check = False
    dir_path = None
    dir_selected = False

    try:
        if not init_dir:
            init_dir = app_dict["conf"]["main_path"]
        if not title:
            title = f'{app_dict["loc"]["mpy"]["dialog_sel_dir_select"]}'

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
            log(mpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["mpy"]["dialog_sel_dir_nosel"]}\n'
                f'{app_dict["loc"]["mpy"]["dialog_sel_dir_choice"]}: {app_dict["loc"]["mpy"]["dialog_sel_dir_cancel"]}')
        else:
            dir_selected = True
            # A directory was chosen by the user.
            log(mpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["mpy"]["dialog_sel_dir_asel"]}\n'
                    f'{app_dict["loc"]["mpy"]["dialog_sel_dir_path"]}: {dir_path}\n'
                    f'{app_dict["loc"]["mpy"]["dialog_sel_dir_choice"]}: {app_dict["loc"]["mpy"]["dialog_sel_dir_open"]}')

            # Create a path object
            mpy_fct.pathtool(mpy_trace, dir_path)

        check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        'dir_path' : dir_path,
        'dir_selected' : dir_selected,
        }