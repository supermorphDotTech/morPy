"""
Author:     Bastian Neuwirth
Date:       13.05.2022
Version:    0.1
Descr.:     This module provides UI-building functions using the TKinter
            libraries.

Ideen:      - Organisation wie folgt:
                main_window() > oberste Ebene, hierin wird sämtlicher code ausgeführt
                elmt_console > Füge Consolenfenster dem Hauptfenster hinzu
                execution > Führe code aus (z.B. Statusmeldungen)
                elmt_load_bar > Füge Ladebalken hinzu
                elmt_load_clock
                >>> Umsetzung mit Klassen

ToDo:       - GUI Instanz im prj_dict anmelden
                > Referenzierung durch Unterprogramme ermöglichen
                > Bei Error, Critical oder sonstige das Fenster schließen
                > Bei Exit-Routine schließen
            - Mit Klassen arbeiten an Stelle eines GUI_dict
                > leichteres modifizieren und instanzieren
            - Fenster schließen funktioniert noch nicht richtig
"""

import tkinter as Tk
from tkinter import *
from tkinter import ttk

def tk_progbar_indeterminate(mpy_trace, prj_dict, GUI_dict):

    """ This function invokes a window with an indeterminate progress bar
        and status messages.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - The mpy-specific global dictionary
        GUI_dict - Dictionary holding all needed parameters:

            GUI_dict = {'frame_title' : 'TITLE' , \
                        'frame_width' : 450 , \
                        'frame_height' : 300 , \
                        'headline_txt' : 'HEADLINE' , \
                        'headline_font_size' : 35 , \
                        'status_font_size' : 25
                        }

    :return - dictionary
        check - The function ended with no errors and a file was chosen
        
    #TODO
        - Use a decorator
        - Debug
        - Avoid import *, to enable checks for import
    """

    import mpy_fct, mpy_msg, mpy_common
    import sys

#   Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_ui_tk'
    operation = 'tk_progbar_indeterminate(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

#   Preparing parameters
    check = False
    frame_title = f'{GUI_dict["frame_title"]}'
    frame_width = f'{GUI_dict["frame_width"]}'
    frame_height = f'{GUI_dict["frame_height"]}'
    headline_txt = f'{GUI_dict["headline_txt"]}'
    headline_font_size = f'{GUI_dict["headline_font_size"]}'
    status_font_size = f'{GUI_dict["status_font_size"]}'
    pbar_length = f'{int(float(frame_width)*0.8)}'

    try:

    #   Invoke GUI
        root = Tk()

    #   Headline on top of the progress bar
        label = Label(root, text = headline_txt, font = headline_font_size)
        label.pack(pady=5)

    #   Draw progress bar
        progbar = ttk.Progressbar(root, orient=HORIZONTAL, length=pbar_length, mode="indeterminate")
        progbar.pack(pady=20)
        progbar.start()

        root.geometry(frame_width + 'x' + frame_height)
        root.title(frame_title)

        """
        YOUR CODE DOWN BELOW

        All logs will show up in the status text below the progress bar.
        """

    #   Open a dialog to select a file
        init_dir = prj_dict["prj_path"]
        ftypes = (('All Files','*.*'),('Text Files','*.txt'))
        file = mpy_common.dialog_sel_file(mpy_trace, prj_dict, init_dir, ftypes, title)["sel_file"]
        mpy_fct.testprint(mpy_trace, f'{file}')

        status = Label(root, text = file, font = status_font_size)
        status.pack(pady=5)
        status.config(text = file)

    #   Open a dialog to select a directory
        init_dir = prj_dict["prj_path"]
        directory = mpy_common.dialog_sel_dir(mpy_trace, prj_dict, init_dir, title)["sel_dir"]
        mpy_fct.testprint(mpy_trace, f'{directory}')

        status.config(text = directory)

        """
        YOUR CODE UP TOP

        The window will be closed once all code is executed.
        """

    #   Close window and exit the loop
        root.destroy
        root.mainloop()

        check = True

#   Error detection
    except Exception as e:
        log_message = (f'{prj_dict["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                      f'{prj_dict["err_excp"]}: {e}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

    return{
        'check' : check
        }