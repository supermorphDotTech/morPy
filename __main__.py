r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Frontend of the morPy framework.
"""

from lib.exceptions import MorPyException

import sys

def initialize_morpy():
    r""" Initialize the morPy framework """

    from lib.init import init, init_cred

    check: bool = False
    init_trace: dict | None = None
    init_dict: dict | None = None

    try:

        trace_pattern = init_cred()
        init_trace, init_dict, init_orch = init(trace_pattern)
        init_trace["module"] = trace_pattern["module"]
        init_trace["operation"] = trace_pattern["operation"]
        init_trace["tracing"] = trace_pattern["tracing"]

        if init_dict and init_orch:
            check: bool = True
        return init_trace, init_dict, init_orch, check

    except Exception as init_e:
        init_trace = init_trace if init_trace else None
        init_dict = init_dict if init_dict else None
        raise MorPyException(init_trace, init_dict, init_e, sys.exc_info()[-1].tb_lineno, "critical")

def main(main_trace, main_dict, main_orch):
    r""" Run morPy """

    main_orch.run(main_trace, main_dict)

def finalize_morpy(final_trace, final_dict):
    r""" Finalize morPy runtime """

    from lib.exit import end_runtime
    end_runtime(final_trace, final_dict)

    # Quit the program
    sys.exit()

if __name__ == '__main__':
    try:
        trace, app_dict, orchestrator, init_check = initialize_morpy()
        main(trace, app_dict, orchestrator)
    except Exception as e:
        # noinspection PyUnboundLocalVariable
        trace = trace if trace else None
        # noinspection PyUnboundLocalVariable
        app_dict = app_dict if app_dict else None
        raise MorPyException(trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")
    finally:
        try:
            finalize_morpy(trace, app_dict)
        except Exception as e:
            raise MorPyException(trace, app_dict, e, sys.exc_info()[-1].tb_lineno, "critical")