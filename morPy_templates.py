r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION

Annotations:
    #TODO
    #FIXME
"""

import lib.mpy as mpy
import sys

from lib.decorators import metrics, log

@metrics
def template(morPy_trace: dict, app_dict: dict) -> dict:

    r"""
    This function is a template.

    :param morPy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        morPy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        template(morPy_trace, app_dict)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module = 'morPy_templates'
    operation = 'template(~)'
    morPy_trace = morPy.tracing(module, operation, morPy_trace)

    # OPTION enable/disable logging
    # ??? morPy_trace["log_enable"] = False

    check = False

    try:
        # LOCALIZED_MESSAGE
        log(morPy_trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["app"]["LOCALIZED_MESSAGE"]}')

        # TODO: MY CODE

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace,
        'check' : check,
        }

class cl_template:
    r"""
    This class is a template.
    """

    def __init__(self, morPy_trace: dict, app_dict: dict) -> None:
        r"""
        In order to get metrics for __init__(), call helper method _init() for
        the @metrics decorator to work. It relies on the returned
        {'morPy_trace' : morPy_trace}, which __init__() can not do (needs to be None).

        :param morPy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return:
            -

        :example:
            instance = cl_template(morPy_trace, app_dict)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module = 'morPy_templates'
        operation = 'cl_template.__init__(~)'
        morPy_trace = morPy.tracing(module, operation, morPy_trace)

        # OPTION enable/disable logging
        # ??? morPy_trace["log_enable"] = False

        try:
            # Use self._init() for initialization
            self._init(morPy_trace, app_dict)

        except Exception as e:
            log(morPy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{type(e).__name__}: {e}')

    @metrics
    def _init(self, morPy_trace: dict, app_dict: dict) -> dict:
        r"""
        Helper method for initialization to ensure @metrics decorator usage.

        :param morPy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morPy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self._init(morPy_trace, app_dict)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module = 'morPy_templates'
        operation = 'cl_template._init(~)'
        morPy_trace = morPy.tracing(module, operation, morPy_trace)

        # OPTION enable/disable logging
        # ??? morPy_trace["log_enable"] = False

        check = False

        try:
            # TODO: MY INSTANCE INITIALIZATION
            # LOCALIZED_MESSAGE
            log(morPy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["app"]["LOCALIZED_MESSAGE"]}')

            check = True

        except Exception as e:
            log(morPy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{type(e).__name__}: {e}')

        return{
            'morPy_trace' : morPy_trace,
            'check' : check,
            }

    @metrics
    def method(self, morPy_trace: dict, app_dict: dict) -> dict:
        r"""
        :param morPy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morPy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self.method(morPy_trace, app_dict)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module = 'morPy_templates'
        operation = 'cl_template.method(~)'
        morPy_trace = morPy.tracing(module, operation, morPy_trace)

        # OPTION enable/disable logging
        # ??? morPy_trace["log_enable"] = False

        check = False

        try:
            # TODO: MY CLASS METHOD
            # LOCALIZED_MESSAGE
            log(morPy_trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["app"]["LOCALIZED_MESSAGE"]}')

            check = True

        except Exception as e:
            log(morPy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{type(e).__name__}: {e}')

        return{
            'morPy_trace' : morPy_trace,
            'check' : check,
            }