"""
Author:     Bastian Neuwirth
Date:       28.06.2021
Version:    0.1
Descr.:     This module is prebuilt to use the Python Productivity Suite (morPy).

TODO
[- enqueue log_db mit lock und unlock
    > Immer das Modul mit angeben mpy_msg.[...]
- enqueue log_txt mit lock und unlock
    > Immer das Modul mit angeben mpy_msg.[...]
    ]
    >>> Erstmal verworfen, um logging zeitnah zu ermöglichen
    >>> Workaround nötig

- Listen von Objekten in Klassen überführen
    > mpy_xl Workbooks
    > mpy_xl_wb Tabellen
    > mpy_xl Copy/Cut
    > mpy_ui_tk
    > webscraper
    > mpy_mt

- Localization
    > Präfix core_ für alle framework-keys hinzufügen
    > Gemeinsame Ausdrücke definieren, um das dictionary zu kürzen
        > Im Idealfall je modul, nicht global, um flexibel zu bleiben

- Anpassung wb_tbl_attributes, sodass tatsächlich nur die angefragte
    Tabelle zurückgegeben wird

- Unterscheidung Anzahl Logs/prints

- Multithreading vorbereiten
>>>ToDo:
    > verfügbare Threads erkennen
    > Threads direkt reservieren (max. von Parametern beachten)
        > Minimal verfügbare Threads für Multithreading aktivieren
        >>> Sonst Fallback auf morPy Thread
    > Nutzung max. Anz. Threads vorbereiten (z.b. max 75%)
        > Am besten mit einer Reservierung im Betriebssystem
    > ERSTEN FREIEN Thread für morPy reservieren
        > Vermutlich wird eine queue für morPy Thread notwendig
        > Dadurch kann auch ein Stau entstehen
        >>> Workauround durch Rückmeldung von Task 1, dass logging fertig
        >>> Erst dann darf der aufrufende Thread weiter arbeiten
    > Restliche Threads werden durchlaufen (cycle through) von
        morPy Thread +1 bis letzten Thread

- Pfadbäume lesen und auswerten
    > Ausbau zu Toll für
        1) Recursive tree exploration
        2) Tree traversal in a node

- Webscraper.py
   > Debugging der Antwort: Warum ist jeder request 'None'
   + Ping-Routine entwickeln, für die Überprüfung am Anfang eines requests
   + HTML-Response codes dictionary anlegen

- mpy_fct.privileges_handler
    > Debugging der Adminrechte-funktion

- Paketkompilierung zu .exe und linux-shell (siehe Forks)

- raise SystemExit wenn CRITICAL

- Review/ToDo mpy_fct.perfinfo()

"""

if __name__ == '__main__':

#   Import standard modules only
    import sys, os, pathlib

#   Add the project specific module library to sys.path
    lib_path = os.path.join(pathlib.Path(__file__).parent.resolve(),'lib')
    sys.path.append(lib_path)

#   Add the path for the localized dictionaries
    loc_path = os.path.join(pathlib.Path(__file__).parent.resolve(),'loc')
    sys.path.append(loc_path)

#   Import morPy modules
    import mpy_init, mpy_exit

#   Initialize the morPy tracing dictionary
    mpy_trace = mpy_init.init_cred()

#   Initialize the globally used project dictionary
    global prj_dict
    prj_dict = mpy_init.init(mpy_trace)

    """--------------------------------------------------
            >>> YOUR PROGRAM STARTS HERE <<<

        This section is only meant to execute modules.
        Optionally, it may be executed with the multi-
        processing capabilities of morPy.
    --------------------------------------------------"""

#   Import project modules
    import debug

    """ >>> DEBUGGING <<< """
    debug.dbg(mpy_trace, prj_dict)

    """--------------------------------------------------
            >>> YOUR PROGRAM ENDS HERE <<<
    --------------------------------------------------"""

#   Executing the morPy exit routine
    mpy_exit.exit(mpy_trace, prj_dict)