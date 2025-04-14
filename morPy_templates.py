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
    This is a template function intended for demonstration purposes. It serves as a
    starting point for creating new morPy operations. Replace the inner placeholder
    code with your actual implementation.

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
    This template class is provided as an example. Note that storing class definitions
    in the global app configuration for sharing across processes may not propagate attributes
    reliably (see README.md for details).
    """


    # Suppress linting for mandatory arguments.
    # noinspection PyUnusedLocal
    @morpy_wrap
    def __init__(self, trace: dict, app_dict: dict) -> None:
        r"""
        Initializes the TemplateClass instance using tracing and the morPy global
        configuration. This constructor logs an informational message and includes
        placeholder code for further initialization.

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
        Example method of the TemplateClass. It logs an informational message and is intended
        as a placeholder for actual class functionality.

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
