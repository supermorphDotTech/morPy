r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module defines custom exceptions for the morPy framework.
"""

from lib.decorators import log

import sys

class MorPyException(Exception):
    r"""
    This wraps errors in the standard morPy fashion. If one of the arguments
    required for logging is missing, this wrapper will raise other errors in
    order to reduce tracebacks and specifically point to the issue at hand.
    """

    __slots__ = ['morpy_trace', 'app_dict', 'log_level', 'line', 'module', 'e']

    def __init__(self, morpy_trace: dict, app_dict: dict, exception_obj: BaseException, line: int,
                 log_level: str, message: str=None) -> None:
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

        try:
            # Use .get() with default values to prevent KeyErrors
            loc = app_dict.get("loc", {}).get("morpy", {}) if app_dict else {}
            err_line = loc.get("err_line", "Line unknown")
            err_module = loc.get("err_module", "Module unknown")
            module = morpy_trace.get("module", "Module unknown") if morpy_trace else "Module unknown"

            # Safely extract current line number; if not available, use provided line
            tb = sys.exc_info()[2]
            current_line = tb.tb_lineno if tb else line

            # Mitigate recursion issues and duplicate errors
            if isinstance(exception_obj, MorPyException):
                return
            else:
                # Build the core message of the original error
                self.core_msg = (
                    f"{err_line} {current_line} {err_module} '{module}'\n"
                    f"{type(exception_obj).__name__}: {exception_obj}"
                )

            # Build the final message
            if message:
                message = f'\n{message}'
                self.message = f'{self.core_msg}\n{message}'
            else:
                self.message = f'{self.core_msg}'

            log(morpy_trace, app_dict, log_level, lambda: self.message)

        except Exception as crit_e:

            # Raise critical error in hierarchical order
            if not app_dict:
                cause = "app_dict"
                logging = False
            elif not morpy_trace:
                cause = "morpy_trace"
                logging = True
            elif not log_level:
                cause = "log_level"
                logging = True
            elif not line:
                cause = "line"
                logging = True
            elif not exception:
                cause = "module"
                logging = True
            else:
                cause = "UNKNOWN"
                logging = False

            raise MorPyCoreError(
                app_dict=app_dict,
                exc=crit_e,
                root_line=line,
                root_e=exception,
                root_trace=morpy_trace,
                logging=logging,
                cause=cause
            )

class MorPyCoreError(Exception):
    r"""
    This error is raised whenever MorPyException fails to generate and log an error
    as intended. This error will reduce the amount of tracebacks to the most
    useful messages required for troubleshooting.

    :param exc: Exception object as passed by sys of the parent function/method.
    :param root_line: Line number of the original error that could not be logged.
    :param root_e: Exception object of the original error that could not be logged.
    :param root_trace: Operation credentials and tracing information of the original caller.
    :param logging: If True, logging is enabled. May lead to RecursionError.
    :param cause: Additional message specifying the issue.
    """

    __slots__ = ['exc', '__suppress_context__', 'root_msg', 'core_msg', 'message']

    def __init__(self, app_dict: dict=None, exc: BaseException=None, root_line: int=None, root_e: BaseException=None,
                 root_trace: dict=None, logging: bool=False, cause: str=None) -> None:

        # Assignments and preparation
        self.exc = exc
        current_line = root_line if root_line else None

        loc_info = "" if logging else " Localization not available."
        self.core_msg = (
            f"Line {current_line} in module lib.exceptions identified as '{type(self.exc).__name__}'\n"
            f"CRITICAL. Missing argument '{cause}' in error call. Logging of error failed.{loc_info}"
        )

        module = root_trace.get("module", None) if root_trace else None
        self.root_msg = (
            f"Root error:\n    > Line {root_line} in module '{module}'\n"
            f"    > {type(root_e).__name__}: {root_e}"
        )
        self.message = f"{self.core_msg}\n{self.root_msg}"

        if logging:
            log(root_trace, app_dict, "critical", lambda: self.message)
        else:
            # Suppress traceback for clarity
            self.__suppress_context__: bool = True
            sys.tracebacklimit = 0
            super().__init__(self.message)

        print(self.message)

        # Quit the program
        sys.exit(-1)
