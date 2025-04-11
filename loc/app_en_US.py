r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module defines all descriptive, localized strings for use in the developed app.
            It is loaded during initialization.
"""

def loc_app() -> dict:

    r"""
    This dictionary defines all messages for app functions localized to a
    specific language.

    :param:
        -

    :return: dict
        loc_app_dict: Localization dictionary for app functions. All keys
            will be copied to app_dict during morPy initialization.

    :example:
        app_dict["loc"]["app"][KEY]
    """

    loc_app_dict = {

        # App specific area - BEGIN

        "demo_starting" : "Starting",
        "demo_title" : "Progress Tracking Demo",
        "demo_finished" : "Finished",
        "demo_begin_stage" : "Beginning stage",
        "demo_step" : "Step",
        "demo_executed" : "Parallel task executed.",

        # App specific area - END
    }

    return loc_app_dict

def loc_app_dbg() -> dict:

    r"""
    This dictionary defines all messages for debugging app functions localized to a
    specific language.

    :param:
        -

    :return: dict
        loc_app_dbg_dict: Localization dictionary for app functions. All keys
            will be copied to app_dict during morPy initialization.

    :example:
        app_dict["loc"]["app"][KEY]
    """

    loc_app_dbg_dict = {

        # App specific area - BEGIN

        "my_dbg_message": "A debug message!",

        # App specific area - END
    }

    return loc_app_dbg_dict