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

from lib.mpy_decorators import metrics, log

@metrics
def template(mpy_trace: dict, app_dict: dict) -> dict:

    r"""
    This function is a template.

    :param mpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        mpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        template(mpy_trace, app_dict)
    """

    # morPy credentials (see mpy_init.init_cred() for all dict keys)
    module = 'morPy_templates'
    operation = 'template(~)'
    mpy_trace = mpy.tracing(module, operation, mpy_trace)

    # OPTION enable/disable logging
    # ??? mpy_trace["log_enable"] = False

    check = False

    try:
        # LOCALIZED_MESSAGE
        log(mpy_trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["app"]["LOCALIZED_MESSAGE"]}')

        # TODO: MY CODE

        check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        }

class cl_template:
    r"""
    This class is a template.
    """

    def __init__(self, mpy_trace: dict, app_dict: dict) -> None:
        r"""
        In order to get metrics for __init__(), call helper method _init() for
        the @metrics decorator to work. It relies on the returned
        {'mpy_trace' : mpy_trace}, which __init__() can not do (needs to be None).

        :param mpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return:
            -

        :example:
            instance = cl_template(mpy_trace, app_dict)
        """

        # morPy credentials (see mpy_init.init_cred() for all dict keys)
        module = 'morPy_templates'
        operation = 'cl_template.__init__(~)'
        mpy_trace = mpy.tracing(module, operation, mpy_trace)

        # OPTION enable/disable logging
        # ??? mpy_trace["log_enable"] = False

        try:
            # Use self._init() for initialization
            self._init(mpy_trace, app_dict)

        except Exception as e:
            log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    @metrics
    def _init(self, mpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Helper method for initialization to ensure @metrics decorator usage.

        :param mpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            mpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self._init(mpy_trace, app_dict)
        """

        # morPy credentials (see mpy_init.init_cred() for all dict keys)
        module = 'morPy_templates'
        operation = 'cl_template._init(~)'
        mpy_trace = mpy.tracing(module, operation, mpy_trace)

        # OPTION enable/disable logging
        # ??? mpy_trace["log_enable"] = False

        check = False

        try:
            # TODO: MY INSTANCE INITIALIZATION
            # LOCALIZED_MESSAGE
            log(mpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["app"]["LOCALIZED_MESSAGE"]}')

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
    def method(self, mpy_trace: dict, app_dict: dict) -> dict:
        r"""
        :param mpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            mpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self.method(mpy_trace, app_dict)
        """

        # morPy credentials (see mpy_init.init_cred() for all dict keys)
        module = 'morPy_templates'
        operation = 'cl_template.method(~)'
        mpy_trace = mpy.tracing(module, operation, mpy_trace)

        # OPTION enable/disable logging
        # ??? mpy_trace["log_enable"] = False

        check = False

        try:
            # TODO: MY CLASS METHOD
            # LOCALIZED_MESSAGE
            log(mpy_trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["app"]["LOCALIZED_MESSAGE"]}')

            check = True

        except Exception as e:
            log(mpy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                    f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

        return{
            'mpy_trace' : mpy_trace,
            'check' : check,
            }