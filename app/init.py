r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     AUTHOR
Descr.:     DESCRIPTION
"""

import morPy
from lib.decorators import morpy_wrap

from UltraDict import UltraDict


@morpy_wrap
def init(trace: dict, app_dict: dict | UltraDict) -> dict:
    r"""
    This function runs the initialization workflow of the app.

    :param trace: operation credentials and tracing information
    :param app_dict: morPy global dictionary containing app configurations

    :return: dict
        app_dict_n_shared: App dictionary, which is not shared with child processes
            or the orchestrator. Efficient to share data in between app phases 'app.init',
            'app.run' and 'app.exit'.
    """

    # OPTION enable/disable logging
    # ??? trace["log_enable"] = False

    app_dict_n_shared = dict()

    """
    >>> APP INITIALIZATION
    """

    return{
        'app_dict_n_shared' : app_dict_n_shared
        }
