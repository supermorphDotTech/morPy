r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION

Annotations:
    #TODO
    #FIXME
"""

import morPy
from lib.decorators import metrics, log

import sys

@metrics
def template(morpy_trace: dict, app_dict: dict) -> dict:
    r"""
    This function is a template.

    :param morpy_trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        morpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors

    :example:
        template(morpy_trace, app_dict)
    """

    # morPy credentials (see init.init_cred() for all dict keys)
    module: str = 'app.my_module'
    operation: str = 'template(~)'
    morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

    # OPTION enable/disable logging
    # ??? morpy_trace["log_enable"] = False

    check: bool = False

    try:
        """
        >>> MY CODE
        """

        # LOCALIZED_MESSAGE
        log(morpy_trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["app"]["LOCALIZED_MESSAGE"]}')

        check: bool = True

    except Exception as e:
        raise morPy.MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    return{
        'morpy_trace' : morpy_trace,
        'check' : check,
        }

class TemplateClass:
    r"""
    This class is a template.

    !! LIMITATIONS IN MULTIPROCESSING !!
    Storing classes in `app_dict` to share them across processes may fail, because it's attributes
    are not propagated reliably to other processes. See README.md for more details.
    """

    def __init__(self, morpy_trace: dict, app_dict: dict) -> None:
        r"""
        In order to get metrics for __init__(), call helper method _init() for
        the @metrics decorator to work. It relies on the returned
        {'morpy_trace' : morpy_trace}, which __init__() can not do (needs to be None).

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return:
            -

        :example:
            instance = TemplateClass(morpy_trace, app_dict)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module: str = 'app.my_module'
        operation: str = 'TemplateClass.__init__(~)'
        morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

        # OPTION enable/disable logging
        # ??? morpy_trace["log_enable"] = False

        try:
            # Use self._init() for initialization
            self._init(morpy_trace, app_dict)

        except Exception as e:
            raise morPy.MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

    @metrics
    def _init(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        Helper method for initialization to ensure @metrics decorator usage.

        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self._init(morpy_trace, app_dict)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module: str = 'app.my_module'
        operation: str = 'TemplateClass._init(~)'
        morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

        # OPTION enable/disable logging
        # ??? morpy_trace["log_enable"] = False

        check: bool = False

        try:
            """
            >>> MY INSTANCE INITIALIZATION
            """

            # LOCALIZED_MESSAGE
            log(morpy_trace, app_dict, "debug",
            lambda: f'{app_dict["loc"]["app"]["LOCALIZED_MESSAGE"]}')

            check: bool = True

        except Exception as e:
            raise morPy.MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            }

    @metrics
    def method(self, morpy_trace: dict, app_dict: dict) -> dict:
        r"""
        :param morpy_trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: dict
            morpy_trace: Operation credentials and tracing
            check: Indicates whether the function ended without errors

        :example:
            self.method(morpy_trace, app_dict)
        """

        # morPy credentials (see init.init_cred() for all dict keys)
        module: str = 'app.my_module'
        operation: str = 'TemplateClass.method(~)'
        morpy_trace: dict = morPy.tracing(module, operation, morpy_trace)

        # OPTION enable/disable logging
        # ??? morpy_trace["log_enable"] = False

        check: bool = False

        try:
            """
            >>> MY CLASS METHOD
            """

            # LOCALIZED_MESSAGE
            log(morpy_trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["app"]["LOCALIZED_MESSAGE"]}')

            check: bool = True

        except Exception as e:
            raise morPy.MorPyException(morpy_trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "error")

        return{
            'morpy_trace' : morpy_trace,
            'check' : check,
            }