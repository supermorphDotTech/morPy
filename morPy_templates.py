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
    This is a template function intended for demonstration purposes. It serves as a
    starting point for creating new morPy operations. Replace the inner placeholder
    code with your actual implementation.

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
    This template class is provided as an example. Note that storing class definitions
    in the global app configuration for sharing across processes may not propagate attributes
    reliably (see README.md for details).
    """

    def __init__(self, morpy_trace: dict, app_dict: dict) -> None:
        r"""
<<<<<<< Updated upstream
        In order to get metrics for __init__(), call helper method _init() for
        the @metrics decorator to work. It relies on the returned
        {'morpy_trace' : morpy_trace}, which __init__() can not do (needs to be None).
=======
        Initializes the TemplateClass instance using tracing and the morPy global
        configuration. This constructor logs an informational message and includes
        placeholder code for further initialization.
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
        Helper method for initialization to ensure @metrics decorator usage.
=======
        Example method of the TemplateClass. It logs an informational message and is intended
        as a placeholder for actual class functionality.
>>>>>>> Stashed changes

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