r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION

Annotations:
    TODO
    FIXME
"""

import morPy
from lib.decorators import morpy_wrap


# Suppress linting for mandatory arguments.
# noinspection PyUnusedLocal
@morpy_wrap
def template(trace: dict, app_dict: dict) -> None:
    r"""
    This function is a template.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: -

    :example:
        template(trace, app_dict)
    """

    # OPTION enable/disable logging
    # ??? trace["log_enable"] = False

    # FULL TEXT HERE
    morPy.log(trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["app"]["MESSAGE_KEY"]}')

    """
    >>> CODE OF FUNCTION
    """


class TemplateClass:
    r"""
    This class is a template.

    !! LIMITATIONS IN MULTIPROCESSING !!
    Storing classes in `app_dict` to share them across processes may fail, because it's attributes
    are not propagated reliably to other processes. See README.md for more details.
    """


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def __init__(self, trace: dict, app_dict: dict) -> None:
        r"""
        Class constructor.

        :param trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :example:
            my_class = TemplateClass(trace, app_dict)
        """

        # OPTION enable/disable logging
        # ??? trace["log_enable"] = False

        # FULL TEXT HERE
        morPy.log(trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["app"]["MESSAGE_KEY"]}')

        """
        >>> CODE OF INITIALIZATION
        """


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def method(self, trace: dict, app_dict: dict) -> None:
        r"""
        METHOD DESCRIPTION

        :param trace: operation credentials and tracing information
        :param app_dict: morPy global dictionary containing app configurations

        :return: -

        :example:
            TemplateClass.method(trace, app_dict)
        """

        # OPTION enable/disable logging
        # ??? trace["log_enable"] = False

        # FULL TEXT HERE
        morPy.log(trace, app_dict, "info",
            lambda: f'{app_dict["loc"]["app"]["MESSAGE_KEY"]}')

        """
        >>> CODE OF METHOD
        """
